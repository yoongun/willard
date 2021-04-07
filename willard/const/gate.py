import numpy as np


class Gate:
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
        # return self.phase(90)
        return np.array([[1, 0.], [0., 1.j]])

    @property
    def t(self):
        # return self.phase(45)
        return np.array([[1, 0.], [0., np.exp(1.j * np.pi / 4)]])

    def phase(self, deg):
        rad = deg / 180 * np.pi
        return np.array([[1, 0.], [0., np.exp(1.j * rad)]])

    @property
    def i(self):
        return np.eye(2)


gate = Gate()
