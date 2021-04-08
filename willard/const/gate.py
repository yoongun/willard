import numpy as np
from willard.const import state


class _Gate:
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
        deg = -deg
        rad = deg / 180 * np.pi
        return np.array([[1, 0.], [0., np.exp(1.j * rad)]])

    @property
    def i(self):
        return np.eye(2)

    @property
    def subspace_0(self):
        return np.kron(state.ket_0.transpose(), state.ket_0)

    @property
    def subspace_1(self):
        return np.kron(state.ket_1.transpose(), state.ket_1)


gate = _Gate()


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

    def cnot(self, *, c, d):
        """
        c: index of the condition qubit
        d: index of the destination qubit
        """
        if c == 0 and d == 1:
            cnot_0 = np.kron(gate.i, subspace_0)
            cnot_1 = np.kron(gate.x, subspace_1)
            cnot = cnot_0 + cnot_1
            self.state = cnot.dot(self.state)
        elif c == 1 and d == 0:
            cnot_0 = np.kron(subspace_0, gate.i)
            cnot_1 = np.kron(subspace_1, gate.x)
            cnot = cnot_0 + cnot_1
            self.state = cnot.dot(self.state)
        else:
            raise IndexError('Index ({c},{d}) is not valid')
        return self

    def swap(self):
        self.cnot(c=0, d=1).cnot(c=1, d=0).cnot(c=0, d=1)
