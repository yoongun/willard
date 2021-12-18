from typing import List
import torch
from willard.const import gate


class GateBuilder:
    def __init__(self, num_bits: int) -> None:
        self.dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.num_bits = num_bits

    def u(self, idx: int, u: torch.Tensor) -> torch.Tensor:
        if type(idx) != int:
            raise IndexError("Index value should be an integer value.")
        if idx < 0 or idx >= self.num_bits:
            raise IndexError(f"Index out of range: {idx}")
        g = torch.tensor([[1.]], dtype=torch.cfloat).to(self.dev)
        for i in range(self.num_bits):
            if i == idx:
                g = torch.kron(u, g)
            else:
                g = torch.kron(gate.i, g)
        return g

    def i(self) -> torch.Tensor:
        return self.u(0, gate.i)

    def x(self, idx: int) -> torch.Tensor:
        return self.u(idx, gate.x)

    def rnot(self, idx: int) -> torch.Tensor:
        return self.u(idx, gate.rnot)

    def y(self, idx: int) -> torch.Tensor:
        return self.u(idx, gate.y)

    def z(self, idx: int) -> torch.Tensor:
        return self.u(idx, gate.z)

    def h(self, idx: int) -> torch.Tensor:
        return self.u(idx, gate.h)

    def s(self, idx: int) -> torch.Tensor:
        return self.u(idx, gate.s)

    def s_dg(self, idx: int) -> torch.Tensor:
        return self.u(idx, gate.s_dg)

    def t(self, idx: int) -> torch.Tensor:
        return self.u(idx, gate.t)

    def t_dg(self, idx: int) -> torch.Tensor:
        return self.u(idx, gate.t_dg)

    def phase(self, idx: int, deg: int) -> torch.Tensor:
        return self.u(idx, gate.phase(deg))

    def phase_dg(self, idx: int, deg: int) -> torch.Tensor:
        return self.u(idx, gate.phase_dg(deg))

    def m0(self, idx: int) -> torch.Tensor:
        return self.u(idx, gate.m0)

    def m1(self, idx: int) -> torch.Tensor:
        return self.u(idx, gate.m1)

    def cu(self, cs: List[int], u: torch.Tensor) -> torch.Tensor:
        if len(cs) == 0:
            return u
        g1 = self.m1(cs[0])
        for i in cs[1:]:
            g1 = self.m1(i).mm(g1)
        g0 = self.i() - g1
        g1 = g1.mm(u)
        g = g0 + g1
        return g

    def cx(self, c: int, t: int) -> torch.Tensor:
        return self.cu([c], self.x(t))

    def swap(self, idx1: int, idx2) -> torch.Tensor:
        g = self.cx(idx1, idx2)
        g = self.cx(idx2, idx1).mm(g)
        g = self.cx(idx1, idx2).mm(g)
        return g
