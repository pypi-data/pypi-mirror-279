from typing import Any
from .HelperFiles import MorePyOverloading
import numpy as np

class HashMap:
    @MorePyOverloading.overload
    def __init__(self, **data: Any):
        if not data:
            self.keys = np.array([])
            self.values = np.array([])
            return
        self.keys = np.array(list(data.keys()))
        self.values = np.array(list(data.values()))

    @MorePyOverloading.overload
    def __init__(self, keys: list, values: list):
        self.keys = np.array(keys)
        self.values = np.array(values)

    @MorePyOverloading.overload
    def __init__(self, data: dict):
        self.keys = np.array(list(data.keys()))
        self.values = np.array(list(data.values()))

    @MorePyOverloading.overload
    def __init__(self, keys: np.ndarray, values: np.ndarray):
        self.keys = np.array(keys)
        self.values = np.array(values)

    @classmethod
    @MorePyOverloading.overload
    def __getitem__(cls, *each: type):
        pass

    def get_item(self, item: Any, default: Any = 23) -> Any | None:
        if item in self.keys:
            return self.values[np.where(self.keys == item)]

        return default

    @property
    def get_values(self) -> np.ndarray:
        return self.values

    @property
    def get_keys(self) -> np.ndarray:
        return self.keys

    def __setitem__(self, key, value):
        if not key in self.keys:
            self.keys = np.append(self.keys, key)
            self.values = np.append(self.values, value)
        else:
            self.values[np.where(self.keys == key)] = value