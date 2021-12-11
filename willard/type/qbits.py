import torch
from willard.type import qtype
from willard.const import dirac


class qbits(qtype):
    def __init__(self, qr, init_value: str):
        super(qbits, self).__init__()
        self.qr = qr
        self.offset = qr.size
        self.size = len(init_value)
        qr.state = torch.kron(dirac.ket(init_value), qr.state)

    def measure(self):
        result = ''
        for i in range(self.size):
            result = str(self[i].measure()[0]) + result
        return result

    @property
    def global_state(self):
        return super().global_state
