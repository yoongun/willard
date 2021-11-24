import pytest
from willard import alg
from willard.type import qreg


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


def test_teleportation():
    qr = qreg(3)
    alice = qr.bits('1')
    channel = qr.bits('0')
    bob = qr.bits('0')

    alice.teleport(bob, channel)
    got = int(bob.measure())
    want = 1

    assert(got == want)


def test_superdense_coding():
    pass
