import torch
from willard.const import gate, dirac
from willard.type import qtype
from willard.type.decorator import qindex


class quint(qtype):
    def __init__(self, qr, size: int, init_value: int = 0) -> None:
        super(quint, self).__init__()
        self.qr = qr
        self.offset = qr.size
        self.size = size
        b = format(init_value, 'b').zfill(size)
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
        # # Draper adder
        # if len(self) != len(other):
        #     raise AttributeError("The length of operands should be equal.")
        # self.qft()
        # for i in reversed(range(len(other))):
        #     for j in range(i, len(self)):
        #         self[i].cu(other[j], gate.phase(360. / (2. ** j)))
        # self.invqft()

        for i in range(len(other)):
            for j in reversed(range(i, len(self))):
                self[:j].w(other[i]).cx(self[j])
        return self

    def sub(self):
        pass
