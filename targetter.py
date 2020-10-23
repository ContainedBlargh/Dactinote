from typing import Callable
import numpy as np

"""
A module that takes a data source and applies a user defined function to turn it into a target value.
This could, e.g. be the state of an accelerometer or compass.
"""

class Targetter:

    def target(self, input_data: np.ndarray) -> float:
        return self.target_func(input_data)

    def __init__(self, target_func: Callable[[np.ndarray], float]):
        self.target_func: Callable[[np.ndarray], float] = target_func

