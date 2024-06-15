import random

import numpy as np
import mlx.core as mx

import yaml

def seed(seed):
    """
    Seed random number generators.
    
    Args:
        seed: The seed value.
    """
    random.seed(seed)
    mx.random.seed(seed)
    np.random.seed(seed)

def load_yaml(fpath, args):
    with open(fpath, "r") as f:
        config = yaml.safe_load(f)

        for key, value in config.items():
            setattr(args, key, value)