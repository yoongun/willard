import numpy as np
import torch


class StateType:
    def ket(self, bit_array: str):
        state = np.array([[1.]])
        for bit in bit_array:
            if bit == '0':
                state = np.kron(state, np.array([[1.], [0.]]))
            elif bit == '1':
                state = np.kron(state, np.array([[0.], [1.]]))
            else:
                raise ValueError(
                    f"bit_array should contain either '0' or '1', but {bit} has found")
        return state


state = StateType()
