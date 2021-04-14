import numpy as np
from willard.const import state, gate, GateBuilder


class qint:
    def __init__(self, qreg, size, offset):
        self.qreg = qreg
        self.size = size
        self.offset = offset

    def __getitem__(self, idx):
        self._check_idx(idx)
        return self.offset + idx

    def x(self, idx):
        self._check_idx(idx)
        self.qreg.x(self.offset + idx)
        return self

    def rnot(self, idx):
        self._check_idx(idx)
        self.qreg.rnot(self.offset + idx)
        return self

    def y(self, idx):
        self._check_idx(idx)
        self.qreg.y(self.offset + idx)
        return self

    def z(self, idx):
        self._check_idx(idx)
        self.qreg.z(self.offset + idx)
        return self

    def h(self, idx):
        self._check_idx(idx)
        self.qreg.h(self.offset + idx)
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
        self.qreg.phase(deg, self.offset + idx)
        return self

    def phase_dg(self, *, deg, idx):
        return self.phase(deg=-deg, idx=idx)

    def measure(self, idx):
        self._check_idx(idx)
        return self.qreg.measure(self.offset + idx)

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

    def cx(self, c, d):
        """
        c: index of the condition qubit
        d: index of the destination qubit
        """
        self._check_idx(c)
        self._check_idx(d)
        if c == d:
            raise IndexError(f'Index ({c},{d}) is not valid')
        self.qreg.cx(self.offset + c, self.offset + d)
        return self

    def cphase(self, deg, c, d):
        """
        c: index of the condition qubit
        d: index of the destination qubit
        """
        return self.cu(c=c, d=d, u=gate.phase(deg))

    def swap(self, *, c, d):
        self.cnot(c=c, d=d).cnot(c=d, d=c).cnot(c=c, d=d)

    def toffoli(self, *, c1, c2, d):
        self._check_idx(c1)
        self._check_idx(c2)
        self._check_idx(d)
        if 3 > len(set([c1, c2, d])):
            raise IndexError(f'Index ({c1},{c2},{d}) is not valid')

        self.state = self.gb.toffoli(c1=c1, c2=c2, d=d).dot(self.state)
        return self

    def cswap(self, *, c, d1, d2):
        return self.toffoli(c1=c, c2=d1, d=d2).toffoli(c1=c, c2=d2, d=d1).toffoli(c1=c, c2=d1, d=d2)

    def swap_test(self, *, input1: int, input2: int, output: int):
        """
        0 if input1 != input2
        1 if input1 == input2
        1 or 0 when input1 and input2 resembles
        """
        self.h(output)
        self.cswap(c=output, d1=input1, d2=input2)
        self.h(output)
        self.x(output)
        return self

    def _check_idx(self, idx):
        if idx < 0 or idx >= self.size:
            raise IndexError(f'Index {idx} is out of the range')


class qreg:
    def __init__(self, size) -> None:
        if size < 1:
            raise ValueError(
                f"num_bits should be bigger than 0. Got {size}")
        self.size = size
        self.gb = GateBuilder(size)
        self.state = state.ket('0' * size)
        self.offset = 0

    def int(self, size) -> qint:
        q = qint(self, size, self.offset)
        self.offset += size
        return q

    def reset(self):
        self.state = state.ket('0' * self.num_bits)
        return self

    def x(self, idx):
        self._check_idx(idx)
        self.state = self.gb.x(idx).dot(self.state)
        return self

    def rnot(self, idx):
        self._check_idx(idx)
        self.state = self.gb.rnot(idx).dot(self.state)
        return self

    def y(self, idx):
        self._check_idx(idx)
        self.state = self.gb.y(idx).dot(self.state)
        return self

    def z(self, idx):
        self._check_idx(idx)
        self.state = self.gb.z(idx).dot(self.state)
        return self

    def h(self, idx):
        self._check_idx(idx)
        self.state = self.gb.h(idx).dot(self.state)
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
        self.state = self.gb.phase(deg, idx).dot(self.state)
        return self

    def phase_dg(self, *, deg, idx):
        return self.phase(deg=-deg, idx=idx)

    def measure(self, idx):
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

    def swap(self, *, c, d):
        self.cnot(c=c, d=d).cnot(c=d, d=c).cnot(c=c, d=d)

    def toffoli(self, *, c1, c2, d):
        self._check_idx(c1)
        self._check_idx(c2)
        self._check_idx(d)
        if 3 > len(set([c1, c2, d])):
            raise IndexError(f'Index ({c1},{c2},{d}) is not valid')

        self.state = self.gb.toffoli(c1=c1, c2=c2, d=d).dot(self.state)
        return self

    def cswap(self, *, c, d1, d2):
        return self.toffoli(c1=c, c2=d1, d=d2).toffoli(c1=c, c2=d2, d=d1).toffoli(c1=c, c2=d1, d=d2)

    def swap_test(self, *, input1: int, input2: int, output: int):
        """
        0 if input1 != input2
        1 if input1 == input2
        1 or 0 when input1 and input2 resembles
        """
        self.h(output)
        self.cswap(c=output, d1=input1, d2=input2)
        self.h(output)
        self.x(output)
        return self

    def teleport(self, *, a: int, b: int, ch: int):
        """
        a: Alice
        b: Bob
        ch: Channel
        """
        self._check_idx(a)
        self._check_idx(b)
        self._check_idx(ch)
        if 3 > len(set([a, b, ch])):
            raise IndexError(f'Index ({a},{ch},{b}) is not valid')
        self.h(ch).cnot(c=ch, d=b)
        self.cnot(c=a, d=ch).h(a)
        a_result = self.measure(a)
        ch_result = self.measure(ch)
        if ch_result:
            self.x(b)
        if a_result:
            self.phase(deg=180, idx=b)
        return self

    def _check_idx(self, idx):
        if idx < 0 or idx >= self.size:
            raise IndexError(f'Index {idx} is out of the range')
