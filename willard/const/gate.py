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
