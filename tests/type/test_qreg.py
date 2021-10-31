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
    q.x(0).x(1).reset()
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))


def test_x_gate():
    # Case 1: Apply X gate on the first qubit
    q = qreg(2)
    q.x(0)
    got = q.state
    want = dirac.ket('01')
    assert(torch.equal(got, want))

    # Case 2: Apply X gate on the second qubit
    q = qreg(2)
    q.x(1)
    got = q.state
    want = dirac.ket('10')
    assert(torch.equal(q.state, torch.tensor(
        [[0.], [0.], [1.], [0.]], dtype=torch.cfloat)))

    # Checks whether the code checks index range
    q = qreg(2)
    with pytest.raises(IndexError):
        q.x(2)


def test_rnot_gate():
    q = qreg(2)
    q.rnot(0).rnot(0)
    got = q.state
    want = dirac.ket('01')
    assert(torch.equal(got, want))

    q = qreg(2)
    q.rnot(1).rnot(1)
    got = q.state
    want = dirac.ket('10')
    assert(torch.equal(got, want))


def test_y_gate():
    # Case 1: Apply Y gate on the first qubit
    q = qreg(2)
    q.y(0)
    got = q.state
    want = torch.tensor([[0.], [1.j], [0.], [0.]], dtype=torch.cfloat)
    assert(torch.equal(got, want))

    # Case 2: Apply Y gate on the second qubit
    q = qreg(2)
    q.y(1)
    got = q.state
    want = torch.tensor([[0.], [0.], [1.j], [0.]], dtype=torch.cfloat)
    assert(torch.equal(got, want))

    # Checks whether the code checks index range
    q = qreg(2)
    with pytest.raises(IndexError):
        q.y(2)


def test_z_gate():
    # Case 1: Apply Z gate on the first qubit
    q = qreg(2)
    q.z(0)
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Case 2: Apply Z gate on the second qubit
    q = qreg(2)
    q.z(1)
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Checks whether the code checks index range
    q = qreg(2)
    with pytest.raises(IndexError):
        q.z(2)


def test_h_gate():
    # Case 1: Apply H gate on the first qubit
    q = qreg(2)
    q.h(0)
    got = q.state
    want = torch.tensor(
        [[1. / np.sqrt(2)], [1. / np.sqrt(2)], [0.], [0.]], dtype=torch.cfloat)
    assert(torch.equal(got, want))

    # Case 2: Apply H gate on the second qubit
    q = qreg(2)
    q.h(1)
    got = q.state
    want = torch.tensor([[1. / np.sqrt(2)], [0.],
                         [1. / np.sqrt(2)], [0.]], dtype=torch.cfloat)
    assert(torch.equal(got, want))

    # Checks whether the code checks index range
    q = qreg(2)
    with pytest.raises(IndexError):
        q.h(2)


def test_s_gate():
    # Case 1: Apply S gate on the first qubit
    q = qreg(2)
    q.s(0)
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Case 2: Apply S gate on the second qubit
    q = qreg(2)
    q.s(1)
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(q.state, torch.tensor(
        [[1.], [0.], [0.], [0.]], dtype=torch.cfloat)))

    # Checks whether the code checks index range
    q = qreg(2)
    with pytest.raises(IndexError):
        q.z(2)


def test_t_gate():
    # Case 1: Apply S gate on the first qubit
    q = qreg(2)
    q.t(0)
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Case 2: Apply S gate on the second qubit
    q = qreg(2)
    q.t(1)
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Checks whether the code checks index range
    q = qreg(2)
    with pytest.raises(IndexError):
        q.z(2)


def test_phase_gate():
    # Test case 1 (pi/2, S gate)
    q = qreg(2)
    q.x(0).phase(deg=90, idx=0)
    got = q.state
    want = torch.tensor([[0.], [1.j], [0.], [0.]], dtype=torch.cfloat)
    assert(torch.allclose(got, want))

    # Test case 2 (pi/4, T gate)
    q = qreg(2)
    q.x(1).phase(deg=45, idx=1)
    got = q.state
    want = torch.tensor(
        [[0.], [0.], [np.exp(1.j * np.pi / 4)], [0.]], dtype=torch.cfloat)
    assert(torch.equal(got, want))


def test_dagger_gates():
    # Test case 1 (s dagger)
    q = qreg(2)
    q.s(0).s_dg(0)
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Test case 2 (t dagger)
    q = qreg(2)
    q.t(1).t_dg(1)
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Test case 3 (phase dagger)
    q = qreg(2)
    q.phase(deg=30, idx=0).phase_dg(deg=30, idx=0)
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))


def test_cx():
    # Case 1: Test on the first qubit
    q = qreg(2)
    q.h(0).cx(0, 1)
    got = q.state
    want = torch.tensor([[1. / np.sqrt(2)], [0.],
                         [0.], [1. / np.sqrt(2)]], dtype=torch.cfloat)
    assert(torch.equal(got, want))

    # Case 2: Test on the second qubit
    q = qreg(2)
    q.h(1).cx(1, 0)
    got = q.state
    want = torch.tensor([[1. / np.sqrt(2)], [0.],
                         [0.], [1. / np.sqrt(2)]], dtype=torch.cfloat)
    assert(torch.equal(got, want))

    # Checks whether the code checks index range
    q = qreg(2)
    with pytest.raises(IndexError):
        q.cx(2, 2)


def test_cphase():
    # Case 1: Test on the first qubit
    q = qreg(2)
    q.h(0).x(1).cphase(c=0, d=1, deg=90)
    got = q.state
    want = torch.tensor(
        [[0.], [0.], [1. / np.sqrt(2)], [1.j / np.sqrt(2)]], dtype=torch.cfloat)
    assert(torch.allclose(got, want))

    # Case 2: Test on the second qubit
    q = qreg(2)
    q.h(1).x(0).cphase(c=1, d=0, deg=45)
    got = q.state
    want = torch.tensor([[0.], [1. / np.sqrt(2)], [0.],
                         [0.5 + 0.5j]], dtype=torch.cfloat)
    assert(torch.allclose(got, want))

    # Checks whether the code checks index range
    q = qreg(2)
    with pytest.raises(IndexError):
        q.cphase(c=2, d=2, deg=180)


def test_swap():
    # Case 1: From qubit0 to qubit1
    q = qreg(2)
    q.x(0).swap(c=0, d=1)
    got = q.state
    want = dirac.ket('10')
    assert(torch.equal(got, want))

    # Case 1: From qubit1 to qubit0
    q = qreg(2)
    q.x(1).swap(c=0, d=1)
    got = q.state
    want = dirac.ket('01')
    assert(torch.equal(got, want))


def test_epr():
    q = qreg(2)
    want = q.h(0).cx(0, 1).measure(0)
    for _ in range(100):
        got = q.measure(1)
        assert(got == want)

    q = qreg(2)
    want = q.h(1).cx(1, 0).measure(1)
    for _ in range(100):
        got = q.measure(0)
        assert(got == want)


def test_toffoli_gate():
    q = qreg(3)
    q.toffoli(c1=0, c2=1, d=2)
    got = q.state
    want = dirac.ket('000')
    assert(torch.equal(got, want))

    q = qreg(3)
    q.x(2)
    q.toffoli(c1=2, c2=1, d=0)
    got = q.state
    want = dirac.ket('100')
    assert(torch.equal(got, want))

    q = qreg(3)
    q.x(1)
    q.toffoli(c1=2, c2=1, d=0)
    got = q.state
    want = dirac.ket('010')
    assert(torch.equal(got, want))

    q = qreg(3)
    q.x(0).x(2)
    q.toffoli(c1=0, c2=2, d=1)
    got = q.state
    want = dirac.ket('111')
    assert(torch.equal(got, want))

    with pytest.raises(IndexError):
        q.toffoli(c1=0, c2=0, d=1)


def test_cphase_commutativity():
    q1 = qreg(3)
    q1.h(0).x(2).cphase(c=0, d=2, deg=90)
    q2 = qreg(3)
    q2.h(0).x(2).cphase(c=2, d=0, deg=90)
    assert(torch.allclose(q1.state, q2.state))

    q1 = qreg(3)
    q1.h(1).x(2).cphase(c=1, d=2, deg=33)
    q2 = qreg(3)
    q2.h(1).x(2).cphase(c=2, d=1, deg=33)
    assert(torch.allclose(q1.state, q2.state))


def test_measure():
    pytest.fail()
