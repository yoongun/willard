from abc import ABCMeta, abstractmethod
from willard.type import qindex
from willard.util import slice_to_range


def default_as_select_all(cls):
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
    cls.swap = lambda self, t: self[:].swap()
    cls.cswap = lambda self, t1, t2: self[:].cswap(t1[:], t2[:])
    cls.equal = lambda self, other, output: self[:].equal(other[:], output[:])
    cls.teleport = lambda self, t, ch: self[:].teleport(t[:], ch[:])
    cls.flip = lambda self, val: self[:].flip(val)
    cls.aa = lambda self: self[:].aa()
    cls.qft = lambda self, swap=True: self[:].qft(swap)
    cls.iqft = lambda self, swap=True: self[:].iqft(swap)
    cls.qpe = lambda self, input, u: self[:].qpe(input, u)
    return cls


@default_as_select_all
class qtype(metaclass=ABCMeta):
    def __len__(self) -> int:
        return self.size

    def __getitem__(self, idx):
        indices = set()
        if type(idx) == int:
            indices.add(idx)
        elif type(idx) == slice:
            indices |= set(slice_to_range(idx, len(self)))
        elif type(idx) == tuple or type(idx) == list:
            for i in idx:
                if type(i) != int:
                    raise IndexError('Indices should be an integer value.')
                indices.add(i)

        global_indices = set()
        for i in indices:
            self.check_idx(i)
            global_indices.add(i + self.offset)
        return qindex(self.qr, global_indices)

    def check_idx(self, idx):
        if idx < 0 or idx >= self.size:
            raise IndexError(f'Index {idx} is out of the range')

    @abstractmethod
    def measure(self):
        raise NotImplementedError(
            "qtype class should implement measure method.")

    @property
    def global_state(self):
        return self.qr.state
