from willard.type import qreg


def qucrumb():
    return qreg(2)


# class qucrumb:
#     def __init__(self):
#         self.state = state.ket_00

#     def x(self, idx):
#         if idx == 0:
#             self.state = torch.kron(gate.i, gate.x).mm(self.state)
#             return self
#         elif idx == 1:
#             self.state = torch.kron(gate.x, gate.i).mm(self.state)
#             return self
#         raise IndexError('Index {idx} is out of the range')

#     def y(self, idx):
#         if idx == 0:
#             self.state = torch.kron(gate.i, gate.y).mm(self.state)
#             return self
#         elif idx == 1:
#             self.state = torch.kron(gate.y, gate.i).mm(self.state)
#             return self
#         raise IndexError('Index {idx} is out of the range')

#     def z(self, idx):
#         if idx == 0:
#             self.state = torch.kron(gate.i, gate.z).mm(self.state)
#             return self
#         elif idx == 1:
#             self.state = torch.kron(gate.z, gate.i).mm(self.state)
#             return self
#         raise IndexError('Index {idx} is out of the range')

#     def h(self, idx):
#         if idx == 0:
#             self.state = torch.kron(gate.i, gate.h).mm(self.state)
#             return self
#         elif idx == 1:
#             self.state = torch.kron(gate.h, gate.i).mm(self.state)
#             return self
#         raise IndexError('Index {idx} is out of the range')

#     def s(self, idx):
#         if idx == 0:
#             self.state = torch.kron(gate.i, gate.s).mm(self.state)
#             return self
#         elif idx == 1:
#             self.state = torch.kron(gate.s, gate.i).mm(self.state)
#             return self
#         raise IndexError('Index {idx} is out of the range')

#     def t(self, idx):
#         if idx == 0:
#             self.state = torch.kron(gate.i, gate.t).mm(self.state)
#             return self
#         elif idx == 1:
#             self.state = torch.kron(gate.t, gate.i).mm(self.state)
#             return self
#         raise IndexError('Index {idx} is out of the range')

#     def cnot(self, *, c, d):
#         """
#         c: index of the condition qubit
#         d: index of the destination qubit
#         """
#         subspace_0 = torch.kron(state.ket_0.conj().T, state.ket_0)
#         subspace_1 = torch.kron(state.ket_1.conj().T, state.ket_1)
#         if c == 0 and d == 1:
#             cnot_0 = torch.kron(gate.i, subspace_0)
#             cnot_1 = torch.kron(gate.x, subspace_1)
#             cnot = cnot_0 + cnot_1
#             self.state = cnot.mm(self.state)
#         elif c == 1 and d == 0:
#             cnot_0 = torch.kron(subspace_0, gate.i)
#             cnot_1 = torch.kron(subspace_1, gate.x)
#             cnot = cnot_0 + cnot_1
#             self.state = cnot.mm(self.state)
#         else:
#             raise IndexError('Index ({c},{d}) is not valid')
#         return self

#     def swap(self):
#         self.cnot(c=0, d=1).cnot(c=1, d=0).cnot(c=0, d=1)
