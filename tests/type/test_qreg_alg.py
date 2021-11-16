
import numpy as np
import torch
import pytest
from willard.type import qreg


def test_equal():
    """
    Testing swap test
    """
    # case 1: return 1 when input1 and input2 contains same value
    qr = qreg(3)
    in1 = qr.bits('0')
    in2 = qr.bits('0')
    out = qr.bits('0')
    in1.equal(in2, out)
    got = int(out.measure())
    want = 1
    assert(got == want)

    # case 2: return 0 with 50% chance
    # when input1 and input2 contains different value
    qr = qreg(3)
    got = 1
    want = 0
    for _ in range(100):
        qr.reset()
        in1 = qr.bits('0')
        in2 = qr.bits('1')
        out = qr.bits('0')
        in1.equal(in2, out)
        got &= int(out.measure())
    assert(got == want)


def test_teleportation():
    qr = qreg(3)
    alice = qr.bits('1')
    channel = qr.bits('0')
    bob = qr.bits('0')

    alice.teleport(bob, channel)
    got = int(bob.measure())
    want = 1

    assert(got == want)


def test_flip():
    qr = qreg(3)
    qr.h()
    qr.flip(1)

    got = qr.state.angle()[1]
    want = pytest.approx(np.pi)
    assert(got == want)

    qr.flip(3)
    got = qr.state.angle()[3]
    want = pytest.approx(np.pi)
    assert(got == want)

    qr.flip(7)
    got = qr.state.angle()[7]
    want = pytest.approx(np.pi)
    assert(got == want)


def test_amplitude_amplification():
    # Prepare
    qr = qreg(3)
    qr.h()
    qr.flip(1)

    # Amplitude Amplification
    qr.aa()
    got = qr.state[1].abs().square()
    want = 0.7
    assert(got > want)

    got = qr.state.angle()
    want = torch.empty(len(qr)).fill_(np.pi)
    assert(torch.isclose(got, want).all())


@pytest.fixture
def freq8():
    qr = qreg(4)
    q = qr.uint(4, 0)
    q.h()
    q[0].phase(180)
    return q


def test_qft(freq8):
    freq8.qft()
    got = freq8.measure()
    want = 8
    assert(got == want)


def test_qpe():
    pass


def test_grover():
    pass


def test_dj():
    pass


def test_bv():
    pass


def test_simon():
    pass


def test_superdense_coding():
    pass
