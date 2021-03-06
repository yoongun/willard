from __future__ import annotations
from typing import TypeVar, overload
from functools import cached_property
import numpy as np
import torch
from willard.const import gate, GateBuilder


qreg = TypeVar("qreg")


def index_size_fixed(size):
    def decorator(f):
        def wrapper(*args):
            if len(args[0]) != size:
                raise IndexError(
                    f'The size of selected indices should be {size}')
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
                            f'The size of target indices should be {size}')
                    elif self.qr != a.qr:
                        raise ValueError('qbits are not on the same qreg')
                    if self.global_idx_set & a.global_idx_set != set():
                        raise IndexError(
                            'selected indicies contain target indices')
            return f(*args)
        return wrapper
    return decorator


class qindex:
    def __init__(self, qr: qreg, g_idcs: tuple):
        """
        :params:
        qr: qreg
        g_idcs: tuple of global indices
        """
        self.qr = qr
        self.g_idcs = g_idcs

    @overload
    def __getitem__(self, idcs: int) -> qindex:
        ...

    @overload
    def __getitem__(self, idcs: slice) -> qindex:
        ...

    def __getitem__(self, idcs: int | slice | tuple | list) -> qindex:
        idx_list = self._parse_idcs(idcs)
        g_idcs = tuple()
        for i in idx_list:
            self._check_idx(i)
            g_idcs += tuple([self.g_idcs[i]])
        return qindex(self.qr, g_idcs)

    def _check_idx(self, i: int):
        if i < 0 or i >= len(self):
            raise IndexError(f"Index out of range: {i}")

    def _parse_idcs(self, idcs: int | slice | tuple | list) -> tuple:
        idx_list = []
        if type(idcs) == int:
            if idcs < 0:
                idcs += len(self)
            idx_list.append(idcs)
        elif type(idcs) == slice:
            i = idcs.indices(len(self))
            idx_list.extend(range(i[0], i[1], i[2]))
        elif type(idcs) == tuple or type(idcs) == list:
            for i in idcs:
                if type(i) != int:
                    raise IndexError('Indices should be an integer value.')
                if i < 0:
                    i += len(self)
                idx_list.append(i)
        return sorted(idx_list)

    def __len__(self) -> int:
        return len(self.g_idcs)

    @property
    def gb(self):
        return GateBuilder(len(self.qr))

    @property
    def state(self):
        return self.qr.state

    @state.setter
    def state(self, state):
        self.qr.state = state

    @cached_property
    def global_idcs(self):
        return sorted(list(self.g_idcs))

    def c(self, other: 'qindex') -> 'qindex':
        return qindex(self.qr, self.g_idcs + other.g_idcs)

    def x(self):
        for i in self.g_idcs:
            self.state = self.gb.x(i).mm(self.state)
        return self

    def rnot(self):
        for i in self.g_idcs:
            self.state = self.gb.rnot(i).mm(self.state)
        return self

    def y(self):
        for i in self.g_idcs:
            self.state = self.gb.y(i).mm(self.state)
        return self

    def z(self):
        for i in self.g_idcs:
            self.state = self.gb.z(i).mm(self.state)
        return self

    def h(self):
        for i in self.g_idcs:
            self.state = self.gb.h(i).mm(self.state)
        return self

    def s(self):
        for i in self.g_idcs:
            self.state = self.gb.s(i).mm(self.state)
        return self

    def s_dg(self):
        for i in self.g_idcs:
            self.state = self.gb.s_dg(i).mm(self.state)
        return self

    def t(self):
        for i in self.g_idcs:
            self.state = self.gb.t(i).mm(self.state)
        return self

    def t_dg(self):
        for i in self.g_idcs:
            self.state = self.gb.t_dg(i).mm(self.state)
        return self

    def phase(self, deg: int):
        for i in self.g_idcs:
            self.state = self.gb.phase(i, deg).mm(self.state)
        return self

    def phase_dg(self, deg: int):
        for i in self.g_idcs:
            self.state = self.gb.phase_dg(i, deg).mm(self.state)
        return self

    def measure(self) -> str:
        result = ''
        for i in self.g_idcs:
            result = self._measure(i) + result
        return result

    def _measure(self, i: int) -> str:
        proj = self.gb.m0(i).mm(self.state)
        p0 = proj.conj().T.mm(proj).abs()
        if p0 > np.random.rand():
            self.state = proj / torch.sqrt(p0)
            return '0'
        self.state = self.gb.m1(i).mm(self.state) / torch.sqrt(1. - p0)
        return '1'

    def cu(self, u: torch.Tensor):
        g = self.gb.cu(self.g_idcs, u)
        self.state = g.mm(self.state)
        return self

    def cx(self, target: 'qindex'):
        if self.g_idcs == target.g_idcs:
            raise IndexError(
                f"The index of control and target qubits should be different. Given {self.g_idcs}, {target.g_idcs}.")
        u = self.gb.x(target.g_idcs[0])
        self.cu(u)
        return self

    def cphase(self, deg: int):
        u = self.gb.phase(self.g_idcs[-1], deg)
        self[:-1].cu(u)
        return self

    def swap(self):
        self[0].cx(self[1])
        self[1].cx(self[0])
        self[0].cx(self[1])
        return self

    def toffoli(self, target: 'qindex'):
        if len(set(self.g_idcs + target.g_idcs)) != 3:
            raise IndexError("Control qubits contains target qubit.")
        if len(self) != 2 or len(target) != 1:
            raise IndexError(
                f"The length of control and target qubits should be 2 and 1 each. Given {len(self)}, {len(target)}")
        u = self.gb.x(target.g_idcs[0])
        self.cu(u)
        return self

    def cswap(self, t1: 'qindex', t2: 'qindex'):
        u = self.gb.swap(t1.g_idcs[0], t2.g_idcs[0])
        self.cu(u)
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

        return self

    def flip(self, val):
        if val < 0:
            raise ValueError("cannot flip value smaller than 0.")
        val_bin = bin(val).replace("0b", "").zfill(len(self))
        if len(val_bin) > len(self):
            raise ValueError(
                f"qindex object cannot contain given value val={val}.")
        val_bin_rev = val_bin[::-1]
        idcs_to_flip = []
        for i, val in enumerate(val_bin_rev):
            if val == '1':
                continue
            idcs_to_flip.append(i)
        self[idcs_to_flip].x()
        self.cphase(180)
        self[idcs_to_flip].x()
        return self

    def aa(self):
        self.h()
        self.x()
        self.cphase(180)
        self.x()
        self.h()
        return self

    def qft(self, swap=True):
        for i in reversed(range(len(self))):
            self[i].h()
            for j in range(i):
                self[i, j].cphase(180. / 2 ** (i - j))
        if swap:
            for i in range(len(self) // 2):
                self[i, len(self) - 1 - i].swap()
        return self

    def iqft(self, swap=True):
        if swap:
            for i in range(len(self) // 2):
                self[i, len(self) - 1 - i].swap()
        for i in range(len(self)):
            self[i].h()
            for j in range(i + 1, len(self)):
                self[i, j].cphase(-180. / 2 ** (j - i))
        return self

    @target_size_fixed(1)
    def qpe(self, input: 'qindex', u: torch.Tensor):
        u = self.gb.u(input.g_idcs[0], u)

        self.h()
        for i in range(len(self)):
            for _ in range(2 ** i):
                self[i].cu(u)
        self.iqft()
        return self
