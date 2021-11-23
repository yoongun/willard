from willard.type import qbits


def deutsch(x: qbits, y: qbits, f):
    if len(x) != 1 or len(y) != 1:
        raise AttributeError(
            f"Length of x and y should be 1. Given x: {len(x)}, y: {len(y)}")
    x.h()
    y.x().h()
    f(x, y)
    x.h()
    return bool(int(x.measure(), 2))
