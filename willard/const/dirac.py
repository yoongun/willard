import torch


class DiracType:
    def bra(self, bits: str):
        return self.ket(bits).conj().T

    def ket(self, bits: str):
        dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        state = torch.tensor([[1.]], dtype=torch.cfloat).to(dev)
        for b in bits:
            if b == '0':
                state = torch.kron(state, torch.tensor(
                    [[1.], [0.]], dtype=torch.cfloat).to(dev))
            elif b == '1':
                state = torch.kron(state, torch.tensor(
                    [[0.], [1.]], dtype=torch.cfloat).to(dev))
            else:
                raise ValueError(
                    f"Bit array should contain either '0' or '1', but {b} has found")
        return state


dirac = DiracType()
