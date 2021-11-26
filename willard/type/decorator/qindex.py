import numpy as np
from willard.const import gate, GateBuilder, GateType
from functools import cached_property


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
    cls.swap = lambda self, t: self[:].swap(t[:])
    cls.cswap = lambda self, t1, t2: self[:].cswap(t1[:], t2[:])
    cls.equal = lambda self, other, output: self[:].equal(other[:], output[:])
    cls.teleport = lambda self, t, ch: self[:].teleport(t[:], ch[:])
    cls.flip = lambda self, val: self[:].flip(val)
    cls.aa = lambda self: self[:].aa()
    cls.qft = lambda self: self[:].qft()
    cls.invqft = lambda self: self[:].invqft()
    cls.qpe = lambda self, input, u: self[:].qpe(input, u)

    return cls


def subscriptable(cls):
    def __len__(self) -> int:
        return self.size

    cls.__len__ = __len__

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

    cls.__getitem__ = __getitem__

    def check_idx(self, idx):
        if idx < 0 or idx >= self.size:
            raise IndexError(f'Index {idx} is out of the range')

    cls.check_idx = check_idx
    return cls


def slice_to_range(s: slice, max_size: int):
    indices = s.indices(max_size)
    return range(indices[0], indices[1], indices[2])


def index_size_fixed(size):
    def decorator(f):
        def wrapper(*args):
            if len(args[0]) != size:
                raise IndexError('The size of selected indices should be 1')
            return f(*args)
        return wrapper
    return decorator


def target_size_fixed(size):
    def decorator(f):
        def wrapper(*args):
            self = args[0]
            for a in args[1:]:
                if type(a) == qindex:
                    if len(a) != size:
                        raise ValueError(
                            'The size of target indices should be 1')
                    elif self.qr != a.qr:
                        raise ValueError('qbits are not on the same qreg')
                    if self.global_idx_set & a.global_idx_set != set():
                        raise IndexError(
                            'selected indicies contain target indices')
                # if type(a) == qtype:
                #     if len(a) != size:
                #         raise ValueError(
                #             'The size of target indices should be 1')
                #     elif self.qr != a.qr:
                #         raise ValueError('qbits are not on the same qreg')
                #     if a is self:
                #         raise IndexError(
                #             'selected indicies contain target indices')
            return f(*args)
        return wrapper
    return decorator


class qindex:
    def __init__(self, qr, global_idx_set: set):
        self.global_idx_set = global_idx_set
        self.qr = qr
        self.gb = GateBuilder(qr.size)

    def __len__(self) -> int:
        return len(self.global_idx_set)

    def __getitem__(self, idx) -> 'qindex':
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
            if i < 0:
                i += len(self)
            self.check_idx(i)
            global_indices.add(self.global_idcs[i])
        return qindex(self.qr, global_indices)

    @property
    def global_state(self):
        return self.qr.state

    @global_state.setter
    def global_state(self, state):
        self.qr.state = state

    def check_idx(self, idx):
        if idx < 0 or idx >= len(self):
            raise IndexError(f'Index {idx} is out of the range')

    @cached_property
    def global_idcs(self):
        return sorted(list(self.global_idx_set))

    def x(self):
        gate = self.gb.i()
        for i in self.global_idx_set:
            gate = self.gb.x(i).mm(gate)
        self.global_state = gate.mm(self.global_state)
        return self

    def rnot(self):
        gate = self.gb.i()
        for i in self.global_idx_set:
            gate = self.gb.rnot(i).mm(gate)
        self.global_state = gate.mm(self.global_state)
        return self

    def y(self):
        gate = self.gb.i()
        for i in self.global_idx_set:
            gate = self.gb.y(i).mm(gate)
        self.global_state = gate.mm(self.global_state)
        return self

    def z(self):
        gate = self.gb.i()
        for i in self.global_idx_set:
            gate = self.gb.z(i).mm(gate)
        self.global_state = gate.mm(self.global_state)
        return self

    def h(self):
        gate = self.gb.i()
        for i in self.global_idx_set:
            gate = self.gb.h(i).mm(gate)
        self.global_state = gate.mm(self.global_state)
        return self

    def s(self):
        return self.phase(deg=90)

    def s_dg(self):
        return self.phase_dg(deg=90)

    def t(self):
        return self.phase(deg=45)

    def t_dg(self):
        return self.phase_dg(deg=45)

    def phase(self, deg: int):
        gate = self.gb.i()
        for i in self.global_idx_set:
            gate = self.gb.phase(deg, i).mm(gate)
        self.global_state = gate.mm(self.global_state)
        return self

    def phase_dg(self, deg: int):
        return self.phase(deg=-deg)

    def measure(self) -> str:
        result = ''
        for i in self.global_idx_set:
            result += self._measure_index(i)
        return result

    def _measure_index(self, i):
        prob_0 = self.global_state.conj().T.mm(
            self.gb.measure_0(i).mm(self.global_state)).abs().item()
        if prob_0 >= np.random.rand():
            self.global_state = self.gb.measure_0(i).mm(
                self.global_state) / np.sqrt(prob_0)
            return '0'
        self.global_state = self.gb.measure_1(i).mm(
            self.global_state) / np.sqrt(1. - prob_0)
        return '1'

    @target_size_fixed(1)
    def cu(self, target: 'qindex', u: GateType):
        cs = self.global_idcs
        t = target.global_idcs[0]
        self.global_state = self.gb.ncu(cs=cs, t=t, u=u).mm(self.global_state)
        return self

    @index_size_fixed(2)
    @target_size_fixed(1)
    def toffoli(self, target: 'qindex'):
        c1 = self.global_idcs[0]
        c2 = self.global_idcs[1]
        t = target.global_idcs[0]
        self.global_state = self.gb.toffoli(
            c1=c1, c2=c2, t=t).mm(self.global_state)
        return self

    def cx(self, target: 'qindex'):
        """
        target: index of the target qubit
        """
        return self.cu(target, gate.x)

    def cphase(self, deg: int):
        """
        deg: degree of phase
        target: qindex of the destination qubit
        """
        return self[:-1].cu(self[-1], gate.phase(deg))

    @index_size_fixed(2)
    def swap(self):
        self[0].cx(self[1])
        self[1].cx(self[0])
        self[0].cx(self[1])
        return self

    @index_size_fixed(1)
    @target_size_fixed(1)
    def cswap(self, target1: 'qindex', target2: 'qindex'):
        c = self.global_idcs[0]
        t1 = target1.global_idcs[0]
        t2 = target2.global_idcs[0]
        self.global_state = self.gb.cswap(
            c=c, d1=t1, d2=t2).mm(self.global_state)
        return self

    @index_size_fixed(1)
    @target_size_fixed(1)
    def equal(self, other: 'qindex', output: 'qindex'):
        """
        swap_test algorithm
        0 if input1 != input2
        1 if input1 == input2
        1 or 0 when input1 and input2 resembles
        """
        output.h()
        output.cswap(self, other)
        output.h()
        output.x()
        return self

    @index_size_fixed(1)
    @target_size_fixed(1)
    def teleport(self, target: 'qindex', channel: 'qindex'):
        # Entangle
        channel.h().cx(target)

        # Preparing payload
        self.h().phase(45).h()

        # Send
        self.cx(channel).h()
        a_result = int(self.measure())
        ch_result = int(channel.measure())

        # Receive
        if ch_result:
            target.x()
        if a_result:
            target.phase(180)

        # Verify
        target.h().phase(-45).h()

    def flip(self, val):
        if val < 0:
            raise ValueError("cannot flip value smaller than 0.")
        val_bin = bin(val).replace("0b", "").zfill(len(self))
        if len(val_bin) > len(self):
            raise ValueError(
                f"qindex object cannot contain given value val={val}.")
        val_bin_rev = val_bin[::-1]
        index_to_flip = []
        for i, val in enumerate(val_bin_rev):
            if val == '1':
                continue
            index_to_flip.append(i)
        self[index_to_flip].x()
        self.cphase(180)
        self[index_to_flip].x()

    def aa(self):
        self.h()
        self.x()
        self.cphase(180)
        self.x()
        self.h()
        return self

    def qft(self):
        for i in reversed(range(len(self))):
            self[i].h()
            deg = 90.
            for j in reversed(range(i)):
                self[i, j].cphase(deg)
                deg /= 2.
            # for j in range(i):
            #     self[i, j].cphase(180. / 2 ** (i - j))
        for i in range(len(self) // 2):
            self[i, len(self) - 1 - i].swap()
        return self

    def invqft(self):
        for i in range(len(self) // 2):
            self[i, len(self) - 1 - i].swap()
        for i in range(len(self)):
            self[i].h()
            deg = -90.
            for j in range(i + 1, len(self)):
                self[i, j].cphase(deg)
                deg /= 2.
        return self

    @target_size_fixed(1)
    def qpe(self, input: 'qindex', u: GateType):
        self.h()
        for i in range(len(self)):
            for _ in range(2 ** i):
                self[i].cu(input[0], u)
        self.invqft()
        return self
