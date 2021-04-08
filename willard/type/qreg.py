import numpy as np
from willard.const import state, gate, GateBuilder


class qreg:
    def __init__(self, num_bits) -> None:
        if num_bits < 1:
            raise ValueError(
                f"num_bits should be bigger than 0. Got {num_bits}")
        self.num_bits = num_bits
        self.gb = GateBuilder(num_bits)
        self.state = state.ket('0' * num_bits)

    def x(self, idx=0):
        self._check_idx(idx)
        self.state = self.gb.x(idx).dot(self.state)
        return self

    def y(self, idx=0):
        self._check_idx(idx)
        self.state = self.gb.y(idx).dot(self.state)
        return self

    def z(self, idx=0):
        self._check_idx(idx)
        self.state = self.gb.z(idx).dot(self.state)
        return self

    def h(self, idx=0):
        self._check_idx(idx)
        self.state = self.gb.h(idx).dot(self.state)
        return self

    def s(self, idx=0):
        return self.phase(90, idx)

    def s_dg(self, idx=0):
        return self.phase_dg(90, idx)

    def t(self, idx=0):
        return self.phase(45, idx)

    def t_dg(self, idx=0):
        return self.phase_dg(45, idx)

    def phase(self, deg, idx=0):
        self._check_idx(idx)
        self.state = self.gb.phase(deg, idx).dot(self.state)
        return self

    def phase_dg(self, deg, idx=0):
        return self.phase(-deg, idx)

    def measure(self, idx=0):
        self._check_idx(idx)
        prob_0 = self.state.conj().T.dot(self.gb.measure_0(idx).dot(self.state))
        if prob_0 >= np.random.rand():
            self.state = self.gb.measure_0(idx).dot(
                self.state) / np.sqrt(prob_0)
            return 0
        self.state = self.gb.measure_1(idx).dot(
            self.state) / np.sqrt(1. - prob_0)
        return 1

    def cu(self, *, c, d, u):
        """
        c: index of the condition qubit
        d: index of the destination qubit
        """
        self._check_idx(c)
        self._check_idx(d)
        if c == d:
            raise IndexError(f'Index ({c},{d}) is not valid')
        self.state = self.gb.cu(c=c, d=d, u=u).dot(self.state)
        return self

    def cnot(self, *, c, d):
        """
        c: index of the condition qubit
        d: index of the destination qubit
        """
        return self.cu(c=c, d=d, u=gate.x)

    def swap(self, *, c, d):
        self.cnot(c=c, d=d).cnot(c=d, d=c).cnot(c=c, d=d)

    def _check_idx(self, idx):
        if idx < 0 or idx >= self.num_bits:
            raise IndexError(f'Index {idx} is out of the range')
