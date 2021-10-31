import pytest
import torch
from willard.type import qucrumb
from willard.const import dirac


def test_init_qucrumb():
    q = qucrumb()
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))


def test_reset():
    q = qucrumb()
    q.x(0).x(1).reset()
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))


def test_x_gate():
    # Case 1: Apply X gate on the first qubit
    q = qucrumb()
    q.x(0)
    got = q.state
    want = dirac.ket('01')
    assert(torch.equal(got, want))

    # Case 2: Apply X gate on the second qubit
    q = qucrumb()
    q.x(1)
    got = q.state
    want = dirac.ket('10')
    assert(torch.equal(q.state, torch.tensor([[0.], [0.], [1.], [0.]])))

    # Checks whether the code checks index range
    q = qucrumb()
    with pytest.raises(IndexError):
        q.x(2)


def test_rnot_gate():
    q = qucrumb()
    q.rnot(0).rnot(0)
    got = q.state
    want = dirac.ket('01')
    assert(torch.equal(got, want))

    q = qucrumb()
    q.rnot(1).rnot(1)
    got = q.state
    want = dirac.ket('10')
    assert(torch.equal(got, want))


def test_y_gate():
    # Case 1: Apply Y gate on the first qubit
    q = qucrumb()
    q.y(0)
    got = q.state
    want = torch.tensor([[0.], [1.j], [0.], [0.]])
    assert(torch.equal(got, want))

    # Case 2: Apply Y gate on the second qubit
    q = qucrumb()
    q.y(1)
    got = q.state
    want = torch.tensor([[0.], [0.], [1.j], [0.]])
    assert(torch.equal(got, want))

    # Checks whether the code checks index range
    q = qucrumb()
    with pytest.raises(IndexError):
        q.y(2)


def test_z_gate():
    # Case 1: Apply Z gate on the first qubit
    q = qucrumb()
    q.z(0)
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Case 2: Apply Z gate on the second qubit
    q = qucrumb()
    q.z(1)
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Checks whether the code checks index range
    q = qucrumb()
    with pytest.raises(IndexError):
        q.z(2)


def test_h_gate():
    # Case 1: Apply H gate on the first qubit
    q = qucrumb()
    q.h(0)
    got = q.state
    want = torch.tensor(
        [[1. / math.sqrt(2)], [1. / math.sqrt(2)], [0.], [0.]])
    assert(torch.equal(got, want))

    # Case 2: Apply H gate on the second qubit
    q = qucrumb()
    q.h(1)
    got = q.state
    want = torch.tensor([[1. / math.sqrt(2)], [0.],
                         [1. / math.sqrt(2)], [0.]])
    assert(torch.equal(got, want))

    # Checks whether the code checks index range
    q = qucrumb()
    with pytest.raises(IndexError):
        q.h(2)


def test_s_gate():
    # Case 1: Apply S gate on the first qubit
    q = qucrumb()
    q.s(0)
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Case 2: Apply S gate on the second qubit
    q = qucrumb()
    q.s(1)
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(q.state, torch.tensor([[1.], [0.], [0.], [0.]])))

    # Checks whether the code checks index range
    q = qucrumb()
    with pytest.raises(IndexError):
        q.z(2)


def test_t_gate():
    # Case 1: Apply S gate on the first qubit
    q = qucrumb()
    q.t(0)
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Case 2: Apply S gate on the second qubit
    q = qucrumb()
    q.t(1)
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Checks whether the code checks index range
    q = qucrumb()
    with pytest.raises(IndexError):
        q.z(2)


def test_phase_gate():
    # Test case 1 (pi/2, S gate)
    q = qucrumb()
    q.x(0).phase(deg=90, idx=0)
    got = q.state
    want = torch.tensor([[0.], [1.j], [0.], [0.]])
    assert(torch.allclose(got, want))

    # Test case 2 (pi/4, T gate)
    q = qucrumb()
    q.x(1).phase(deg=45, idx=1)
    got = q.state
    want = torch.tensor([[0.], [0.], [torch.exp(1.j * torch.pi / 4)], [0.]])
    assert(torch.equal(got, want))


def test_dagger_gates():
    # Test case 1 (s dagger)
    q = qucrumb()
    q.s(0).s_dg(0)
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Test case 2 (t dagger)
    q = qucrumb()
    q.t(1).t_dg(1)
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))

    # Test case 3 (phase dagger)
    q = qucrumb()
    q.phase(deg=30, idx=0).phase_dg(deg=30, idx=0)
    got = q.state
    want = dirac.ket('00')
    assert(torch.equal(got, want))


def test_cnot():
    # Case 1: Test on the first qubit
    q = qucrumb()
    q.h(0).cnot(c=0, d=1)
    got = q.state
    want = torch.tensor([[1. / math.sqrt(2)], [0.],
                         [0.], [1. / math.sqrt(2)]])
    assert(torch.equal(got, want))

    # Case 2: Test on the second qubit
    q = qucrumb()
    q.h(1).cnot(c=1, d=0)
    got = q.state
    want = torch.tensor([[1. / math.sqrt(2)], [0.],
                         [0.], [1. / math.sqrt(2)]])
    assert(torch.equal(got, want))

    # Checks whether the code checks index range
    q = qucrumb()
    with pytest.raises(IndexError):
        q.cnot(c=2, d=2)


def test_cphase():
    # Case 1: Test on the first qubit
    q = qucrumb()
    q.h(0).x(1).cphase(c=0, d=1, deg=90)
    got = q.state
    want = torch.tensor(
        [[0.], [0.], [1. / math.sqrt(2)], [1.j / math.sqrt(2)]])
    assert(torch.allclose(got, want))

    # Case 2: Test on the second qubit
    q = qucrumb()
    q.h(1).x(0).cphase(c=1, d=0, deg=45)
    got = q.state
    want = torch.tensor([[0.], [1. / math.sqrt(2)], [0.], [0.5 + 0.5j]])
    assert(torch.allclose(got, want))

    # Checks whether the code checks index range
    q = qucrumb()
    with pytest.raises(IndexError):
        q.cphase(c=2, d=2, deg=180)


def test_swap():
    # Case 1: From qubit0 to qubit1
    q = qucrumb()
    q.x(0).swap(c=0, d=1)
    got = q.state
    want = dirac.ket('10')
    assert(torch.equal(got, want))

    # Case 1: From qubit1 to qubit0
    q = qucrumb()
    q.x(1).swap(c=0, d=1)
    got = q.state
    want = dirac.ket('01')
    assert(torch.equal(got, want))


def test_epr():
    q = qucrumb()
    want = q.h(0).cnot(c=0, d=1).measure(0)
    for _ in range(100):
        got = q.measure(1)
        assert(got == want)

    q = qucrumb()
    want = q.h(1).cnot(c=1, d=0).measure(1)
    for _ in range(100):
        got = q.measure(0)
        assert(got == want)
