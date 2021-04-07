import numpy as np
from willard.const import state, gate


class qubit:
    def __init__(self):
        self.state = state.ket_0

    def x(self):
        self.state = gate.x.dot(self.state)
        return self

    def y(self):
        self.state = gate.y.dot(self.state)
        return self

    def z(self):
        self.state = gate.z.dot(self.state)
        return self

    def h(self):
        self.state = gate.h.dot(self.state)
        return self

    def s(self):
        self.phase(90)
        return self

    def t(self):
        self.phase(45)
        return self

    def phase(self, deg):
        rad = deg / 180 * np.pi
        phase = np.array([[1, 0.], [0., np.exp(1.j * rad)]])
        self.state = phase.dot(self.state)
        return self

    def measure(self):
        prob_0 = self.state[0] ** 2
        if prob_0 >= np.random.rand():
            self.state = state.ket_0
            return 0
        self.state = state.ket_1
        return 1


class qucrumb:
    def __init__(self):
        self.state = state.ket_00

    def x(self, idx):
        if idx == 0:
            self.state = np.kron(gate.i, gate.x).dot(self.state)
            return self
        elif idx == 1:
            self.state = np.kron(gate.x, gate.i).dot(self.state)
            return self
        raise IndexError('Index {idx} is out of the range')

    def y(self, idx):
        if idx == 0:
            self.state = np.kron(gate.i, gate.y).dot(self.state)
            return self
        elif idx == 1:
            self.state = np.kron(gate.y, gate.i).dot(self.state)
            return self
        raise IndexError('Index {idx} is out of the range')

    def z(self, idx):
        if idx == 0:
            self.state = np.kron(gate.i, gate.z).dot(self.state)
            return self
        elif idx == 1:
            self.state = np.kron(gate.z, gate.i).dot(self.state)
            return self
        raise IndexError('Index {idx} is out of the range')

    def h(self, idx):
        if idx == 0:
            self.state = np.kron(gate.i, gate.h).dot(self.state)
            return self
        elif idx == 1:
            self.state = np.kron(gate.h, gate.i).dot(self.state)
            return self
        raise IndexError('Index {idx} is out of the range')

    def s(self, idx):
        if idx == 0:
            self.state = np.kron(gate.i, gate.s).dot(self.state)
            return self
        elif idx == 1:
            self.state = np.kron(gate.s, gate.i).dot(self.state)
            return self
        raise IndexError('Index {idx} is out of the range')

    def t(self, idx):
        if idx == 0:
            self.state = np.kron(gate.i, gate.t).dot(self.state)
            return self
        elif idx == 1:
            self.state = np.kron(gate.t, gate.i).dot(self.state)
            return self
        raise IndexError('Index {idx} is out of the range')

    def cnot(self, *, c, d):
        """
        c: index of the condition qubit
        d: index of the destination qubit
        """
        subspace_0 = np.kron(state.ket_0.transpose(), state.ket_0)
        subspace_1 = np.kron(state.ket_1.transpose(), state.ket_1)
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
