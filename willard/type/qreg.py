from willard.const import dirac
from willard.type import quint, qselected, qbits
from willard.type.interface import subscriptable


class qreg(subscriptable):
    def __init__(self, size) -> None:
        super(qreg, self).__init__()
        if size < 1:
            raise ValueError(f"size should be bigger than 0. Got {size}")
        self.size = size
        self.offset = 0
        self.qr = self

        self.state = dirac.ket('0' * size)
        self.cursor = 0

    def uint(self, size, init_value) -> quint:
        q = quint(self, size, self.cursor, init_value)
        self._check_overflow(size)
        return q

    def bits(self, init_value: str) -> qselected:
        q = qbits(self, self.cursor, init_value)
        self._check_overflow(len(init_value))
        return q

    def reset(self):
        self.state = dirac.ket('0' * self.size)
        self.cursor = 0
        return self

    def _check_overflow(self, size: int):
        if self.cursor + size > self.size:
            raise ValueError(
                "This register is already full. Please try creating another register with larger size")
        else:
            self.cursor += size
