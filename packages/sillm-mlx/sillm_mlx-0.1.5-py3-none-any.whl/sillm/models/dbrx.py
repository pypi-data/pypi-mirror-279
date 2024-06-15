from typing import Optional, Tuple

import mlx.core as mx
import mlx.nn as nn

from sillm.models.base import BaseModel
from sillm.models.args import ModelArgs
import sillm.models.mixtral as mixtral

class Attention(nn.Module):
    """
    Multi-head attention module.
    """
    def __init__(self, args: ModelArgs):
        """
        Args:
            args: Model arguments.
        """
        super().__init__()
        self.args = args

        self.dim: int = args.dim
        self.head_dim: int = args.head_dim
        self.n_heads: int = args.n_heads
        self.n_kv_heads: int = args.n_kv_heads
        self.clip_qkv: float = args.clip_qkv

        self.scale = self.args.head_dim ** -0.5

        self.wqkv = nn.Linear(args.dim, (self.n_kv_heads * 2 + self.n_heads) * self.head_dim, bias=False)
        self.wo = nn.Linear(args.dim, args.dim, bias=False)
        self.rope = nn.RoPE(args.head_dim,
                            traditional=args.rope_traditional,
                            base=args.rope_theta)
        
    def __call__(self,
                 x: mx.array,
                 mask: Optional[mx.array] = None,
                 cache: Optional[Tuple[mx.array, mx.array]] = None,
                 ) -> mx.array:
        B, L, _ = x.shape

        qkv = self.wqkv(x)
        qkv = mx.clip(qkv, a_min=-self.clip_qkv, a_max=self.clip_qkv)
        splits = [self.dim, self.dim + self.head_dim * self.n_kv_heads]
        queries, keys, values = mx.split(qkv, splits, axis=-1)

        queries = queries.reshape(B, L, self.n_heads, -1).transpose(0, 2, 1, 3)
        keys = keys.reshape(B, L, self.n_kv_heads, -1).transpose(0, 2, 1, 3)
        values = values.reshape(B, L, self.n_kv_heads, -1).transpose(
            0, 2, 1, 3
        )

        if cache is not None:
            key_cache, value_cache = cache
            queries = self.rope(queries, offset=key_cache.shape[2])
            keys = self.rope(keys, offset=key_cache.shape[2])
            keys = mx.concatenate([key_cache, keys], axis=2)
            values = mx.concatenate([value_cache, values], axis=2)
        else:
            queries = self.rope(queries)
            keys = self.rope(keys)

        output = mx.fast.scaled_dot_product_attention(
            queries, keys, values, scale=self.scale, mask=mask
        )
        output = output.transpose(0, 2, 1, 3).reshape(B, L, -1)

        return self.wo(output), (keys, values)

class TransformerBlock(mixtral.TransformerBlock):
    """
    Transformer block for DBRX models.
    """
    def __init__(self, args: ModelArgs):
        nn.Module.__init__(self)

        self.n_heads = args.n_heads
        self.dim = args.dim
        self.attention = Attention(args=args)
        self.feed_forward = mixtral.FeedForward(args=args)
        self.attention_norm = nn.LayerNorm(args.dim, bias=False)
        self.ffn_norm = nn.LayerNorm(args.dim, bias=False)
        self.args = args

class Model(mixtral.Model):
    """
    DBRX model wrapper.
    """
    def __init__(self, args: ModelArgs):
        """
        Args:
            args: Model arguments.
        """
        BaseModel.__init__(self, args)
        self.args = args

        self.n_layers = args.n_layers
        self.vocab_size = args.vocab_size
        self.router_aux_loss_coef = args.router_aux_loss_coef

        self.tok_embeddings = nn.Embedding(args.vocab_size, args.dim)
        self.layers = [TransformerBlock(args=args) for _ in range(args.n_layers)]
        self.norm = nn.LayerNorm(args.dim, bias=False)
        self.output = nn.Linear(args.dim, args.vocab_size, bias=False)