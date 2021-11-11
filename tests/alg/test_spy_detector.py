import pytest
from willard.alg.spy_detector import detect_spy


def test_spy_detector():
    def spy(q):
        from willard.type import qreg
        q[0].h().measure()
        q = qreg(1)
        q[0].x().h()
        return q
    assert(detect_spy(spy))

    def no_spy(q):
        return q
    assert(not detect_spy(no_spy))
