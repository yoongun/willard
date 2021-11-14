
import numpy as np
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
    in1[0].equal(in2[0], out[0])
    got = int(out[0].measure())
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
        in1[0].equal(in2[0], out[0])
        got &= int(out.measure())
    assert(got == want)

# def test_teleportation():
#     q = qreg(3)
#     q.x(0)
#     q.h(0).phase(idx=0, deg=45).h(0)
#     q.teleport(a=0, ch=1, b=2)
#     q.h(2).phase(deg=-45, idx=2).h(2)
#     got = q.measure(2)
#     want = 1
#     assert(got == want)

#     q = qreg(3)
#     q.x(1)
#     q.h(1).phase(idx=1, deg=45).h(1)
#     q.teleport(a=1, ch=2, b=0)
#     q.h(0).phase(deg=-45, idx=0).h(0)
#     got = q.measure(0)
#     want = 1
#     assert(got == want)


def test_teleportation():
    qr = qreg(3)
    alice = qr.bits('1')
    channel = qr.bits('0')
    bob = qr.bits('0')

    alice[:].teleport(bob[:], channel[:])
    got = int(bob[:].measure())
    want = 1

    assert(got == want)


def test_flip():
    qr = qreg(3)
    qr[:].h()
    qr[:].flip(1)
    assert(qr.state.angle()[1] == np.pi)

    qr[:].flip(3)
    assert(qr.state.angle()[3] == np.pi)

    qr[:].flip(7)
    assert(qr.state.angle()[7] == np.pi)


def test_amplitude_amplification():
    # Prepare
    qr = qreg(3)
    qr[:].h()
    qr[:].flip(1)

    # Amplitude Amplification
    qr[:].aa()
    assert(qr.state[1].abs().square() > 0.7)
    assert(all(qr.state.angle() == np.pi))
