import torch
from willard.type import quint, qbits


class qreg:
    def __init__(self) -> None:
        self.size = 0
        self.qr = self

        dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.state = torch.tensor([[1.]], dtype=torch.cfloat).to(dev)
        self.objs = []

    def __len__(self) -> int:
        return self.size

    def uint(self, size: int, init_value: int = None) -> quint:
        if init_value is None:
            init_value = 0
        q = quint(self, size, init_value)
        self.size += size
        self.objs.append(q)
        return q

    def bits(self, size: int, init_value: str = None) -> qbits:
        if init_value is None:
            init_value = '0' * size
        elif len(init_value) != size:
            raise AttributeError(
                f"size {size} does not match the length of init_value {init_value}.")
        q = qbits(self, init_value)
        self.size += len(init_value)
        self.objs.append(q)
        return q

    def reset(self):
        self.size = 0
        dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.state = torch.tensor([[1.]], dtype=torch.cfloat).to(dev)
        for o in self.objs:
            o.qr = None
        self.objs = []
        return self
