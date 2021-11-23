from willard.type import qbits
from willard.const import GateType


def simon(x: qbits, y: qbits, f: GateType):
    if len(x) != len(y):
        raise AttributeError(
            f"The length of x and y should be equal. Got x: {len(x)}, y: {len(y)}.")
    x.h()
    f(x, y)
    y.measure()
    x.h()
