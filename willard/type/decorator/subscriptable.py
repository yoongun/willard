from willard.type import qindex


def subscriptable(cls):
    def check_idx(self, idx):
        if idx < 0 or idx >= self.size:
            raise IndexError(f'Index {idx} is out of the range')

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
        return qindex(self.qr, global_indices)

    cls.__getitem__ = __getitem__
    cls.__len__ = __len__
    cls.check_idx = check_idx
    return cls
