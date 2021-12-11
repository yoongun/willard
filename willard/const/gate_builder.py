from willard.const import gate, GateType
import torch


class GateBuilder:
    def __init__(self, num_bits: int) -> None:
        self.dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.num_bits = num_bits

    def x(self, idx):
        result = torch.tensor([[1]], dtype=torch.cfloat).to(self.dev)
        for i in range(self.num_bits):
            if i == idx:
                result = torch.kron(gate.x, result)
            else:
                result = torch.kron(gate.i, result)
        return result

    def rnot(self, idx):
        result = torch.tensor([[1]], dtype=torch.cfloat).to(self.dev)
        for i in range(self.num_bits):
            if i == idx:
                result = torch.kron(gate.rnot, result)
            else:
                result = torch.kron(gate.i, result)
        return result

    def y(self, idx):
        result = torch.tensor([[1]], dtype=torch.cfloat).to(self.dev)
        for i in range(self.num_bits):
            if i == idx:
                result = torch.kron(gate.y, result)
            else:
                result = torch.kron(gate.i, result)
        return result

    def z(self, idx):
        result = torch.tensor([[1]], dtype=torch.cfloat).to(self.dev)
        for i in range(self.num_bits):
            if i == idx:
                result = torch.kron(gate.z, result)
            else:
                result = torch.kron(gate.i, result)
        return result

    def h(self, idx):
        result = torch.tensor([[1]], dtype=torch.cfloat).to(self.dev)
        for i in range(self.num_bits):
            if i == idx:
                result = torch.kron(gate.h, result)
            else:
                result = torch.kron(gate.i, result)
        return result

    def s(self, idx):
        result = torch.tensor([[1]], dtype=torch.cfloat).to(self.dev)
        for i in range(self.num_bits):
            if i == idx:
                result = torch.kron(gate.s, result)
            else:
                result = torch.kron(gate.i, result)
        return result

    def t(self, idx):
        result = torch.tensor([[1]], dtype=torch.cfloat).to(self.dev)
        for i in range(self.num_bits):
            if i == idx:
                result = torch.kron(gate.t, result)
            else:
                result = torch.kron(gate.i, result)
        return result

    def phase(self, deg, idx):
        result = torch.tensor([[1]], dtype=torch.cfloat).to(self.dev)
        for i in range(self.num_bits):
            if i == idx:
                result = torch.kron(gate.phase(deg), result)
            else:
                result = torch.kron(gate.i, result)
        return result

    def m0(self, idx):
        result = torch.tensor([[1]], dtype=torch.cfloat).to(self.dev)
        for i in range(self.num_bits):
            if i == idx:
                result = torch.kron(gate.m0, result)
            else:
                result = torch.kron(gate.i, result)
        return result

    def m1(self, idx):
        result = torch.tensor([[1]], dtype=torch.cfloat).to(self.dev)
        for i in range(self.num_bits):
            if i == idx:
                result = torch.kron(gate.m1, result)
            else:
                result = torch.kron(gate.i, result)
        return result

    def i(self):
        result = torch.tensor([[1]], dtype=torch.cfloat).to(self.dev)
        for _ in range(self.num_bits):
            result = torch.kron(gate.i, result)
        return result

    def cu(self, *, c, t, u: GateType):
        """
        c: index of the condition qubit
        t: index of the target qubit
        u: gate to apply on destination qubit
        """
        self._check_idx(c)
        self._check_idx(t)
        if c == t:
            raise IndexError(f'Index ({c},{t}) is not valid')
        cu_0 = torch.tensor([[1]]).to(self.dev)
        cu_1 = torch.tensor([[1]]).to(self.dev)
        for i in range(self.num_bits):
            if i == c:
                cu_0 = torch.kron(gate.m0, cu_0)
                cu_1 = torch.kron(gate.m1, cu_1)
            elif i == t:
                cu_0 = torch.kron(gate.i, cu_0)
                cu_1 = torch.kron(u, cu_1)
            else:
                cu_0 = torch.kron(gate.i, cu_0)
                cu_1 = torch.kron(gate.i, cu_1)
        return cu_0 + cu_1

    def ncu(self, cs: list, t: int, u: GateType):
        """
        cs: list of index of control qubits
        d: index of destination qubit
        u: gate to apply on destination qubit
        """
        for c in cs:
            self._check_idx(c)
        self._check_idx(t)
        if len(cs) + 1 > len([*cs, t]):
            raise IndexError(f'Index ({cs},{t}) is not valid')

        submatrices = []
        for _ in range(2 ** len(cs)):
            submatrices.append(torch.tensor(
                [[1]], dtype=torch.cfloat).to(self.dev))
        values = set(range(2 ** len(cs)))

        for i in range(self.num_bits):
            if i in cs:
                targets = set([x | 2 ** cs.index(i) for x in values])
                nontargets = values - targets
                for target in targets:
                    submatrices[target] = torch.kron(
                        gate.m1, submatrices[target])
                for nt in nontargets:
                    submatrices[nt] = torch.kron(
                        gate.m0, submatrices[nt])
            elif i == t:
                submatrices[-1] = torch.kron(u, submatrices[-1])
                for j in range(2 ** len(cs) - 1):
                    submatrices[j] = torch.kron(gate.i, submatrices[j])
            else:
                for j in range(2 ** len(cs)):
                    submatrices[j] = torch.kron(gate.i, submatrices[j])
        return sum(submatrices)

    def cnot(self, *, c, d):
        """
        c: index of the condition qubit
        d: index of the destination qubit
        """
        return self.cu(c=c, t=d, u=gate.x)

    def swap(self, *, d1, d2):
        return self.cnot(c=d1, d=d2).mm(self.cnot(c=d1, d=d2)).mm(self.cnot(c=d1, d=d2))

    def toffoli(self, *, c1, c2, t):
        return self.ncu([c1, c2], t, gate.x)
        # self._check_idx(c1)
        # self._check_idx(c2)
        # self._check_idx(d)
        # if 3 > len(set([c1, c2, d])):
        #     raise IndexError(f'Index ({c1},{c2},{d}) is not valid')
        # t00 = [[1]]
        # t01 = [[1]]
        # t10 = [[1]]
        # t11 = [[1]]
        # for i in range(self.num_bits):
        #     if i == c1:
        #         t00 = torch.kron(gate.subspace_0, t00)
        #         t01 = torch.kron(gate.subspace_1, t01)
        #         t10 = torch.kron(gate.subspace_0, t10)
        #         t11 = torch.kron(gate.subspace_1, t11)
        #     elif i == c2:
        #         t00 = torch.kron(gate.subspace_0, t00)
        #         t01 = torch.kron(gate.subspace_0, t01)
        #         t10 = torch.kron(gate.subspace_1, t10)
        #         t11 = torch.kron(gate.subspace_1, t11)
        #     elif i == d:
        #         t00 = torch.kron(gate.i, t00)
        #         t01 = torch.kron(gate.i, t01)
        #         t10 = torch.kron(gate.i, t10)
        #         t11 = torch.kron(gate.x, t11)
        #     else:
        #         t00 = torch.kron(gate.i, t00)
        #         t01 = torch.kron(gate.i, t01)
        #         t10 = torch.kron(gate.i, t10)
        #         t11 = torch.kron(gate.i, t11)
        # return t00 + t01 + t10 + t11

    def cswap(self, *, c, d1, d2):
        return self.toffoli(c1=c, c2=d1, t=d2).mm(self.toffoli(c1=c, c2=d2, t=d1)).mm(self.toffoli(c1=c, c2=d1, t=d2))

    def _check_idx(self, idx):
        if idx < 0 or idx >= self.num_bits:
            raise IndexError(f'Index {idx} is out of the range')
