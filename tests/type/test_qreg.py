import pytest
import torch
from willard.const import dirac
from willard.type import qreg


def test_init_qreg():
    qr = qreg()
    qr.bits(1)
    got = qr.state
    wanted = dirac.ket('0')
    assert(torch.equal(got, wanted))

    qr.bits(1)
    got = qr.state
    wanted = dirac.ket('00')
    assert(torch.equal(got, wanted))


@pytest.fixture
def modified():
    qr = qreg()
    q = qr.bits(2)
    q.x()
    return qr


def test_reset(modified):
    modified.reset()
    got = modified.state
    wanted = qreg().state
    assert(torch.equal(got, wanted))

    qr = qreg()
    q1 = qr.bits(3)
    q2 = qr.bits(1)
    qr.reset()
    with pytest.raises(AttributeError):
        q1.x()
    with pytest.raises(AttributeError):
        q2.x()


def test_len():
    q = qreg()
    got = len(q)
    wanted = 0
    assert(got == wanted)

    q = qreg()
    q.bits(5)
    got = len(q)
    wanted = 5
    assert(got == wanted)

    q = qreg()
    q.bits(1)
    got = len(q)
    wanted = 1
    assert(got == wanted)
