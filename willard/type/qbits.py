import torch
from willard.type import qindex
from willard.const import dirac


class qbits(qindex):
    def __init__(self, qr, init_value: str):
        super(qbits, self).__init__(
            qr, set(range(qr.size, qr.size+len(init_value))))
        self.qr = qr
        self.offset = qr.size
        self.size = len(init_value)
        qr.state = torch.kron(dirac.ket(init_value), qr.state)

    def measure(self):
        result = ''
        for i in range(self.size):
            result = str(self[i].measure()[0]) + result
        return result
