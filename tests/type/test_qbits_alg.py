
import numpy as np
import torch
import pytest
from willard.const import gate
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
    q = qr.bits('000')
    q.h()
    q.flip(1)

    got = q.global_state.angle()[1]
    want = pytest.approx(np.pi)
    assert(got == want)

    q.flip(3)
    got = q.global_state.angle()[3]
    want = pytest.approx(np.pi)
    assert(got == want)

    q.flip(7)
    got = q.global_state.angle()[7]
    want = pytest.approx(np.pi)
    assert(got == want)


def test_amplitude_amplification():
    # Prepare
    qr = qreg(3)
    q = qr.bits('000')
    q.h()
    q.flip(1)

    # Amplitude Amplification
    q.aa()
    got = q.global_state[1].abs().square()
    want = 0.7
    assert(got > want)

    got = q.global_state.angle()
    want = torch.empty(len(qr)).fill_(np.pi)
    assert(torch.isclose(got, want).all())


@pytest.fixture
def f8():
    qr = qreg(4)
    q = qr.bits('0000')
    q.h()
    q[0].phase(180)
    return q


@pytest.fixture
def f2():
    qr = qreg(4)
    q = qr.bits('0000')
    q.h()
    q[0].phase(-45)
    q[1].phase(-90)
    q[2].phase(-180)
    return q


@pytest.fixture
def square():
    qr = qreg(4)
    q = qr.bits('0000')
    q.h()
    q[1].phase(180)
    return q


def test_qft(f8, square, f2):
    f8.qft()
    got = int(f8.measure(), 2)
    want = 8
    assert(got == want)

    square.qft()
    got = int(square.measure(), 2)
    want1 = 4
    want2 = 12
    assert(got == want1 or got == want2)

    f2.qft()
    got = int(f2.measure(), 2)
    want = 2
    assert(got == want)


def test_inv_qft(f8, square, f2):
    want = f8.global_state.clone()
    f8.qft().invqft()
    got = f8.global_state
    assert(torch.equal(got, want))

    want = square.global_state.clone()
    square.qft().invqft()
    got = square.global_state
    assert(torch.allclose(got, want))

    want = f2.global_state.clone()
    f2.qft().invqft()
    got = f2.global_state
    assert(torch.allclose(got, want))


def test_qpe():
    qr = qreg(4)
    output = qr.bits('000')
    input = qr.bits('1')
    output.qpe(input, gate.t)
    got = int(output.measure(), 2) / (2 ** len(output))
    want = 1 / 8
    assert (got == want)

    qr.reset()
    input.x()
    output.qpe(input, gate.s)
    got = int(output.measure(), 2) / (2 ** len(output))
    want = 1 / 4
    assert (got == want)


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
