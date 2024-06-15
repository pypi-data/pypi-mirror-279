from typing import Optional, Tuple

import mlx.core as mx
import mlx.nn as nn

from sillm.models.base import BaseModel
from sillm.models.args import ModelArgs
import sillm.models.llama as llama

########
# Based on Phi-3 model implementation by Microsoft:
# https://huggingface.co/microsoft/Phi-3-mini-128k-instruct/blob/38143357bf52ce57009ecbd58cf9f0b0029cb393/modeling_phi3.py#L142
########
class SuScaledRotaryEmbedding(nn.RoPE):
    """
    Phi-3 Scaled Uniform RoPE.
    """
    def __init__(self,
                 args: ModelArgs,
                 head_dim: int
                 ):
        """
        Args:
            head_dim: Head dimension.
            base: Base for the RoPE.
        """
        super().__init__(head_dim, base=args.rope_theta, traditional=args.rope_traditional)

        self.short_factor = args.rope_scaling["short_factor"]
        self.long_factor = args.rope_scaling["long_factor"]
        self.original_max_position_embeddings = args.original_max_position_embeddings

        raise NotImplementedError("Scaled Uniform RoPE is not fully implemented")

########
# Based on Phi-3 model implementation by Microsoft:
# https://huggingface.co/microsoft/Phi-3-mini-128k-instruct/blob/38143357bf52ce57009ecbd58cf9f0b0029cb393/modeling_phi3.py#L194
########
class YarnScaledRotaryEmbedding(nn.RoPE):
    """
    Phi-3 Yarn RoPE.
    """
    def __init__(self,
                 args: ModelArgs,
                 head_dim: int
                 ):
        """
        Args:
            head_dim: Head dimension.
            base: Base for the RoPE.
        """
        super().__init__(head_dim, base=args.rope_theta, traditional=args.rope_traditional)

        self.short_factor = args.rope_scaling["short_factor"]
        self.long_factor = args.rope_scaling["long_factor"]
        self.original_max_position_embeddings = args.original_max_position_embeddings

        raise NotImplementedError("Yarn RoPE is not fully implemented")

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

        self.n_heads: int = args.n_heads
        self.n_kv_heads: int = args.n_kv_heads
        self.head_dim: int = args.dim // self.n_heads

        self.scale = self.args.head_dim ** -0.5

        op_size = args.n_heads * self.head_dim + 2 * (args.n_kv_heads * args.head_dim)

        self.wqkv = nn.Linear(args.dim, op_size, bias=False)
        self.wo = nn.Linear(args.n_heads * args.head_dim, args.dim, bias=False)
        
        if args.rope_scaling is not None:
            # TODO implement Phi3LongScaledRotaryEmbedding & Phi3YarnScaledRotaryEmbedding
            if args.rope_scaling["type"] == "su":
                self.rope = SuScaledRotaryEmbedding(args, args.head_dim)
            elif args.rope_scaling["type"] == "yarn":
                self.rope = YarnScaledRotaryEmbedding(args, args.head_dim)
            else:
                raise NotImplementedError(f"Unknown scaling type {args.rope_scaling['type']}")
        else:
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
        query_pos = self.n_heads * self.head_dim
        queries, keys, values = mx.split(qkv, [query_pos, query_pos + self.n_kv_heads * self.head_dim], axis=-1)

        queries = queries.reshape(B, L, self.n_heads, -1).transpose(0, 2, 1, 3)
        keys = keys.reshape(B, L, self.n_kv_heads, -1).transpose(0, 2, 1, 3)
        values = values.reshape(B, L, self.n_kv_heads, -1).transpose(0, 2, 1, 3)

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

class FeedForward(nn.Module):
    """
    Feed-forward module.
    """
    def __init__(self, args: ModelArgs):
        """
        Args:
            args: Model arguments.
        """
        super().__init__()

        self.w1 = nn.Linear(args.dim, 2 * args.hidden_dim, bias=False)
        self.w2 = nn.Linear(args.hidden_dim, args.dim, bias=False)

    def __call__(self,
                 x: mx.array
                 ) -> mx.array:
        """
        Args:
            x: Input tensor.
        Returns:
            Output tensor.
        """
        x = self.w1(x)
        gate, x = mx.split(x, 2, axis=-1)

        return self.w2(x * nn.silu(gate))

class TransformerBlock(llama.TransformerBlock):
    """
    Transformer block.
    """
    def __init__(self, args: ModelArgs):
        """
        Args:
            args: Model arguments.
        """
        nn.Module.__init__(self)

        self.args = args

        self.n_heads = args.n_heads
        self.dim = args.dim

        self.attention = Attention(args=args)
        self.attention_norm = nn.RMSNorm(args.dim, eps=args.norm_eps)
        self.feed_forward = FeedForward(args=args)
        self.ffn_norm = nn.RMSNorm(args.dim, eps=args.norm_eps)

class Model(llama.Model):
    """
    Phi-3 model wrapper.
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
        
        self.tok_embeddings = nn.Embedding(args.vocab_size, args.dim)
        # TODO add optional dropout layer with embd_pdrop parameter
        self.layers = [TransformerBlock(args=args) for _ in range(args.n_layers)]
        self.norm = nn.RMSNorm(args.dim, eps=args.norm_eps)
        self.output = nn.Linear(args.dim, args.vocab_size, bias=False)