import torch
import numpy as np
from willard.const import dirac


class GateType:
    @property
    def x(self):
        return torch.tensor([[0., 1.], [1., 0.]], dtype=torch.cfloat)

    @property
    def rnot(self):
        return torch.tensor([[0.5 + 0.5j, 0.5 - 0.5j],
                             [0.5 - 0.5j, 0.5 + 0.5j]], dtype=torch.cfloat)

    @property
    def y(self):
        return torch.tensor([[0., -1.j], [1.j, 0.]], dtype=torch.cfloat)

    @property
    def z(self):
        return torch.tensor([[1., 0.], [0., -1.]], dtype=torch.cfloat)

    @property
    def h(self):
        return torch.tensor([[1. / np.sqrt(2), 1. / np.sqrt(2)],
                             [1. / np.sqrt(2), -1. / np.sqrt(2)]], dtype=torch.cfloat)

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
        return torch.tensor([[1, 0.], [0., np.exp(1.j * rad)]], dtype=torch.cfloat)

    def phase_dg(self, deg):
        return self.phase(-deg)

    @property
    def i(self):
        return torch.eye(2)

    @property
    def subspace_0(self):
        return torch.kron(dirac.ket('0').conj().T, dirac.ket('0'))

    @property
    def subspace_1(self):
        return torch.kron(dirac.ket('1').conj().T, dirac.ket('1'))


gate = GateType()
