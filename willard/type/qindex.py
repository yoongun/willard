import numpy as np
from willard.const import gate, GateBuilder, GateType


def index_size_fixed(size):
    def decorator(f):
        def wrapper(*args):
            if len(args[0]) != size:
                raise IndexError('The size of selected indices should be 1')
            return f(*args)
        return wrapper
    return decorator


def double_indexed(f):
    def validity_checked(*args):
        if len(args[0]) != 2:
            raise IndexError('The size of selected indices should be 2')
        return f(*args)
    return validity_checked


def qbit_targeted(f):
    def validity_checked(*args):
        self = args[0]
        for a in args[1:]:
            if type(a) == 'qindex':
                if len(a) != 1:
                    raise ValueError('The size of target indices should be 1')
                elif self.qr != a.qr:
                    raise ValueError('qbits are not on the same qreg')
                elif self.global_idx_set & a.global_idx_set != set():
                    raise IndexError(
                        'selected indicies contain target indices')
        return f(*args)
    return validity_checked


class qindex:
    def __init__(self, qr, global_idx_set: set, *, init_value: str = ''):
        self.global_idx_set = global_idx_set
        self.qr = qr
        self.gb = GateBuilder(qr.size)

        if init_value:
            if len(init_value) != len(global_idx_set):
                raise ValueError(
                    "init_value does not match the size of qbits.")
            init_value_rev = init_value[::-1]
            for i, elem in enumerate(init_value_rev):
                if elem == '1':
                    self.qr[list(global_idx_set)[i]].x()

    def __len__(self) -> int:
        return len(self.global_idx_set)

    def x(self):
        gate = self.gb.i()
        for i in self.global_idx_set:
            gate = self.gb.x(i).mm(gate)
        self.qr.state = gate.mm(self.qr.state)
        return self

    def rnot(self):
        gate = self.gb.i()
        for i in self.global_idx_set:
            gate = self.gb.rnot(i).mm(gate)
        self.qr.state = gate.mm(self.qr.state)
        return self

    def y(self):
        gate = self.gb.i()
        for i in self.global_idx_set:
            gate = self.gb.y(i).mm(gate)
        self.qr.state = gate.mm(self.qr.state)
        return self

    def z(self):
        gate = self.gb.i()
        for i in self.global_idx_set:
            gate = self.gb.z(i).mm(gate)
        self.qr.state = gate.mm(self.qr.state)
        return self

    def h(self):
        gate = self.gb.i()
        for i in self.global_idx_set:
            gate = self.gb.h(i).mm(gate)
        self.qr.state = gate.mm(self.qr.state)
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
        self.qr.state = gate.mm(self.qr.state)
        return self

    def phase_dg(self, deg: int):
        return self.phase(deg=-deg)

    def measure(self) -> str:
        result = ''
        for i in self.global_idx_set:
            result += self._measure_index(i)
        return result

    def _measure_index(self, i):
        prob_0 = self.qr.state.conj().T.mm(
            self.gb.measure_0(i).mm(self.qr.state)).abs().item()
        if prob_0 >= np.random.rand():
            self.qr.state = self.gb.measure_0(i).mm(
                self.qr.state) / np.sqrt(prob_0)
            return '0'
        self.qr.state = self.gb.measure_1(i).mm(
            self.qr.state) / np.sqrt(1. - prob_0)
        return '1'

    @qbit_targeted
    def cu(self, target: 'qindex', u: GateType):
        cs = list(self.global_idx_set)
        t = list(target.global_idx_set)[0]
        self.qr.state = self.gb.ncu(cs=cs, d=t, u=u).mm(self.qr.state)
        return self

    @index_size_fixed(2)
    @qbit_targeted
    def toffoli(self, target: 'qindex'):
        c1 = list(self.global_idx_set)[0]
        c2 = list(self.global_idx_set)[1]
        t = list(target.global_idx_set)[0]
        self.qr.state = self.gb.toffoli(c1=c1, c2=c2, d=t).mm(self.qr.state)
        return self

    def cx(self, target: 'qindex'):
        """
        target: index of the target qubit
        """
        return self.cu(target, gate.x)

    def cphase(self, deg: int, target: 'qindex'):
        """
        deg: degree of phase
        target: index of the destination qubit
        """
        return self.cu(target, gate.phase(deg))

    @index_size_fixed(1)
    @qbit_targeted
    def swap(self, target: 'qindex'):
        self.cx(target)
        target.cx(self)
        self.cx(target)
        return self

    @index_size_fixed(1)
    @qbit_targeted
    def cswap(self, target1: 'qindex', target2: 'qindex'):
        c = list(self.global_idx_set)[0]
        t1 = list(target1.global_idx_set)[0]
        t2 = list(target2.global_idx_set)[0]
        self.qr[c, t1].toffoli(target2)
        self.qr[c, t2].toffoli(target1)
        self.qr[c, t1].toffoli(target2)
        return self

    @index_size_fixed(1)
    @qbit_targeted
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
    @qbit_targeted
    def teleport(self, target: 'qindex', channel: 'qindex'):
        # Preparing payload
        self.h().phase(45).h()

        # Send
        channel.h().cx(target)
        self.cx(channel).h()
        a_result = int(self.measure())
        ch_result = int(channel.measure())

        # Resolve
        if ch_result:
            target.x()
        if a_result:
            target.phase(180)

        # Verify
        target.h().phase(-45).h()
