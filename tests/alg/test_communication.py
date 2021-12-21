import pytest
from willard import alg
from willard.type import qreg
from willard.network import SuperdenseChannel


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
    alice = qr.bits('1')
    channel = qr.bits(1)
    bob = qr.bits(1)

    alice.teleport(bob, channel)
    got = int(bob.measure())
    wanted = 1

    assert(got == wanted)


@pytest.mark.parametrize(
    "data",
    [(format(i, 'b').zfill(2)) for i in range(4)]
)
def test_superdense_coding(data):
    sd = SuperdenseChannel()
    q = sd.encode(data)
    got = sd.decode(q)
    wanted = data
    assert(got == wanted)
