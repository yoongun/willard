import pytest
from willard import alg
from willard.type import qreg


def test_spy_detector():
    def spy(q):
        from willard.type import qreg
        q.h().measure()
        q = qreg().bits(1)
        q.x().h()
        return q
    assert(alg.detect_spy(spy))

    def no_spy(q):
        return q
    assert(not alg.detect_spy(no_spy))


def test_teleportation():
    qr = qreg()
    alice = qr.bits(1, '1')
    channel = qr.bits(1)
    bob = qr.bits(1)

    alice.teleport(bob, channel)
    got = int(bob.measure())
    wanted = 1

    assert(got == wanted)


def test_superdense_coding():
    pass
