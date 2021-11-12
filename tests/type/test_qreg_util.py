import pytest
import torch
import numpy as np
from willard.type import qreg
from willard.const import dirac


def test_init_qreg():
    got = qreg(1).state
    want = dirac.ket('0')
    assert(torch.equal(got, want))

    got = qreg(2).state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    with pytest.raises(ValueError):
        qreg(0)

    with pytest.raises(ValueError):
        qreg(-1)


def test_reset():
    q = qreg(2)
    q[0].x()
    q[1].x()
    q.reset()
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))


def test_len():
    q = qreg(3)
    got = len(q)
    want = 3
    assert(got == want)

    q = qreg(5)
    got = len(q)
    want = 5
    assert(got == want)

    q = qreg(1)
    got = len(q)
    want = 1
    assert(got == want)


def test_equal():
    # case 1: return 1 when input1 and input2 contains same value
    qr = qreg(3)
    input1 = qr.uint(1, 0)
    input2 = qr.uint(1, 0)
    output = qr.uint(1, 0)
    input1.equal(input2, output)
    got = output[0].measure()
    want = 1
    assert(got == want)

    # case 2: return 0 with 50% chance
    # when input1 and input2 contains different value
    qr = qreg(3)
    got = 1
    want = 0
    for _ in range(100):
        qr.reset()
        input1 = qr.uint(1, 0)
        input2 = qr.uint(1, 1)
        output = qr.uint(1, 0)
        input1.equal(input2, output)
        got &= output[0].measure()
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
    want = 1

    qr = qreg(3)
    alice = qr.uint(1, want)
    channel = qr.uint(1, 0)
    bob = qr.uint(1, 0)

    alice.teleport(bob, channel)
    got = bob[0].measure()

    assert(got == want)
