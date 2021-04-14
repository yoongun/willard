import pytest
import numpy as np
from willard.type import qreg
from willard.const import state


def test_init_qreg():
    from willard.type import qubit, qucrumb
    got = qreg(1).state
    want = qubit().state
    assert(np.array_equal(got, want))

    got = qreg(2).state
    want = qucrumb().state
    assert(np.array_equal(got, want))

    with pytest.raises(ValueError):
        qreg(0)

    with pytest.raises(ValueError):
        qreg(-1)


def test_reset():
    q = qucrumb()
    q.x(0).x(1).reset()
    got = q.state
    want = state.ket('00')
    assert(np.array_equal(got, want))


def test_x_gate():
    # Case 1: Apply X gate on the first qubit
    q = qucrumb()
    q.x(0)
    got = q.state
    want = state.ket('01')
    assert(np.array_equal(got, want))

    # Case 2: Apply X gate on the second qubit
    q = qucrumb()
    q.x(1)
    got = q.state
    want = state.ket('10')
    assert(np.array_equal(q.state, np.array([[0.], [0.], [1.], [0.]])))

    # Checks whether the code checks index range
    q = qucrumb()
    with pytest.raises(IndexError):
        q.x(2)


def test_rnot_gate():
    q = qucrumb()
    q.rnot(0).rnot(0)
    got = q.state
    want = state.ket('01')
    assert(np.array_equal(got, want))

    q = qucrumb()
    q.rnot(1).rnot(1)
    got = q.state
    want = state.ket('10')
    assert(np.array_equal(got, want))


def test_y_gate():
    # Case 1: Apply Y gate on the first qubit
    q = qucrumb()
    q.y(0)
    got = q.state
    want = np.array([[0.], [1.j], [0.], [0.]])
    assert(np.array_equal(got, want))

    # Case 2: Apply Y gate on the second qubit
    q = qucrumb()
    q.y(1)
    got = q.state
    want = np.array([[0.], [0.], [1.j], [0.]])
    assert(np.array_equal(got, want))

    # Checks whether the code checks index range
    q = qucrumb()
    with pytest.raises(IndexError):
        q.y(2)


def test_z_gate():
    # Case 1: Apply Z gate on the first qubit
    q = qucrumb()
    q.z(0)
    got = q.state
    want = state.ket('00')
    assert(np.array_equal(got, want))

    # Case 2: Apply Z gate on the second qubit
    q = qucrumb()
    q.z(1)
    got = q.state
    want = state.ket('00')
    assert(np.array_equal(got, want))

    # Checks whether the code checks index range
    q = qucrumb()
    with pytest.raises(IndexError):
        q.z(2)


def test_h_gate():
    # Case 1: Apply H gate on the first qubit
    q = qucrumb()
    q.h(0)
    got = q.state
    want = np.array([[1. / np.sqrt(2)], [1. / np.sqrt(2)], [0.], [0.]])
    assert(np.array_equal(got, want))

    # Case 2: Apply H gate on the second qubit
    q = qucrumb()
    q.h(1)
    got = q.state
    want = np.array([[1. / np.sqrt(2)], [0.], [1. / np.sqrt(2)], [0.]])
    assert(np.array_equal(got, want))

    # Checks whether the code checks index range
    q = qucrumb()
    with pytest.raises(IndexError):
        q.h(2)


def test_s_gate():
    # Case 1: Apply S gate on the first qubit
    q = qucrumb()
    q.s(0)
    got = q.state
    want = state.ket('00')
    assert(np.array_equal(got, want))

    # Case 2: Apply S gate on the second qubit
    q = qucrumb()
    q.s(1)
    got = q.state
    want = state.ket('00')
    assert(np.array_equal(q.state, np.array([[1.], [0.], [0.], [0.]])))

    # Checks whether the code checks index range
    q = qucrumb()
    with pytest.raises(IndexError):
        q.z(2)


def test_t_gate():
    # Case 1: Apply S gate on the first qubit
    q = qucrumb()
    q.t(0)
    got = q.state
    want = state.ket('00')
    assert(np.array_equal(got, want))

    # Case 2: Apply S gate on the second qubit
    q = qucrumb()
    q.t(1)
    got = q.state
    want = state.ket('00')
    assert(np.array_equal(got, want))

    # Checks whether the code checks index range
    q = qucrumb()
    with pytest.raises(IndexError):
        q.z(2)


def test_phase_gate():
    # Test case 1 (pi/2, S gate)
    q = qucrumb()
    q.x(0).phase(deg=90, idx=0)
    got = q.state
    want = np.array([[0.], [1.j], [0.], [0.]])
    assert(np.allclose(got, want))

    # Test case 2 (pi/4, T gate)
    q = qucrumb()
    q.x(1).phase(deg=45, idx=1)
    got = q.state
    want = np.array([[0.], [0.], [np.exp(1.j * np.pi / 4)], [0.]])
    assert(np.array_equal(got, want))


def test_dagger_gates():
    # Test case 1 (s dagger)
    q = qucrumb()
    q.s(0).s_dg(0)
    got = q.state
    want = state.ket('00')
    assert(np.array_equal(got, want))

    # Test case 2 (t dagger)
    q = qucrumb()
    q.t(1).t_dg(1)
    got = q.state
    want = state.ket('00')
    assert(np.array_equal(got, want))

    # Test case 3 (phase dagger)
    q = qucrumb()
    q.phase(deg=30, idx=0).phase_dg(deg=30, idx=0)
    got = q.state
    want = state.ket('00')
    assert(np.array_equal(got, want))


def test_cnot():
    # Case 1: Test on the first qubit
    q = qucrumb()
    q.h(0).cnot(c=0, d=1)
    got = q.state
    want = np.array([[1. / np.sqrt(2)], [0.], [0.], [1. / np.sqrt(2)]])
    assert(np.array_equal(got, want))

    # Case 2: Test on the second qubit
    q = qucrumb()
    q.h(1).cnot(c=1, d=0)
    got = q.state
    want = np.array([[1. / np.sqrt(2)], [0.], [0.], [1. / np.sqrt(2)]])
    assert(np.array_equal(got, want))

    # Checks whether the code checks index range
    q = qucrumb()
    with pytest.raises(IndexError):
        q.cnot(c=2, d=2)


def test_cphase():
    # Case 1: Test on the first qubit
    q = qucrumb()
    q.h(0).x(1).cphase(c=0, d=1, deg=90)
    got = q.state
    want = np.array([[0.], [0.], [1. / np.sqrt(2)], [1.j / np.sqrt(2)]])
    assert(np.allclose(got, want))

    # Case 2: Test on the second qubit
    q = qucrumb()
    q.h(1).x(0).cphase(c=1, d=0, deg=45)
    got = q.state
    want = np.array([[0.], [1. / np.sqrt(2)], [0.], [0.5 + 0.5j]])
    assert(np.allclose(got, want))

    # Checks whether the code checks index range
    q = qucrumb()
    with pytest.raises(IndexError):
        q.cphase(c=2, d=2, deg=180)


def test_swap():
    # Case 1: From qubit0 to qubit1
    q = qucrumb()
    q.x(0).swap(c=0, d=1)
    got = q.state
    want = state.ket('10')
    assert(np.array_equal(got, want))

    # Case 1: From qubit1 to qubit0
    q = qucrumb()
    q.x(1).swap(c=0, d=1)
    got = q.state
    want = state.ket('01')
    assert(np.array_equal(got, want))


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


def test_toffoli_gate():
    q = qreg(3)
    q.toffoli(c1=0, c2=1, d=2)
    got = q.state
    want = state.ket('000')
    assert(np.array_equal(got, want))

    q = qreg(3)
    q.x(2)
    q.toffoli(c1=2, c2=1, d=0)
    got = q.state
    want = state.ket('100')
    assert(np.array_equal(got, want))

    q = qreg(3)
    q.x(1)
    q.toffoli(c1=2, c2=1, d=0)
    got = q.state
    want = state.ket('010')
    assert(np.array_equal(got, want))

    q = qreg(3)
    q.x(0).x(2)
    q.toffoli(c1=0, c2=2, d=1)
    got = q.state
    want = state.ket('111')
    assert(np.array_equal(got, want))

    with pytest.raises(IndexError):
        q.toffoli(c1=0, c2=0, d=1)


def test_cphase_commutativity():
    q1 = qreg(3)
    q1.h(0).x(2).cphase(c=0, d=2, deg=90)
    q2 = qreg(3)
    q2.h(0).x(2).cphase(c=2, d=0, deg=90)
    assert(np.allclose(q1.state, q2.state))

    q1 = qreg(3)
    q1.h(1).x(2).cphase(c=1, d=2, deg=33)
    q2 = qreg(3)
    q2.h(1).x(2).cphase(c=2, d=1, deg=33)
    assert(np.allclose(q1.state, q2.state))


def test_swap_test():
    q = qreg(3)
    q.swap_test(input1=0, input2=1, output=2)
    assert(q.measure(2) == 1)

    q = qreg(3)
    q.x(0)
    q.swap_test(input1=0, input2=1, output=2)
    assert(q.measure(2) == 0)

    q = qreg(3)
    q.h(0).h(1)
    q.swap_test(input1=0, input2=1, output=2)
    assert(q.measure(2) == 1)

    # q = qreg(3)
    # q.x(0).h(1)
    # swap_test(q, input1=0, input2=1, output=2)
    # assert(q.measure(2) == 0)
