import numpy as np
from willard.const import gate, GateBuilder
# from willard.type import qreg


class qbit:
    def __init__(self, qr, global_idx: int) -> None:
        self.global_idx = global_idx
        self.qr = qr
        self.gb = GateBuilder(qr.size)

    def x(self):
        self.qr.state = self.gb.x(self.global_idx).mm(self.qr.state)
        return self

    def rnot(self):
        self.qr.state = self.gb.rnot(self.global_idx).mm(self.qr.state)
        return self

    def y(self):
        self.qr.state = self.gb.y(self.global_idx).mm(self.qr.state)
        return self

    def z(self):
        self.qr.state = self.gb.z(self.global_idx).mm(self.qr.state)
        return self

    def h(self):
        self.qr.state = self.gb.h(self.global_idx).mm(self.qr.state)
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
        self.qr.state = self.gb.phase(deg, self.global_idx).mm(self.qr.state)
        return self

    def phase_dg(self, deg: int):
        return self.phase(deg=-deg)

    def measure(self):
        prob_0 = self.qr.state.conj().T.mm(self.gb.measure_0(
            self.global_idx).mm(self.qr.state)).abs().item()
        if prob_0 >= np.random.rand():
            self.qr.state = self.gb.measure_0(self.global_idx).mm(
                self.qr.state) / np.sqrt(prob_0)
            return 0
        self.qr.state = self.gb.measure_1(self.global_idx).mm(
            self.qr.state) / np.sqrt(1. - prob_0)
        return 1

    def equal(self, other: 'qbit', output: 'qbit'):
        self._check_qreg(other)
        self._check_qreg(output)
        output.h()
        output.cswap(self, other)
        output.h()
        output.x()
        return self

    def teleport(self, target: 'qbit', channel: 'qbit'):
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

    def cu(self, target: 'qbit', u):
        """
        target: index of the target qubit
        """
        self._check_qreg(target)
        if self.global_idx == target.global_idx:
            raise IndexError(
                f'Index ({self.global_idx},{target.global_idx}) is not valid')
        self.qr.state = self.gb.cu(
            c=self.global_idx, d=target.global_idx, u=u).mm(self.qr.state)
        return self

    def cx(self, target: 'qbit'):
        """
        target: index of the target qubit
        """
        return self.cu(target, gate.x)

    def cphase(self, deg: int, target: 'qbit'):
        """
        d: index of the destination qubit
        """
        return self.cu(target, u=gate.phase(deg))

    def swap(self, target: 'qbit'):
        self._check_qreg(target)
        self.cx(target)
        self.qr[target.global_idx].cx(self)
        return self.cx(target)

    def cswap(self, d1: 'qbit', d2: 'qbit'):
        self._check_qreg(d1)
        self._check_qreg(d2)
        self.qr[self.global_idx, d1.global_idx].toffoli(d2)
        self.qr[self.global_idx, d2.global_idx].toffoli(d1)
        return self.qr[self.global_idx, d1.global_idx].toffoli(d2)

    def _check_qreg(self, other: 'qbit'):
        if self.qr != other.qr:
            raise ValueError('qbits are not on the same qreg')


class qbits:
    def __init__(self, qr, global_idx_set: set) -> None:
        self.global_idx_set = global_idx_set
        self.qr = qr
        self.gb = GateBuilder(qr.size)

    def cu(self, target: qbit, u):
        self._check_qreg(target)
        self._check_index(target)
        self.qr.state = self.gb.ncu(
            cs=list(self.global_idx_set), d=target.global_idx, u=u).mm(self.qr.state)
        return self

    def toffoli(self, target: qbit):
        self._check_qreg(target)
        self._check_index(target)
        if len(self.global_idx_set) != 2:
            raise IndexError('toffoli requires two control qbit')
        self.qr.state = self.gb.toffoli(
            c1=list(self.global_idx_set)[0], c2=list(self.global_idx_set)[1], d=target.global_idx).mm(self.qr.state)
        return self

    def _check_qreg(self, other: qbit):
        if self.qr != other.qr:
            raise ValueError('qbits are not on the same qreg')

    def _check_index(self, other: qbit):
        if other.global_idx in self.global_idx_set:
            raise IndexError('control qbits contain target qbit')
