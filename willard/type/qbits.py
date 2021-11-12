import numpy as np
from willard.const import gate, GateBuilder


class qbits:
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
            prob_0 = self.qr.state.conj().T.mm(
                self.gb.measure_0(i).mm(self.qr.state)).abs().item()
            if prob_0 >= np.random.rand():
                self.qr.state = self.gb.measure_0(i).mm(
                    self.qr.state) / np.sqrt(prob_0)
                result += '0'
            else:
                self.qr.state = self.gb.measure_1(i).mm(
                    self.qr.state) / np.sqrt(1. - prob_0)
                result += '1'
        return result

    def cu(self, target: 'qbits', u):
        self._check_qreg(target)
        self._check_index(target)
        self._check_size(target, 1)
        if len(target) != 1:
            raise ValueError('The lenght of target qbits should be 1')
        self.qr.state = self.gb.ncu(
            cs=list(self.global_idx_set), d=list(target.global_idx_set)[0], u=u).mm(self.qr.state)
        return self

    def toffoli(self, target: 'qbits'):
        self._check_qreg(target)
        self._check_index(target)
        self._check_size(target, 1)
        if len(self) != 2:
            raise IndexError('toffoli requires two control qbit')
        self.qr.state = self.gb.toffoli(
            c1=list(self.global_idx_set)[0], c2=list(self.global_idx_set)[1], d=list(target.global_idx_set)[0]).mm(self.qr.state)
        return self

    def cx(self, target: 'qbits'):
        """
        target: index of the target qubit
        """
        return self.cu(target, gate.x)

    def cphase(self, deg: int, target: 'qbits'):
        """
        d: index of the destination qubit
        """
        return self.cu(target, u=gate.phase(deg))

    def swap(self, target: 'qbits'):
        self._check_qreg(target)
        self._check_size(target, 1)
        if len(self) != 1:
            raise IndexError('swap requires one control qbit')

        self.cx(target)
        self.qr[list(target.global_idx_set)[0]].cx(self)
        return self.cx(target)

    def cswap(self, d1: 'qbits', d2: 'qbits'):
        self._check_qreg(d1)
        self._check_qreg(d2)
        self._check_size(d1, 1)
        self._check_size(d2, 1)
        if len(self) != 1:
            raise IndexError('cswap requires one control qbit')

        self.qr[list(self.global_idx_set)[0], list(
            d1.global_idx_set)[0]].toffoli(d2)
        self.qr[list(self.global_idx_set)[0], list(
            d2.global_idx_set)[0]].toffoli(d1)
        self.qr[list(self.global_idx_set)[0], list(
            d1.global_idx_set)[0]].toffoli(d2)
        return self

    def equal(self, other: 'qbits', output: 'qbits'):
        self._check_qreg(other)
        self._check_qreg(output)

        output.h()
        output.cswap(self, other)
        output.h()
        output.x()
        return self

    def teleport(self, target: 'qbits', channel: 'qbits'):
        self._check_qreg(target)
        self._check_qreg(channel)

        # Preparing payload
        self.h().phase(45).h()

        # Send
        channel.h().cx(target)
        self.cx(channel)
        self.h()
        a_result = self.measure()
        ch_result = channel.measure()

        # Resolve
        if ch_result:
            target.x()
        if a_result:
            target.phase(180)

        # Verify
        target.h().phase(-45).h()

    def _check_qreg(self, other: 'qbits'):
        if self.qr != other.qr:
            raise ValueError('qbits are not on the same qreg')

    def _check_index(self, other: 'qbits'):
        if other.global_idx_set & self.global_idx_set != set():
            raise IndexError('control qbits contain target qbit')

    def _check_size(self, other: 'qbits', size):
        if len(other) != size:
            raise ValueError(f'The size of qbits should be {size}')
