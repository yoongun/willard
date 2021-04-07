import numpy as np


class State:
    @property
    def ket_0(self):
        return np.array([[1.], [0.]])

    @property
    def ket_1(self):
        return np.array([[0.], [1.]])

    @property
    def ket_00(self):
        return np.array([[1.], [0.], [0.], [0.]])


state = State()
