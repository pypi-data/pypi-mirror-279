import pathlib
import json
import logging
import dataclasses

from sillm.utils.mapping import map_config

logger = logging.getLogger("sillm")

@dataclasses.dataclass
class ModelArgs:
    """
    Model arguments.
    """
    model_type: str
    dim: int
    n_layers: int
    head_dim: int
    n_heads: int
    n_kv_heads: int
    norm_eps: float = None
    hidden_dim: int = None
    vocab_size: int = -1
    rope_theta: float = 10000.0
    rope_traditional: bool = True
    max_position_embeddings: int = 0
    tie_word_embeddings: bool = False
    bos_token_id: int = None
    eos_token_id: int = None
    pad_token_id: int = None
    quantization: dict = None

    def __repr__(self):
        return json.dumps(dataclasses.asdict(self), indent=4)
    
    def log_config(self):
        for k, v in dataclasses.asdict(self).items():
            if isinstance(v, dict):
                for k2, v2 in v.items():
                    logger.debug(f"Config {k}.{k2}: {v2}")
            else:
                logger.debug(f"Config {k}: {v}")
    
    def fix_config(self, weights):
        """
        Fix config with shape information from weights.
        """
        if self.hidden_dim is None and "layers.0.feed_forward.w1.weight" in weights:
            self.hidden_dim = weights["layers.0.feed_forward.w1.weight"].shape[0]
        if self.vocab_size <= 0 and "output.weight" in weights:
            self.vocab_size = weights["output.weight"].shape[0]

    def save_config(self, config_path):
        """
        Save model config to JSON file.
        Args:
            config_path: Path to config file.
        """
        config = dataclasses.asdict(self)
        
        # Remove None values
        for k in list(config.keys()):
            if config[k] is None:
                del config[k]

        with open(config_path, "w") as f:
            f.write(json.dumps(config, indent=4))

    @staticmethod
    def load_config(config):
        ArgsClass = None
        if "model_type" in config:
            if config["model_type"] in ("llama", "mistral", "gemma"):
                ArgsClass = LlamaArgs
            elif config["model_type"] == "mixtral":
                ArgsClass = MixtralArgs
            elif config["model_type"] == "phi":
                ArgsClass = PhiArgs
            elif config["model_type"] == "qwen2":
                ArgsClass = Qwen2Args
            elif config["model_type"] == "starcoder2":
                ArgsClass = Starcoder2Args
            elif config["model_type"] == "dbrx":
                ArgsClass = DbrxArgs
            elif config["model_type"] == "cohere":
                ArgsClass = CohereArgs
            elif config["model_type"] == "phi3":
                ArgsClass = Phi3Args
            else:
                ArgsClass = LlamaArgs
        if ArgsClass is None:
            ArgsClass = LlamaArgs
            config["model_type"] = "llama"
            logger.warn(f"No model type specified - falling back to `llama` config")

        fields = ModelArgs.__annotations__
        fields.update(ArgsClass.__annotations__)
        config = {k:v for k, v in config.items() if k in fields}

        return ArgsClass(**config)
    
    @staticmethod
    def load_file(config_path):
        """
        Load model config from JSON file.
        Args:
            config_path: Path to config file.
        Returns:
            ModelArgs instance.
        """
        assert pathlib.Path(config_path).exists(), config_path

        with open(config_path, "r") as f:
            config = json.loads(f.read())
        config = map_config(config)

        return ModelArgs.load_config(config)
    
@dataclasses.dataclass
class LlamaArgs(ModelArgs):
    """
    Llama model arguments.
    """
    rope_scaling: dict = None

@dataclasses.dataclass
class MixtralArgs(ModelArgs):
    """
    Mixtral model arguments.
    """
    rope_theta: float = 1000000.0
    rope_scaling: dict = None
    router_aux_loss_coef: float = 0.001
    moe: dict = None

    def __post_init__(self):
        if self.moe is None:
            self.moe = {
                "num_experts": 8,
                "num_experts_per_tok": 2
            }

@dataclasses.dataclass
class PhiArgs(ModelArgs):
    """
    Phi model arguments.
    """
    rope_scaling: dict = None
    partial_rotary_factor: float = 0.4

@dataclasses.dataclass
class Qwen2Args(ModelArgs):
    """
    Starcoder2 model arguments.
    """
    rope_scaling: dict = None

@dataclasses.dataclass
class Starcoder2Args(ModelArgs):
    """
    Starcoder2 model arguments.
    """
    rope_scaling: dict = None
    tie_word_embeddings: bool = True

@dataclasses.dataclass
class DbrxArgs(ModelArgs):
    """
    DBRX model arguments.
    """
    clip_qkv: int = 8
    rope_theta: float = 500000.0
    router_aux_loss_coef: float = 0.05
    moe: dict = None

    def __post_init__(self):
        if self.moe is None:
            self.moe = {
                "num_experts": 16,
                "num_experts_per_tok": 4
            }

        if self.bos_token_id is None:
            self.bos_token_id = 100257
        if self.eos_token_id is None:
            self.eos_token_id = 100257

@dataclasses.dataclass
class CohereArgs(ModelArgs):
    """
    Cohere model arguments.
    """
    norm_bias: bool = False
    logit_scale: float = 0.0625
    use_qk_norm: bool = False

@dataclasses.dataclass
class Phi3Args(ModelArgs):
    """
    Phi-3 model arguments.
    """
    rope_scaling: dict = None
    embd_pdrop: float = 0.0