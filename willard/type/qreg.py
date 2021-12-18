from __future__ import annotations
from typing import overload
import torch
from willard.type import quint, qbits


class qreg:
    def __init__(self):
        self.cursor = 0
        dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.state = torch.tensor([[1.]], dtype=torch.cfloat).to(dev)
        self.objs = []

    def __len__(self) -> int:
        return self.cursor

    @overload
    def bits(self, size: int) -> qbits:
        ...

    @overload
    def bits(self, init_value: str) -> qbits:
        ...

    def bits(self, param: int | str) -> qbits:
        init_value = ''
        if type(param) == int:
            init_value = '0' * param
        elif type(param) == str:
            init_value = param
        else:
            raise TypeError(
                f"Parameter type should be 'int' or 'str', Given {type(param)}")
        q = qbits(self, self.cursor, init_value)
        self.objs.append(q)
        self.cursor += len(init_value)
        return q

    def uint(self, size: int, init_value: int = 0) -> quint:
        q = quint(self, self.cursor, size, init_value)
        self.cursor += size
        self.objs.append(q)
        return q

    def reset(self):
        self.cursor = 0
        dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.state = torch.tensor([[1.]], dtype=torch.cfloat).to(dev)
        for o in self.objs:
            o.qr = None
        self.objs = []
        return self
