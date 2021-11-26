import numpy as np
import torch
import pytest
from willard.const import gate
from willard.type import qreg


@pytest.fixture
def dev():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def test_equal():
    """
    Testing swap test
    """
    # case 1: return 1 when input1 and input2 contains same value
    qr = qreg()
    in1 = qr.bits(1)
    in2 = qr.bits(1)
    out = qr.bits(1)
    in1.equal(in2, out)
    got = int(out.measure())
    wanted = 1
    assert(got == wanted)

    # case 2: return 0 with 50% chance
    # when input1 and input2 contains different value
    qr = qreg()
    got = 1
    wanted = 0
    for _ in range(100):
        qr.reset()
        in1 = qr.bits(1)
        in2 = qr.bits(1, '1')
        out = qr.bits(1)
        in1.equal(in2, out)
        got &= int(out.measure())
    assert(got == wanted)


def test_flip():
    qr = qreg()
    q = qr.bits(3)
    q.h()
    q.flip(1)

    got = q.global_state.angle()[1].cpu()
    wanted = pytest.approx(np.pi)
    assert(got == wanted)

    q.flip(3)
    got = q.global_state.angle()[3].cpu()
    wanted = pytest.approx(np.pi)
    assert(got == wanted)

    q.flip(7)
    got = q.global_state.angle()[7].cpu()
    wanted = pytest.approx(np.pi)
    assert(got == wanted)


def test_amplitude_amplification(dev):
    # Prepare
    qr = qreg()
    q = qr.bits(3)
    q.h()
    q.flip(1)

    # Amplitude Amplification
    q.aa()
    got = q.global_state[1].abs().square()
    wanted = 0.7
    assert(got > wanted)

    got = q.global_state.angle()
    wanted = torch.empty(len(qr)).fill_(np.pi).to(dev)
    assert(torch.isclose(got, wanted).all())


@pytest.fixture
def f8():
    qr = qreg()
    q = qr.bits(4)
    q.h()
    q[0].phase(180)
    return q


@pytest.fixture
def f2():
    qr = qreg()
    q = qr.bits(4)
    q.h()
    q[0].phase(-45)
    q[1].phase(-90)
    q[2].phase(-180)
    return q


@pytest.fixture
def square():
    qr = qreg()
    q = qr.bits(4)
    q.h()
    q[1].phase(180)
    return q


def test_qft(f8, square, f2):
    f8.qft()
    got = int(f8.measure(), 2)
    wanted = 8
    assert(got == wanted)

    square.qft()
    got = int(square.measure(), 2)
    want1 = 4
    want2 = 12
    assert(got == want1 or got == want2)

    f2.qft()
    got = int(f2.measure(), 2)
    wanted = 2
    assert(got == wanted)


def test_inv_qft(f8, square, f2):
    wanted = f8.global_state.clone()
    f8.qft().invqft()
    got = f8.global_state
    assert(torch.equal(got, wanted))

    wanted = square.global_state.clone()
    square.qft().invqft()
    got = square.global_state
    assert(torch.allclose(got, wanted))

    wanted = f2.global_state.clone()
    f2.qft().invqft()
    got = f2.global_state
    assert(torch.allclose(got, wanted))


def test_qpe():
    qr = qreg()
    output = qr.bits(3)
    input = qr.bits(1, '1')
    output.qpe(input, gate.t)
    got = int(output.measure(), 2) / (2 ** len(output))
    wanted = 1 / 8
    assert (got == wanted)

    qr.reset()
    output = qr.bits(3)
    input = qr.bits(1, '1')
    output.qpe(input, gate.s)
    got = int(output.measure(), 2) / (2 ** len(output))
    wanted = 1 / 4
    assert (got == wanted)
