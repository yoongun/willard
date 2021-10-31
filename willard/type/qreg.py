import numpy as np
from willard.const import state, gate, GateBuilder
from willard.type import qint


class qreg:
    def __init__(self, size) -> None:
        if size < 1:
            raise ValueError(
                f"size should be bigger than 0. Got {size}")
        self.size = size
        self.gb = GateBuilder(size)
        self.state = state.ket('0' * size)
        self._offset = 0

    def int(self, size, init_value) -> qint:
        q = qint(self, size, self._offset, init_value)
        if self._offset + size > self.size:
            raise ValueError(
                "This register is already full. Please try creating another register with larger size")
        self._offset += size
        return q

    def reset(self):
        self.state = state.ket('0' * self.size)
        return self

    def x(self, idx):
        self._check_idx(idx)
        self.state = self.gb.x(idx).mm(self.state)
        return self

    def rnot(self, idx):
        self._check_idx(idx)
        self.state = self.gb.rnot(idx).mm(self.state)
        return self

    def y(self, idx):
        self._check_idx(idx)
        self.state = self.gb.y(idx).mm(self.state)
        return self

    def z(self, idx):
        self._check_idx(idx)
        self.state = self.gb.z(idx).mm(self.state)
        return self

    def h(self, idx):
        self._check_idx(idx)
        self.state = self.gb.h(idx).mm(self.state)
        return self

    def s(self, idx):
        return self.phase(deg=90, idx=idx)

    def s_dg(self, idx):
        return self.phase_dg(deg=90, idx=idx)

    def t(self, idx):
        return self.phase(deg=45, idx=idx)

    def t_dg(self, idx):
        return self.phase_dg(deg=45, idx=idx)

    def phase(self, deg, idx):
        self._check_idx(idx)
        self.state = self.gb.phase(deg, idx).mm(self.state)
        return self

    def phase_dg(self, *, deg, idx):
        return self.phase(deg=-deg, idx=idx)

    def measure(self, idx):
        self._check_idx(idx)
        prob_0 = self.state.conj().T.mm(
            self.gb.measure_0(idx).mm(self.state)).abs().item()
        if prob_0 >= np.random.rand():
            self.state = self.gb.measure_0(idx).mm(
                self.state) / np.sqrt(prob_0)
            return 0
        self.state = self.gb.measure_1(idx).mm(
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
        self.state = self.gb.cu(c=c, d=d, u=u).mm(self.state)
        return self

    def ncu(self, cs: list, d: int, u):
        for c in cs:
            self._check_idx(c)
        self._check_idx(d)
        if len(cs) + 1 > len([*cs, d]):
            raise IndexError(f'Index ({cs},{d}) is not valid')
        self.state = self.gb.ncu(cs=cs, d=d, u=u).mm(self.state)
        return self

    def cx(self, c, d):
        """
        c: index of the condition qubit
        d: index of the destination qubit
        """
        return self.cu(c=c, d=d, u=gate.x)

    def cphase(self, *, c, d, deg):
        """
        c: index of the condition qubit
        d: index of the destination qubit
        """
        return self.cu(c=c, d=d, u=gate.phase(deg))

    def swap(self, c, d):
        self.cx(c, d).cx(d, c).cx(c, d)

    def toffoli(self, *, c1, c2, d):
        self._check_idx(c1)
        self._check_idx(c2)
        self._check_idx(d)
        if 3 > len(set([c1, c2, d])):
            raise IndexError(f'Index ({c1},{c2},{d}) is not valid')

        self.state = self.gb.toffoli(c1=c1, c2=c2, d=d).mm(self.state)
        return self

    def cswap(self, *, c, d1, d2):
        return self.toffoli(c1=c, c2=d1, d=d2).toffoli(c1=c, c2=d2, d=d1).toffoli(c1=c, c2=d1, d=d2)

    def _check_idx(self, idx):
        if idx < 0 or idx >= self.size:
            raise IndexError(f'Index {idx} is out of the range')
