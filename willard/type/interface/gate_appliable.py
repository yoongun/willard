from willard.const import GateBuilder
from abc import ABCMeta


class gate_appliable(metaclass=ABCMeta):
    def __init__(self, qr, global_idx_set: set):
        self.global_idx_set = global_idx_set
        self.gb = GateBuilder(qr.size)

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
