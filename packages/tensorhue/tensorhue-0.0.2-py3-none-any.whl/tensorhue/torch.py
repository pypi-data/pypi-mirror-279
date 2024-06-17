import torch
import numpy as np


def _tensorhue_to_numpy_torch(tensor: torch.Tensor) -> np.ndarray:
    if isinstance(tensor, torch.masked.MaskedTensor):
        return np.ma.masked_array(tensor.get_data(), torch.logical_not(tensor.get_mask()))
    else:
        try:
            return tensor.numpy()
        except:
            raise NotImplementedError(
                f"It looks like tensors of type {type(tensor)} cannot be converted\
            to numpy arrays out-of-the-box. Raise an issue if you need to visualize them."
            )
