import torch
from willard.const import gate, dirac
from willard.type import qindex


class quint(qindex):
    def __init__(self, qr, size: int, init_value: int = 0) -> None:
        self.qr = qr
        self.offset = qr.size
        self.size = size
        b = format(init_value, 'b').zfill(size)
        super(quint, self).__init__(qr, set(range(qr.size, qr.size+len(b))))
        if len(b) > size:
            raise ValueError("init_value is bigger than the size of qint.")
        qr.state = torch.kron(dirac.ket(b), qr.state)

    def __len__(self) -> int:
        return self.size

    def measure(self):
        result = ''
        for i in range(len(self)):
            result = str(self[i].measure()[0]) + result
        return int(result, 2)

    def inc(self, val=1):
        bs = format(val, 'b').zfill(len(self))
        for i, b in enumerate(bs[::-1]):
            if b == '0':
                continue
            for j in reversed(range(i, len(self))):
                self[i:j].cu(self[j], gate.x)
        return self

    def dec(self, val=1):
        bs = format(val, 'b').zfill(len(self))
        for i, b in enumerate(bs[::-1]):
            if b == '0':
                continue
            for j in range(i, len(self)):
                self[i:j].cu(self[j], gate.x)
        return self

    def add(self, other: 'quint'):
        for i in range(len(other)):
            for j in reversed(range(i, len(self))):
                self[:j].c(other[i]).cx(self[j])
        return self

    def dadd(self, other: 'quint'):
        # Draper adder
        if len(self) != len(other):
            raise AttributeError("The length of operands should be equal.")
        self.qft(swap=False)
        for i in reversed(range(len(self))):
            deg = 180.
            for j in reversed(range(i+1)):
                self[i].c(other[j]).cphase(deg)
                deg /= 2.
        self.iqft(swap=False)
        return self

    def sub(self):
        pass
