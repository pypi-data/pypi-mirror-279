import numpy as np


class NumpyArrayWrapper(np.ndarray):
    def __new__(cls, input_array, *args, **kwargs):
        obj = np.asarray(input_array).view(cls)
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return

    def _tensorhue_to_numpy(self):
        return self
