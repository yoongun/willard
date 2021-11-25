import torch
from willard.const import gate, dirac
from willard.type import qtype


class quint(qtype):
    def __init__(self, qr, size: int, init_value: int) -> None:
        super(quint, self).__init__()
        self.qr = qr
        self.offset = qr.size
        self.size = size
        b = format(init_value, 'b').zfill(size)
        if len(b) > size:
            raise ValueError("init_value is bigger than the size of qint.")
        qr.state = torch.kron(dirac.ket(b), qr.state)

    def measure(self):
        result = ''
        for i in range(self.size):
            result = str(self[i].measure()[0]) + result
        return int(result, 2)

    def inc(self, val=1):
        bs = format(val, 'b').zfill(self.size)
        for i, b in enumerate(bs[::-1]):
            if b == '0':
                continue
            for j in reversed(range(i, self.size)):
                self[i:j].cu(self[j], gate.x)
        return self

    def dec(self, val=1):
        bs = format(val, 'b').zfill(self.size)
        for i, b in enumerate(bs[::-1]):
            if b == '0':
                continue
            for j in range(i, self.size):
                self[i:j].cu(self[j], gate.x)
        return self

    def add(self):
        pass

    def sub(self):
        pass
