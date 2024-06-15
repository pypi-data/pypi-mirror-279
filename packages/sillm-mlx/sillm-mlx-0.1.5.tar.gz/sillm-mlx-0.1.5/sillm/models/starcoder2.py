from typing import Optional, Tuple

import mlx.core as mx
import mlx.nn as nn

from sillm.models.base import BaseModel
from sillm.models.args import ModelArgs
import sillm.models.llama as llama

class Attention(llama.Attention):
    """
    Multi-head attention module.
    """
    def __init__(self, args: ModelArgs):
        """
        Args:
            args: Model arguments.
        """
        nn.Module.__init__(self)
        self.args = args

        self.n_heads: int = args.n_heads
        self.n_kv_heads: int = args.n_kv_heads

        self.scale = self.args.head_dim ** -0.5

        self.wq = nn.Linear(args.dim, args.n_heads * args.head_dim, bias=True)
        self.wk = nn.Linear(args.dim, args.n_kv_heads * args.head_dim, bias=True)
        self.wv = nn.Linear(args.dim, args.n_kv_heads * args.head_dim, bias=True)
        self.wo = nn.Linear(args.n_heads * args.head_dim, args.dim, bias=True)

        self.rope = nn.RoPE(args.head_dim,
                            traditional=args.rope_traditional,
                            base=args.rope_theta
                            )

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

        self.w1 = nn.Linear(args.dim, args.hidden_dim, bias=True)
        self.w2 = nn.Linear(args.hidden_dim, args.dim, bias=True)

    def __call__(self,
                 x: mx.array
                 ) -> mx.array:
        """
        Args:
            x: Input tensor.
        Returns:
            Output tensor.
        """
        return self.w2(nn.gelu(self.w1(x)))

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
        self.feed_forward = FeedForward(args=args)
        self.attention_norm = nn.LayerNorm(args.dim, eps=args.norm_eps)
        self.ffn_norm = nn.LayerNorm(args.dim, eps=args.norm_eps)

########
# References:
# https://github.com/bigcode-project/starcoder2/
# https://github.com/huggingface/transformers/blob/main/src/transformers/models/starcoder2/modeling_starcoder2.py
########
class Model(llama.Model):
    """
    Starcoder2 model wrapper.
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
        self.layers = [TransformerBlock(args=args) for _ in range(args.n_layers)]
        self.norm = nn.LayerNorm(args.dim, eps=args.norm_eps)

        if args.tie_word_embeddings:
            self.output = None
        else:
            self.output = nn.Linear(args.dim, args.vocab_size, bias=False)

    def __call__(self,
                 inputs: mx.array,
                 cache = None
                 ):
        """
        Args:
            inputs: Input tokens.
            cache: Cache from previous forward pass.
        Returns:
            Output logits and cache.
        """
        h = self.tok_embeddings(inputs)

        mask = None
        if h.shape[1] > 1:
            mask = nn.MultiHeadAttention.create_additive_causal_mask(h.shape[1])
            mask = mask.astype(h.dtype)

        if cache is None:
            cache = [None] * len(self.layers)

        for e, layer in enumerate(self.layers):
            h, cache[e] = layer.forward(h, mask, cache[e])

        if self.output is None:
            out = self.tok_embeddings.as_linear(self.norm(h))
        else:
            out = self.output(self.norm(h))

        return out, cache