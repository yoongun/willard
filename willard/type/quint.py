from willard.const import gate
from willard.type.decorator import subscriptable


@subscriptable
class quint:
    def __init__(self, qr, size: int, offset: int, init_value: int) -> None:
        super(quint, self).__init__()
        self.qr = qr
        self.size = size
        self.offset = offset
        b = format(init_value, 'b')
        if len(b) > size:
            raise ValueError("init_value is bigger than the size of qint.")
        b_rev = b[::-1]
        for i, elem in enumerate(b_rev):
            if elem == '1':
                self[i].x()

    def measure(self):
        result = ''
        for i in range(self.size):
            result = str(self[i].measure()[0]) + result
        return int(result, 2)

    def inc(self):
        for i in reversed(range(self.size)):
            cs = []
            for j in reversed(range(i)):
                cs.append(j)
            self[cs].cu(self[i], gate.x)
        return self

    def dec(self):
        for i in range(self.size):
            cs = []
            for j in range(i):
                cs.append(j)
            self[cs].cu(self[i], gate.x)
        return self
