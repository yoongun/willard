import numpy as np
from willard.const import state, gate


def qucrumb():
    return qreg(2)


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
