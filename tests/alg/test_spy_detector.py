import pytest
from willard import alg


def test_spy_detector():
    def spy(q):
        from willard.type import qreg
        q.h().measure()
        q = qreg(1).bits('0')
        q.x().h()
        return q
    assert(alg.detect_spy(spy))

    def no_spy(q):
        return q
    assert(not alg.detect_spy(no_spy))
