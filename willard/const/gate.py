import numpy as np
from willard.const import state


class GateType:
    @property
    def x(self):
        return np.array([[0., 1.], [1., 0.]])

    @property
    def y(self):
        return np.array([[0., -1.j], [1.j, 0.]])

    @property
    def z(self):
        return np.array([[1., 0.], [0., -1.]])

    @property
    def h(self):
        return np.array([[1. / np.sqrt(2), 1. / np.sqrt(2)],
                         [1. / np.sqrt(2), -1. / np.sqrt(2)]])

    @property
    def s(self):
        return self.phase(90)

    @property
    def s_dg(self):
        return self.phase(-90)

    @property
    def t(self):
        return self.phase(45)

    @property
    def t_dg(self):
        return self.phase(-45)

    def phase(self, deg):
        rad = deg / 180 * np.pi
        return np.array([[1, 0.], [0., np.exp(1.j * rad)]])

    def phase_dg(self, deg):
        return self.phase(-deg)

    @property
    def i(self):
        return np.eye(2)

    @property
    def subspace_0(self):
        return np.kron(state.ket('0').conj().T, state.ket('0'))

    @property
    def subspace_1(self):
        return np.kron(state.ket('1').conj().T, state.ket('1'))


gate = GateType()


class GateBuilder:
    def __init__(self, num_bits: int) -> None:
        self.num_bits = num_bits

    def x(self, idx):
        result = [[1]]
        for i in range(self.num_bits):
            if i == idx:
                result = np.kron(gate.x, result)
            else:
                result = np.kron(gate.i, result)
        return result

    def y(self, idx):
        result = [[1]]
        for i in range(self.num_bits):
            if i == idx:
                result = np.kron(gate.y, result)
            else:
                result = np.kron(gate.i, result)
        return result

    def z(self, idx):
        result = [[1]]
        for i in range(self.num_bits):
            if i == idx:
                result = np.kron(gate.z, result)
            else:
                result = np.kron(gate.i, result)
        return result

    def h(self, idx):
        result = [[1]]
        for i in range(self.num_bits):
            if i == idx:
                result = np.kron(gate.h, result)
            else:
                result = np.kron(gate.i, result)
        return result

    def s(self, idx):
        result = [[1]]
        for i in range(self.num_bits):
            if i == idx:
                result = np.kron(gate.s, result)
            else:
                result = np.kron(gate.i, result)
        return result

    def t(self, idx):
        result = [[1]]
        for i in range(self.num_bits):
            if i == idx:
                result = np.kron(gate.t, result)
            else:
                result = np.kron(gate.i, result)
        return result

    def phase(self, deg, idx):
        result = [[1]]
        for i in range(self.num_bits):
            if i == idx:
                result = np.kron(gate.phase(deg), result)
            else:
                result = np.kron(gate.i, result)
        return result

    def measure_0(self, idx):
        result = [[1]]
        for i in range(self.num_bits):
            if i == idx:
                result = np.kron(gate.subspace_0, result)
            else:
                result = np.kron(gate.i, result)
        return result

    def measure_1(self, idx):
        result = [[1]]
        for i in range(self.num_bits):
            if i == idx:
                result = np.kron(gate.subspace_1, result)
            else:
                result = np.kron(gate.i, result)
        return result

    def i(self):
        result = [[1]]
        for i in range(self.num_bits):
            result = np.kron(gate.i, result)
        return result

    def cu(self, *, c, d, u: GateType):
        """
        c: index of the condition qubit
        d: index of the destination qubit
        """
        self._check_idx(c)
        self._check_idx(d)
        if c == d:
            raise IndexError(f'Index ({c},{d}) is not valid')
        cu_0 = [[1]]
        cu_1 = [[1]]
        for i in range(self.num_bits):
            if i == c:
                cu_0 = np.kron(gate.subspace_0, cu_0)
                cu_1 = np.kron(gate.subspace_1, cu_1)
            elif i == d:
                cu_0 = np.kron(gate.i, cu_0)
                cu_1 = np.kron(u, cu_1)
            else:
                cu_0 = np.kron(gate.i, cu_0)
                cu_1 = np.kron(u, cu_1)
        return cu_0 + cu_1

    def cnot(self, *, c, d):
        """
        c: index of the condition qubit
        d: index of the destination qubit
        """
        return self.cu(c=c, d=d, u=gate.x)

    def swap(self):
        self.cnot(c=0, d=1).cnot(c=1, d=0).cnot(c=0, d=1)

    def _check_idx(self, idx):
        if idx < 0 or idx >= self.num_bits:
            raise IndexError(f'Index {idx} is out of the range')
