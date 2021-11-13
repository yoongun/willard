from abc import ABCMeta
from willard.type import qselected


class subscriptable(metaclass=ABCMeta):
    def __len__(self) -> int:
        return self.size

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
        global_indices = set()
        for i in indices:
            self.check_idx(i)
            global_indices.add(i + self.offset)
        return qselected(self.qr, global_indices)

    def check_idx(self, idx):
        if idx < 0 or idx >= self.size:
            raise IndexError(f'Index {idx} is out of the range')
