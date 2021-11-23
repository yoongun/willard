from willard.type import qbits
from willard.const import GateType


def deutsch(x: qbits, y: qbits, f):
    if len(x) != 1 or len(y) != 1:
        raise AttributeError(
            f"Length of x and y should be 1. Given x: {len(x)}, y: {len(y)}")
    x.h()
    y.x().h()
    f(x, y)
    x.h()
    return bool(int(x.measure(), 2))


def deutsch_jozsa(x: qbits, y: qbits, f):
    if len(y) != 1:
        raise AttributeError(
            f"Length of y should be 1. Given y: {len(y)}")
    x.h()
    y.x().h()
    f(x, y)
    x.h()
    return bool(int(x.measure(), 2))


def bv(x: qbits, y: qbits, f: GateType):
    """
    bernstein vazirani
    """
    x.h()
    y.h().z()
    f(x, y)
    x.h()
    return x.measure()


def simon(x: qbits, y: qbits, f: GateType):
    if len(x) != len(y):
        raise AttributeError(
            f"The length of x and y should be equal. Got x: {len(x)}, y: {len(y)}.")
    x.h()
    f(x, y)
    y.measure()
    x.h()
