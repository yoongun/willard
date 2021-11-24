import pytest
import torch
from willard.const import dirac
from willard.type import qreg


def test_init_qreg():
    qr = qreg()
    qr.bits(1)
    got = qr.state
    want = dirac.ket('0')
    assert(torch.equal(got, want))

    qr.bits(1)
    got = qr.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))


@pytest.fixture
def modified():
    qr = qreg()
    q = qr.bits(2)
    q.x()
    return qr


def test_reset(modified):
    modified.reset()
    got = modified.state
    want = qreg().state
    assert(torch.equal(got, want))


def test_len():
    q = qreg()
    got = len(q)
    want = 0
    assert(got == want)

    q = qreg()
    q.bits(5)
    got = len(q)
    want = 5
    assert(got == want)

    q = qreg()
    q.bits(1)
    got = len(q)
    want = 1
    assert(got == want)
