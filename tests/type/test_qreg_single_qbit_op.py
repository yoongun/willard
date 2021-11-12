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


def test_x_gate():
    # Case 1: Apply X gate on the first qubit
    q = qreg(2)
    q[0].x()
    got = q.state
    want = dirac.ket('01')
    assert(torch.equal(got, want))

    # Case 2: Apply X gate on the second qubit
    q = qreg(2)
    q[1].x()
    got = q.state
    want = dirac.ket('10')
    assert(torch.equal(q.state, torch.tensor(
        [[0.], [0.], [1.], [0.]], dtype=torch.cfloat)))

    # Checks whether the code checks index range
    q = qreg(2)
    with pytest.raises(IndexError):
        q[2].x()


def test_rnot_gate():
    q = qreg(2)
    q[0].rnot().rnot()
    got = q.state
    want = dirac.ket('01')
    assert(torch.equal(got, want))

    q = qreg(2)
    q[1].rnot().rnot()
    got = q.state
    want = dirac.ket('10')
    assert(torch.equal(got, want))


def test_y_gate():
    # Case 1: Apply Y gate on the first qubit
    q = qreg(2)
    q[0].y()
    got = q.state
    want = torch.tensor([[0.], [1.j], [0.], [0.]], dtype=torch.cfloat)
    assert(torch.equal(got, want))

    # Case 2: Apply Y gate on the second qubit
    q = qreg(2)
    q[1].y()
    got = q.state
    want = torch.tensor([[0.], [0.], [1.j], [0.]], dtype=torch.cfloat)
    assert(torch.equal(got, want))

    # Checks whether the code checks index range
    q = qreg(2)
    with pytest.raises(IndexError):
        q[2].y()


def test_z_gate():
    # Case 1: Apply Z gate on the first qubit
    q = qreg(2)
    q[0].z()
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Case 2: Apply Z gate on the second qubit
    q = qreg(2)
    q[1].z()
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Checks whether the code checks index range
    q = qreg(2)
    with pytest.raises(IndexError):
        q[2].z()


def test_h_gate():
    # Case 1: Apply H gate on the first qubit
    q = qreg(2)
    q[0].h()
    got = q.state
    want = torch.tensor(
        [[1. / np.sqrt(2)], [1. / np.sqrt(2)], [0.], [0.]], dtype=torch.cfloat)
    assert(torch.equal(got, want))

    # Case 2: Apply H gate on the second qubit
    q = qreg(2)
    q[1].h()
    got = q.state
    want = torch.tensor([[1. / np.sqrt(2)], [0.],
                         [1. / np.sqrt(2)], [0.]], dtype=torch.cfloat)
    assert(torch.equal(got, want))

    # Checks whether the code checks index range
    q = qreg(2)
    with pytest.raises(IndexError):
        q[2].h()


def test_s_gate():
    # Case 1: Apply S gate on the first qubit
    q = qreg(2)
    q[0].s()
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Case 2: Apply S gate on the second qubit
    q = qreg(2)
    q[1].s()
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(q.state, torch.tensor(
        [[1.], [0.], [0.], [0.]], dtype=torch.cfloat)))

    # Checks whether the code checks index range
    q = qreg(2)
    with pytest.raises(IndexError):
        q[2].s()


def test_t_gate():
    # Case 1: Apply S gate on the first qubit
    q = qreg(2)
    q[0].t()
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Case 2: Apply S gate on the second qubit
    q = qreg(2)
    q[1].t()
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Checks whether the code checks index range
    q = qreg(2)
    with pytest.raises(IndexError):
        q[2].t()


def test_phase_gate():
    # Test case 1 (pi/2, S gate)
    q = qreg(2)
    q[0].x().phase(90)
    got = q.state
    want = torch.tensor([[0.], [1.j], [0.], [0.]], dtype=torch.cfloat)
    assert(torch.allclose(got, want))

    # Test case 2 (pi/4, T gate)
    q = qreg(2)
    q[1].x().phase(45)
    got = q.state
    want = torch.tensor(
        [[0.], [0.], [np.exp(1.j * np.pi / 4)], [0.]], dtype=torch.cfloat)
    assert(torch.equal(got, want))


def test_dagger_gates():
    # Test case 1 (s dagger)
    q = qreg(2)
    q[0].s().s_dg()
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Test case 2 (t dagger)
    q = qreg(2)
    q[1].t().t_dg()
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Test case 3 (phase dagger)
    q = qreg(2)
    q[0].phase(30).phase_dg(30)
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

# def test_measure():
#     pytest.fail()
