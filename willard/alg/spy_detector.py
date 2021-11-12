from willard.type import qreg


def _alice(q):
    a1 = qreg(1)[0].h().measure()[0]
    a2 = qreg(1)[0].h().measure()[0]
    if a1:
        q[0].x()
    if a2:
        q[0].h()
    return q, a1, a2


def _bob(q):
    b2 = qreg(1)[0].h().measure()[0]
    if b2:
        q[0].h()
    b1 = q[0].measure()[0]
    return b1, b2


def detect_spy(might_spy):
    # This test could fail with probability 1/2^{100}
    is_spy = False

    for _ in range(100):
        q = qreg(1)
        q, a1, a2 = _alice(q)
        q = might_spy(q)
        b1, b2 = _bob(q)
        if b2 == a2:
            is_spy |= a1 != b1
    return is_spy
