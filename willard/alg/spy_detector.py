from willard.type import qreg


def _alice(q):
    a1 = int(qreg(1).bits('0').h().measure())
    a2 = int(qreg(1).bits('0').h().measure())
    if a1:
        q.x()
    if a2:
        q.h()
    return q, a1, a2


def _bob(q):
    b2 = int(qreg(1).bits('0').h().measure())
    if b2:
        q.h()
    b1 = int(q.measure())
    return b1, b2


def detect_spy(might_spy):
    # This test could fail with probability 1/2^{100}
    is_spy = False

    for _ in range(100):
        q = qreg(1).bits('0')
        q, a1, a2 = _alice(q)
        q = might_spy(q)
        b1, b2 = _bob(q)
        if b2 == a2:
            is_spy |= a1 != b1
    return is_spy
