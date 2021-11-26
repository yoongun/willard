import torch


class DiracType:
    def ket(self, bit_array: str):
        dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        state = torch.tensor([[1.]], dtype=torch.cfloat).to(dev)
        for bit in bit_array:
            if bit == '0':
                state = torch.kron(state, torch.tensor(
                    [[1.], [0.]], dtype=torch.cfloat).to(dev))
            elif bit == '1':
                state = torch.kron(state, torch.tensor(
                    [[0.], [1.]], dtype=torch.cfloat).to(dev))
            else:
                raise ValueError(
                    f"bit_array should contain either '0' or '1', but {bit} has found")
        return state


dirac = DiracType()
