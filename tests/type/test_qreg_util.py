import pytest
import torch
from willard.type import qreg
from willard.const import dirac


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
