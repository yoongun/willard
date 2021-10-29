from willard.type import qreg


def qubit():
    return qreg(1)

# class qubit:
#     def __init__(self):
#         self.state = state.ket_0

#     def x(self):
#         self.state = gate.x.mm(self.state)
#         return self

#     def y(self):
#         self.state = gate.y.mm(self.state)
#         return self

#     def z(self):
#         self.state = gate.z.mm(self.state)
#         return self

#     def h(self):
#         self.state = gate.h.mm(self.state)
#         return self

#     def s(self):
#         self.phase(90)
#         return self

#     def s_dg(self):
#         self.phase(-90)
#         return self

#     def t(self):
#         self.phase(45)
#         return self

#     def t_dg(self):
#         self.phase(-45)
#         return self

#     def phase(self, deg):
#         rad = deg / 180 * torch.pi
#         phase = torch.tensor([[1, 0.], [0., torch.exp(1.j * rad)]])
#         self.state = phase.mm(self.state)
#         return self

#     def phase_dg(self, deg):
#         return self.phase(-deg)

#     def measure(self):
#         prob_0 = self.state[0] ** 2
#         if prob_0 >= torch.random.rand():
#             self.state = state.ket_0
#             return 0
#         self.state = state.ket_1
#         return 1
