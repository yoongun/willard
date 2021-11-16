from willard.type import qindex


def subscriptable(cls):
    def check_idx(self, idx):
        if idx < 0 or idx >= self.size:
            raise IndexError(f'Index {idx} is out of the range')

    def __len__(self) -> int:
        return self.size

    cls.__len__ = __len__

    def __getitem__(self, idx):
        def ifnone(a, b): return b if a is None else a

        indices = set()
        if type(idx) == int:
            indices.add(idx)
        elif type(idx) == slice:
            indices |= set(range(
                ifnone(idx.start, 0),
                ifnone(idx.stop, len(self)),
                ifnone(idx.step, 1)))
        elif type(idx) == tuple or type(idx) == list:
            for i in idx:
                if type(i) != int:
                    raise IndexError('Indices should be integer value.')
                indices.add(i)

        global_indices = set()
        for i in indices:
            self.check_idx(i)
            global_indices.add(i + self.offset)
        return qindex(self.qr, global_indices)

    cls.__getitem__ = __getitem__

    cls.x = lambda self: self[:].x()
    cls.rnot = lambda self: self[:].rnot()
    cls.y = lambda self: self[:].y()
    cls.z = lambda self: self[:].z()
    cls.h = lambda self: self[:].h()
    cls.s = lambda self: self[:].s()
    cls.s_dg = lambda self: self[:].s_dg()
    cls.t = lambda self: self[:].t()
    cls.t_dg = lambda self: self[:].t_dg()
    cls.phase = lambda self, deg: self[:].phase(deg)
    cls.phase_dg = lambda self, deg: self[:].phase_dg(deg)
    cls.measure = lambda self: self[:].measure()
    cls.cu = lambda self, t, u: self[:].cu(t[:], u)
    cls.toffoli = lambda self, t: self[:].toffoli(t[:])
    cls.cx = lambda self, t: self[:].cx(t[:])
    cls.cphase = lambda self, deg: self[:].cphase(deg)
    cls.swap = lambda self, t: self[:].swap(t[:])
    cls.cswap = lambda self, t1, t2: self[:].cswap(t1[:], t2[:])
    cls.equal = lambda self, other, output: self[:].equal(other[:], output[:])
    cls.teleport = lambda self, t, ch: self[:].teleport(t[:], ch[:])
    cls.flip = lambda self, val: self[:].flip(val)
    cls.aa = lambda self: self[:].aa()

    cls.check_idx = check_idx
    return cls
