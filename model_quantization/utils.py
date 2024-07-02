import torch

import numpy as np


# Utils
def print_param_dtype(model):
    for name, param in model.named_parameters():
        print(f"{name} is loaded in {param.dtype}")
        break


def named_module_tensors(module, recurse=False):
    for named_parameter in module.named_parameters(recurse=recurse):
        name, val = named_parameter
        flag = True
        if hasattr(val, "_data") or hasattr(val, "_scale"):
            if hasattr(val, "_data"):
                yield name + "._data", val._data
            if hasattr(val, "_scale"):
                yield name + "._scale", val._scale
        else:
            yield named_parameter

    for named_buffer in module.named_buffers(recurse=recurse):
        yield named_buffer


def dtype_byte_size(dtype):
    """
    Returns the size (in bytes) occupied by one parameter of type `dtype`.
    """
    import re

    if dtype == torch.bool:
        return 1 / 8
    bit_search = re.search(r"[^\d](\d+)$", str(dtype))
    if bit_search is None:
        raise ValueError(f"`dtype` is not a valid dtype: {dtype}.")
    bit_size = int(bit_search.groups()[0])
    return bit_size // 8


def compute_module_sizes(model):
    """
    Compute the size of each submodule of a given model.
    """
    from collections import defaultdict

    module_sizes = defaultdict(int)
    for name, tensor in named_module_tensors(model, recurse=True):
        size = tensor.numel() * dtype_byte_size(tensor.dtype)
        name_parts = name.split(".")
        for idx in range(len(name_parts) + 1):
            module_sizes[".".join(name_parts[:idx])] += size

    return module_sizes


# 1. Calculate Minimum and Maximum Values
def calculate_min_max(values):
    x_min = np.min(values)
    x_max = np.max(values)
    return x_min, x_max


# 2. Compute Scale and Zero-Point
def compute_scale_zero_point(x_min, x_max, q_min, q_max):
    s = (x_max - x_min) / (q_max - q_min)
    z = q_min - (x_min / s)
    return s, z


# 3. Quantize the Values
def quantize_value(x, s, z):
    q = np.round(x / s + z)

    return q


# 4. Dequantize to Verify
def dequantize_value(q, s, z):
    x_dequantized = s * (q - z)
    return x_dequantized
