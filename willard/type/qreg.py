from willard.const import dirac
from willard.type import quint, qbits


class qreg:
    def __init__(self, size) -> None:
        if size < 1:
            raise ValueError(
                f"size should be bigger than 0. Got {size}")
        self.size = size
        self.state = dirac.ket('0' * size)
        self.cursor = 0

    def __getitem__(self, idx):
        indices = set()
        if type(idx) == int:
            indices.add(idx)
        elif type(idx) == slice:
            indices |= set(range(idx.start, idx.stop, idx.step))
        elif type(idx) == tuple or type(idx) == list:
            for i in idx:
                if type(i) == slice:
                    indices |= set(range(idx.start, idx.stop, idx.step))
                elif type(i) == int:
                    indices.add(i)
        for i in indices:
            self._check_idx(i)
        return qbits(self, indices)

    def __len__(self) -> int:
        return self.size

    def uint(self, size, init_value) -> quint:
        q = quint(self, size, self.cursor, init_value)
        self._check_overflow(size)
        return q

    def bits(self) -> qbits:
        q = qbits(self, set([self.cursor]))
        self._check_overflow(1)
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
            self.cursor += 1

    def _check_idx(self, idx: int):
        if idx < 0 or idx >= self.size:
            raise IndexError(f'Index {idx} is out of the range')
