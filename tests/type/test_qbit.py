import pytest
import torch
import numpy as np
from willard.type import qreg
from willard.const import dirac

# def test_measure():
#     pytest.fail()


def test_equal():
    # case 1: return 1 when input1 and input2 contains same value
    qr = qreg(3)
    in1 = qr.bit(0)
    in2 = qr.bit(0)
    out = qr.bit(0)
    in1.equal(in2, out)
    got = out.measure()
    want = 1
    assert(got == want)

    # case 2: return 0 with 50% chance
    # when input1 and input2 contains different value
    qr = qreg(3)
    got = 1
    want = 0
    for _ in range(100):
        qr.reset()
        in1 = qr.bit(0)
        in2 = qr.bit(1)
        out = qr.bit(0)
        in1.equal(in2, out)
        got &= out.measure()
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
    alice = qr.bit(want)
    channel = qr.bit(0)
    bob = qr.bit(0)

    alice.teleport(bob, channel)
    got = bob.measure()

    assert(got == want)
