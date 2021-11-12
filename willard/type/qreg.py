from willard.const import dirac
from willard.type import quint, qbit, qbits


class qreg:
    def __init__(self, size) -> None:
        if size < 1:
            raise ValueError(
                f"size should be bigger than 0. Got {size}")
        self.size = size
        self.state = dirac.ket('0' * size)
        self._offset = 0

    def __getitem__(self, idx):
        if type(idx) == int:
            self._check_idx(idx)
            return qbit(self, idx)
        elif type(idx) == slice:
            indices = set(range(idx.start, idx.stop, idx.step))
            for i in indices:
                self._check_idx(i)
            return qbits(self, indices)
        elif type(idx) == tuple or type(idx) == list:
            indices = set()
            for i in idx:
                if type(i) == slice:
                    indices = indices | set(
                        range(idx.start, idx.stop, idx.step))
                    for i_ in indices:
                        self._check_idx(i_)
                elif type(i) == int:
                    self._check_idx(i)
                    indices.add(i)
            return qbits(self, indices)

    def __len__(self) -> int:
        return self.size

    def uint(self, size, init_value) -> quint:
        q = quint(self, size, self._offset, init_value)
        if self._offset + size > self.size:
            raise ValueError(
                "This register is already full. Please try creating another register with larger size")
        self._offset += size
        return q

    def reset(self):
        self.state = dirac.ket('0' * self.size)
        self._offset = 0
        return self

    def _check_idx(self, idx):
        if idx < 0 or idx >= self.size:
            raise IndexError(f'Index {idx} is out of the range')
