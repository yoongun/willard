import pytest
import torch
from willard.const import dirac
from willard.type import qreg


@pytest.fixture
def modified():
    qr = qreg(2)
    q = qr.bits('00')
    q.x()
    return qr


def test_reset(modified):
    modified.reset()
    got = modified.state
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
