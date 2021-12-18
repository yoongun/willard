import torch
from typing import TypeVar
from willard.type import qindex
from willard.const import dirac


qreg = TypeVar('qreg')


class qbits(qindex):
    def __init__(self, qr: qreg, offset: int, init_value: str):
        g_idcs = range(offset, offset + len(init_value))
        g_idcs = tuple(g_idcs)
        super(qbits, self).__init__(qr, g_idcs)
        qr.state = torch.kron(dirac.ket(init_value), qr.state)
