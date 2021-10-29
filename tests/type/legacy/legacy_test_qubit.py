import torch
from willard.type import qubit
from willard.const import state


def test_init_qubit():
    q = qubit()
    got = q.state
    want = state.ket('0')
    assert(torch.equal(got, want))


def test_reset():
    q = qubit()
    q.x(0).reset()
    got = q.state
    want = state.ket('0')
    assert(torch.equal(got, want))


def test_x_gate():
    q = qubit()
    q.x(0)
    got = q.state
    want = torch.tensor([[0.], [1.]])
    assert(torch.equal(got, want))


def test_rnot_gate():
    q = qubit()
    q.rnot(0).rnot(0)
    got = q.state
    want = torch.tensor([[0.], [1.]])
    assert(torch.equal(got, want))


def test_y_gate():
    # Test case 1 (on state [1, 0])
    q = qubit()
    q.y(0)
    got = q.state
    want = torch.tensor([[0.], [1.j]])
    assert(torch.equal(got, want))

    # Test case 2 (on state [0, 1])
    q = qubit()
    q.x(0).y(0)
    got = q.state
    want = torch.tensor([[-1.j], [0.]])
    assert(torch.equal(got, want))


def test_z_gate():
    # Test case 1 (on state [1, 0])
    q = qubit()
    q.z(0)
    got = q.state
    want = torch.tensor([[1.], [0.]])
    assert(torch.equal(got, want))

    # Test case 2 (on state [0, 1])
    q = qubit()
    q.x(0).z(0)
    got = q.state
    want = torch.tensor([[0.], [-1.]])
    assert(torch.equal(got, want))


def test_h_gate():
    # Test case 1 (on state [1, 0])
    q = qubit()
    q.h(0)
    got = q.state
    want = torch.tensor([[1. / math.sqrt(2)], [1. / math.sqrt(2)]])
    assert(torch.equal(got, want))

    # Test case 2 (on state [0, 1])
    q = qubit()
    q.x(0).h(0)
    got = q.state
    want = torch.tensor([[1. / math.sqrt(2)], [-1. / math.sqrt(2)]])
    assert(torch.equal(got, want))


def test_s_gate():
    # Test case 1 (on state [1, 0])
    q = qubit()
    q.s(0)
    got = q.state
    want = torch.tensor([[1.], [0.]])
    assert(torch.equal(got, want))

    # Test case 2 (on state [0, 1])
    q = qubit()
    q.x(0).s(0)
    got = q.state
    want = torch.tensor([[0.], [1.j]])
    assert(torch.allclose(got, want))


def test_t_gate():
    # Test case 1 (on state [1, 0])
    q = qubit()
    q.t(0)
    got = q.state
    want = torch.tensor([[1.], [0.]])
    assert(torch.equal(got, want))

    # Test case 2 (on state [0, 1])
    q = qubit()
    q.x(0).t(0)
    got = q.state
    want = torch.tensor([[0.], [torch.exp(1.j * torch.pi / 4)]])
    assert(torch.equal(got, want))


def test_phase_gate():
    # Test case 1 (pi/2, S gate)
    q = qubit()
    q.x(0).phase(deg=90, idx=0)
    got = q.state
    want = torch.tensor([[0.], [1.j]])
    assert(torch.allclose(got, want))

    # Test case 2 (pi/4, T gate)
    q = qubit()
    q.x(0).phase(deg=45, idx=0)
    got = q.state
    want = torch.tensor([[0.], [torch.exp(1.j * torch.pi / 4)]])
    assert(torch.equal(got, want))


def test_dagger_gates():
    # Test case 1 (s dagger)
    q = qubit()
    q.s(0).s_dg(0)
    got = q.state
    want = torch.tensor([[1.], [0.]])
    assert(torch.equal(got, want))

    # Test case 2 (t dagger)
    q = qubit()
    q.t(0).t_dg(0)
    got = q.state
    want = torch.tensor([[1.], [0.]])
    assert(torch.equal(got, want))

    # Test case 3 (phase dagger)
    q = qubit()
    q.phase(deg=30, idx=0).phase_dg(deg=30, idx=0)
    got = q.state
    want = torch.tensor([[1.], [0.]])
    assert(torch.equal(got, want))


def test_measure():
    # Test case 1 (on state [1, 0])
    q = qubit()
    got = q.measure(0)
    want = 0
    assert(got == want)

    # Test case 2 (on state [1, 0])
    q = qubit()
    got = q.x(0).measure(0)
    want = 1
    assert(got == want)

    # Test case 3 (on superposition)
    q = qubit()
    want = q.h(0).measure(0)
    for _ in range(100):
        got = q.measure(0)
        assert(got == want)
