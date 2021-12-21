from willard.type import qreg, qbits


class SuperdenseChannel:
    def __init__(self) -> None:
        self.qr = qreg()
        self.a = self.qr.bits(1)
        self.b = self.qr.bits(1)

    def encode(self, bits: str) -> qbits:
        self.a.h().cx(self.b)
        if bits[0] == '1':
            self.b.z()
        if bits[1] == '1':
            self.b.x()
        return self.b

    def decode(self, qbit: qbits) -> str:
        self.a.cx(self.b).h()
        f = self.a.measure()
        s = self.b.measure()
        result = f + s
        return result
