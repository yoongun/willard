import numpy as np
from willard.const import gate, GateType


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

    def rnot(self, idx):
        result = [[1]]
        for i in range(self.num_bits):
            if i == idx:
                result = np.kron(gate.rnot, result)
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
                cu_1 = np.kron(gate.i, cu_1)
        return cu_0 + cu_1

    def cnot(self, *, c, d):
        """
        c: index of the condition qubit
        d: index of the destination qubit
        """
        return self.cu(c=c, d=d, u=gate.x)

    def swap(self, *, d1, d2):
        return self.cnot(c=d1, d=d2).dot(self.cnot(c=d1, d=d2)).dot(self.cnot(c=d1, d=d2))

    def toffoli(self, *, c1, c2, d):
        self._check_idx(c1)
        self._check_idx(c2)
        self._check_idx(d)
        if 3 > len(set([c1, c2, d])):
            raise IndexError(f'Index ({c1},{c2},{d}) is not valid')
        t00 = [[1]]
        t01 = [[1]]
        t10 = [[1]]
        t11 = [[1]]
        for i in range(self.num_bits):
            if i == c1:
                t00 = np.kron(gate.subspace_0, t00)
                t01 = np.kron(gate.subspace_1, t01)
                t10 = np.kron(gate.subspace_0, t10)
                t11 = np.kron(gate.subspace_1, t11)
            elif i == c2:
                t00 = np.kron(gate.subspace_0, t00)
                t01 = np.kron(gate.subspace_0, t01)
                t10 = np.kron(gate.subspace_1, t10)
                t11 = np.kron(gate.subspace_1, t11)
            elif i == d:
                t00 = np.kron(gate.i, t00)
                t01 = np.kron(gate.i, t01)
                t10 = np.kron(gate.i, t10)
                t11 = np.kron(gate.x, t11)
            else:
                t00 = np.kron(gate.i, t00)
                t01 = np.kron(gate.i, t01)
                t10 = np.kron(gate.i, t10)
                t11 = np.kron(gate.i, t11)
        return t00 + t01 + t10 + t11

    def cswap(self, *, c, d1, d2):
        return self.toffoli(c1=c, c2=d1, d=d2).dot(self.toffoli(c1=c, c2=d2, d=d1)).dot(self.toffoli(c1=c, c2=d1, d=d2))

    def _check_idx(self, idx):
        if idx < 0 or idx >= self.num_bits:
            raise IndexError(f'Index {idx} is out of the range')
