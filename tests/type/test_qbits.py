import pytest
import torch
import numpy as np
from willard.type import qreg
from willard.const import dirac


@pytest.fixture
def qr():
    return qreg()


def test_init_qbits():
    qr = qreg()
    q = qr.bits(1)
    got = q.measure()
    want = '0'
    assert(got == want)

    q = qr.bits(1, '1')
    got = q.measure()
    want = '1'
    assert(got == want)


def test_x_gate():
    qr = qreg()
    q = qr.bits(2)

    # Case 1: Apply X gate on the first qubit
    q[0].x()
    got = q.global_state
    want = dirac.ket('01')
    assert(torch.equal(got, want))

    # Case 2: Apply X gate on the second qubit
    qr.reset()
    q = qr.bits(2)
    q[1].x()
    got = q.global_state
    want = dirac.ket('10')
    assert(torch.equal(got, want))

    # Checks whether the code checks index range
    qr.reset()
    with pytest.raises(IndexError):
        q[2].x()


def test_rnot_gate():
    qr = qreg()
    q = qr.bits(2)
    q[0].rnot().rnot()
    got = q.global_state
    want = dirac.ket('01')
    assert(torch.equal(got, want))

    qr.reset()
    q = qr.bits(2)
    q[1].rnot().rnot()
    got = q.global_state
    want = dirac.ket('10')
    assert(torch.equal(got, want))


def test_y_gate():
    # Case 1: Apply Y gate on the first qubit
    qr = qreg()
    q = qr.bits(2)
    q[0].y()
    got = q.global_state
    want = torch.tensor([[0.], [1.j], [0.], [0.]], dtype=torch.cfloat)
    assert(torch.equal(got, want))

    # Case 2: Apply Y gate on the second qubit
    qr.reset()
    q = qr.bits(2)
    q[1].y()
    got = q.global_state
    want = torch.tensor([[0.], [0.], [1.j], [0.]], dtype=torch.cfloat)
    assert(torch.equal(got, want))

    # Checks whether the code checks index range
    qr.reset()
    q = qr.bits(2)
    with pytest.raises(IndexError):
        q[2].y()


def test_z_gate():
    # Case 1: Apply Z gate on the first qubit
    qr = qreg()
    q = qr.bits(2)
    q[0].z()
    got = q.global_state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Case 2: Apply Z gate on the second qubit
    qr.reset()
    q = qr.bits(2)
    q[1].z()
    got = q.global_state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Checks whether the code checks index range
    qr.reset()
    q = qr.bits(2)
    with pytest.raises(IndexError):
        q[2].z()


def test_h_gate():
    # Case 1: Apply H gate on the first qubit
    qr = qreg()
    q = qr.bits(2)
    q[0].h()
    got = q.global_state
    want = torch.tensor(
        [[1. / np.sqrt(2)], [1. / np.sqrt(2)], [0.], [0.]], dtype=torch.cfloat)
    assert(torch.equal(got, want))

    # Case 2: Apply H gate on the second qubit
    qr.reset()
    q = qr.bits(2)
    q[1].h()
    got = q.global_state
    want = torch.tensor([[1. / np.sqrt(2)], [0.],
                         [1. / np.sqrt(2)], [0.]], dtype=torch.cfloat)
    assert(torch.equal(got, want))

    # Checks whether the code checks index range
    qr.reset()
    q = qr.bits(2)
    with pytest.raises(IndexError):
        q[2].h()


def test_s_gate():
    # Case 1: Apply S gate on the first qubit
    qr = qreg()
    q = qr.bits(2)
    q[0].s()
    got = q.global_state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Case 2: Apply S gate on the second qubit
    qr.reset()
    q = qr.bits(2)
    q[1].s()
    got = q.global_state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Checks whether the code checks index range
    qr.reset()
    q = qr.bits(2)
    with pytest.raises(IndexError):
        q[2].s()


def test_t_gate():
    # Case 1: Apply S gate on the first qubit
    qr = qreg()
    q = qr.bits(2)
    q[0].t()
    got = q.global_state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Case 2: Apply S gate on the second qubit
    qr.reset()
    q = qr.bits(2)
    q[1].t()
    got = q.global_state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Checks whether the code checks index range
    qr.reset()
    q = qr.bits(2)
    with pytest.raises(IndexError):
        q[2].t()


def test_phase_gate():
    # Test case 1 (pi/2, S gate)
    qr = qreg()
    q = qr.bits(2)
    q[0].x().phase(90)
    got = q.global_state
    want = torch.tensor([[0.], [1.j], [0.], [0.]], dtype=torch.cfloat)
    assert(torch.allclose(got, want))

    # Test case 2 (pi/4, T gate)
    qr.reset()
    q = qr.bits(2)
    q[1].x().phase(45)
    got = q.global_state
    want = torch.tensor(
        [[0.], [0.], [np.exp(1.j * np.pi / 4)], [0.]], dtype=torch.cfloat)
    assert(torch.equal(got, want))


def test_dagger_gates():
    # Test case 1 (s dagger)
    qr = qreg()
    q = qr.bits(2)
    q[0].s().s_dg()
    got = q.global_state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Test case 2 (t dagger)
    qr.reset()
    q = qr.bits(2)
    q[1].t().t_dg()
    got = q.global_state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Test case 3 (phase dagger)
    qr.reset()
    q = qr.bits(2)
    q[0].phase(30).phase_dg(30)
    got = q.global_state
    want = dirac.ket('00')
    assert(torch.equal(got, want))


def test_cx():
    # Case 1: Test on the first qubit
    qr = qreg()
    q = qr.bits(2)
    q[0].h().cx(q[1])
    got = q.global_state
    want = torch.tensor([[1. / np.sqrt(2)], [0.],
                         [0.], [1. / np.sqrt(2)]], dtype=torch.cfloat)
    assert(torch.equal(got, want))

    # Case 2: Test on the second qubit
    qr.reset()
    q = qr.bits(2)
    q[1].h().cx(q[0])
    got = q.global_state
    want = torch.tensor([[1. / np.sqrt(2)], [0.],
                         [0.], [1. / np.sqrt(2)]], dtype=torch.cfloat)
    assert(torch.equal(got, want))

    # Checks whether the code checks index range
    qr.reset()
    q = qr.bits(2)
    with pytest.raises(IndexError):
        q[2].cx(q[2])


def test_cphase():
    # Case 1: Test on the first qubit
    qr = qreg()
    q = qr.bits(2)
    q[0].h()
    q[1].x()
    q[0, 1].cphase(90)
    got = q.global_state
    want = torch.tensor(
        [[0.], [0.], [1. / np.sqrt(2)], [1.j / np.sqrt(2)]],
        dtype=torch.cfloat)
    assert(torch.allclose(got, want))

    # Case 2: Test on the second qubit
    qr.reset()
    q = qr.bits(2)
    q[1].h()
    q[0].x()
    q[1, 0].cphase(45)
    got = q.global_state
    want = torch.tensor([[0.], [1. / np.sqrt(2)], [0.],
                         [0.5 + 0.5j]], dtype=torch.cfloat)
    assert(torch.allclose(got, want))

    # Checks whether the code checks index range
    qr.reset()
    q = qr.bits(2)
    with pytest.raises(IndexError):
        q[2, 2].cphase(180)


def test_swap():
    # Case 1: From qubit0 to qubit1
    qr = qreg()
    q = qr.bits(2)
    q[0].x()
    q[0, 1].swap()
    got = q.global_state
    want = dirac.ket('10')
    assert(torch.equal(got, want))

    # Case 2: From qubit1 to qubit0
    qr.reset()
    q = qr.bits(2)
    q[1].x()
    q[1, 0].swap()
    got = q.global_state
    want = dirac.ket('01')
    assert(torch.equal(got, want))


def test_epr():
    qr = qreg()
    q = qr.bits(2)
    want = q[0].h().cx(q[1]).measure()
    for _ in range(100):
        got = q[1].measure()
        assert(got == want)

    qr.reset()
    q = qr.bits(2)
    want = q[1].h().cx(q[0]).measure()
    for _ in range(100):
        got = q[0].measure()
        assert(got == want)


def test_toffoli_gate():
    qr = qreg()
    q = qr.bits(3)
    q[0, 1].toffoli(q[2])
    got = q.global_state
    want = dirac.ket('000')
    assert(torch.equal(got, want))

    qr.reset()
    q = qr.bits(3)
    q[2].x()
    q[2, 1].toffoli(q[0])
    got = q.global_state
    want = dirac.ket('100')
    assert(torch.equal(got, want))

    qr.reset()
    q = qr.bits(3)
    q[1].x()
    q[2, 1].toffoli(q[0])
    got = q.global_state
    want = dirac.ket('010')
    assert(torch.equal(got, want))

    qr.reset()
    q = qr.bits(3)
    q[0].x()
    q[2].x()
    q[0, 2].toffoli(q[1])
    got = q.global_state
    want = dirac.ket('111')
    assert(torch.equal(got, want))

    qr.reset()
    with pytest.raises(IndexError):
        q[0, 0].toffoli(q[1])


def test_phase_kickback():
    qr1 = qreg()
    qr2 = qreg()
    q1 = qr1.bits(3)
    q2 = qr2.bits(3)
    q1[0].h()
    q1[2].x()
    q1[0, 2].cphase(90)
    q2[0].h()
    q2[2].x()
    q2[2, 0].cphase(90)
    got = q2.global_state
    want = q1.global_state
    assert(torch.allclose(got, want))

    qr1.reset()
    qr2.reset()
    q1 = qr1.bits(3)
    q2 = qr2.bits(3)
    q1[1].h()
    q1[2].x()
    q1[1, 2].cphase(33)
    q2[1].h()
    q2[2].x()
    q2[2, 1].cphase(33)
    got = q2.global_state
    want = q1.global_state
    assert(torch.allclose(got, want))


def test_measure():
    # Test case 1 (on state [1, 0])
    qr = qreg()
    q = qr.bits(1)
    got = q.measure()
    want = '0'
    assert(got == want)

    # Test case 2 (on state [0, 1])
    qr.reset()
    q = qr.bits(1)
    got = q.x().measure()
    want = '1'
    assert(got == want)

    # Test case 3 (on superposition)
    qr.reset()
    q = qr.bits(1)
    want = q.h().measure()
    for _ in range(100):
        got = q.measure()
        assert(got == want)
