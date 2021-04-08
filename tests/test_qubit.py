import numpy as np
from willard.type import qubit


def test_init_qubit():
    q = qubit()
    got = q.state
    want = np.array([[1.], [0.]])
    assert(np.array_equal(got, want))


def test_x_gate():
    q = qubit()
    q.x()
    got = q.state
    want = np.array([[0.], [1.]])
    assert(np.array_equal(got, want))


def test_y_gate():
    # Test case 1 (on state [1, 0])
    q = qubit()
    q.y()
    got = q.state
    want = np.array([[0.], [1.j]])
    assert(np.array_equal(got, want))

    # Test case 2 (on state [0, 1])
    q = qubit()
    q.x().y()
    got = q.state
    want = np.array([[-1.j], [0.]])
    assert(np.array_equal(got, want))


def test_z_gate():
    # Test case 1 (on state [1, 0])
    q = qubit()
    q.z()
    got = q.state
    want = np.array([[1.], [0.]])
    assert(np.array_equal(got, want))

    # Test case 2 (on state [0, 1])
    q = qubit()
    q.x().z()
    got = q.state
    want = np.array([[0.], [-1.]])
    assert(np.array_equal(got, want))


def test_h_gate():
    # Test case 1 (on state [1, 0])
    q = qubit()
    q.h()
    got = q.state
    want = np.array([[1. / np.sqrt(2)], [1. / np.sqrt(2)]])
    assert(np.array_equal(got, want))

    # Test case 2 (on state [0, 1])
    q = qubit()
    q.x().h()
    got = q.state
    want = np.array([[1. / np.sqrt(2)], [-1. / np.sqrt(2)]])
    assert(np.array_equal(got, want))


def test_s_gate():
    # Test case 1 (on state [1, 0])
    q = qubit()
    q.s()
    got = q.state
    want = np.array([[1.], [0.]])
    assert(np.array_equal(got, want))

    # Test case 2 (on state [0, 1])
    q = qubit()
    q.x().s()
    got = q.state
    want = np.array([[0.], [1.j]])
    assert(np.allclose(got, want))


def test_t_gate():
    # Test case 1 (on state [1, 0])
    q = qubit()
    q.t()
    got = q.state
    want = np.array([[1.], [0.]])
    assert(np.array_equal(got, want))

    # Test case 2 (on state [0, 1])
    q = qubit()
    q.x().t()
    got = q.state
    want = np.array([[0.], [np.exp(1.j * np.pi / 4)]])
    assert(np.array_equal(got, want))


def test_phase_gate():
    # Test case 1 (pi/2, S gate)
    q = qubit()
    q.x().phase(90)
    got = q.state
    want = np.array([[0.], [1.j]])
    assert(np.allclose(got, want))

    # Test case 2 (pi/4, T gate)
    q = qubit()
    q.x().phase(45)
    got = q.state
    want = np.array([[0.], [np.exp(1.j * np.pi / 4)]])
    assert(np.array_equal(got, want))


def test_dagger_gates():
    # Test case 1 (s dagger)
    q = qubit()
    q.s().s_dg()
    got = q.state
    want = np.array([[1.], [0.]])
    assert(np.array_equal(got, want))

    # Test case 2 (t dagger)
    q = qubit()
    q.t().t_dg()
    got = q.state
    want = np.array([[1.], [0.]])
    assert(np.array_equal(got, want))

    # Test case 3 (phase dagger)
    q = qubit()
    q.phase(30).phase_dg(30)
    got = q.state
    want = np.array([[1.], [0.]])
    assert(np.array_equal(got, want))


def test_measure():
    # Test case 1 (on state [1, 0])
    q = qubit()
    got = q.measure()
    want = 0
    assert(got == want)

    # Test case 2 (on state [1, 0])
    q = qubit()
    got = q.x().measure()
    want = 1
    assert(got == want)

    # Test case 3 (on superposition)
    q = qubit()
    want = q.h().measure()
    for _ in range(100):
        got = q.measure()
        assert(got == want)
