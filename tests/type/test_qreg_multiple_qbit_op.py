import pytest
import torch
import numpy as np
from willard.type import qreg
from willard.const import dirac


def test_cx():
    # Case 1: Test on the first qubit
    q = qreg(2)
    q[0].h().cx(q[1])
    got = q.state
    want = torch.tensor([[1. / np.sqrt(2)], [0.],
                         [0.], [1. / np.sqrt(2)]], dtype=torch.cfloat)
    assert(torch.equal(got, want))

    # Case 2: Test on the second qubit
    q = qreg(2)
    q[1].h().cx(q[0])
    got = q.state
    want = torch.tensor([[1. / np.sqrt(2)], [0.],
                         [0.], [1. / np.sqrt(2)]], dtype=torch.cfloat)
    assert(torch.equal(got, want))

    # Checks whether the code checks index range
    q = qreg(2)
    with pytest.raises(IndexError):
        q[2].cx(q[2])


def test_cphase():
    # Case 1: Test on the first qubit
    q = qreg(2)
    q[0].h()
    q[1].x()
    q[0].cphase(90, q[1])
    got = q.state
    want = torch.tensor(
        [[0.], [0.], [1. / np.sqrt(2)], [1.j / np.sqrt(2)]], dtype=torch.cfloat)
    assert(torch.allclose(got, want))

    # Case 2: Test on the second qubit
    q = qreg(2)
    q[1].h()
    q[0].x()
    q[1].cphase(45, q[0])
    got = q.state
    want = torch.tensor([[0.], [1. / np.sqrt(2)], [0.],
                         [0.5 + 0.5j]], dtype=torch.cfloat)
    assert(torch.allclose(got, want))

    # Checks whether the code checks index range
    q = qreg(2)
    with pytest.raises(IndexError):
        q[2].cphase(180, q[2])


def test_swap():
    # Case 1: From qubit0 to qubit1
    q = qreg(2)
    q[0].x().swap(q[1])
    got = q.state
    want = dirac.ket('10')
    assert(torch.equal(got, want))

    # Case 1: From qubit1 to qubit0
    q = qreg(2)
    q[1].x().swap(q[0])
    got = q.state
    want = dirac.ket('01')
    assert(torch.equal(got, want))


def test_epr():
    q = qreg(2)
    want = q[0].h().cx(q[1]).measure()
    for _ in range(100):
        got = q[1].measure()
        assert(got == want)

    q = qreg(2)
    want = q[1].h().cx(q[0]).measure()
    for _ in range(100):
        got = q[0].measure()
        assert(got == want)


def test_toffoli_gate():
    q = qreg(3)
    q[0, 1].toffoli(q[2])
    got = q.state
    want = dirac.ket('000')
    assert(torch.equal(got, want))

    q = qreg(3)
    q[2].x()
    q[2, 1].toffoli(q[0])
    got = q.state
    want = dirac.ket('100')
    assert(torch.equal(got, want))

    q = qreg(3)
    q[1].x()
    q[2, 1].toffoli(q[0])
    got = q.state
    want = dirac.ket('010')
    assert(torch.equal(got, want))

    q = qreg(3)
    q[0].x()
    q[2].x()
    q[0, 2].toffoli(q[1])
    got = q.state
    want = dirac.ket('111')
    assert(torch.equal(got, want))

    with pytest.raises(IndexError):
        q[0, 0].toffoli(q[1])


def test_cphase_commutativity():
    q1 = qreg(3)
    q1[0].h()
    q1[2].x()
    q1[0].cphase(90, q1[2])
    q2 = qreg(3)
    q2[0].h()
    q2[2].x()
    q2[2].cphase(90, q2[0])
    assert(torch.allclose(q1.state, q2.state))

    q1 = qreg(3)
    q1[1].h()
    q1[2].x()
    q1[1].cphase(33, q1[2])
    q2 = qreg(3)
    q2[1].h()
    q2[2].x()
    q2[2].cphase(33, q2[1])
    assert(torch.allclose(q1.state, q2.state))


# def test_measure():
#     pytest.fail()
