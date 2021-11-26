import pytest
import torch
from willard.const import GateBuilder


@pytest.fixture
def dev():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


@pytest.fixture
def gb2():
    gb2 = GateBuilder(2)
    return gb2


def test_build_x(gb2, dev):
    got = gb2.x(0)
    wanted = torch.tensor([[0., 1., 0., 0.],
                           [1., 0., 0., 0.],
                           [0., 0., 0., 1.],
                           [0., 0., 1., 0.]], dtype=torch.cfloat).to(dev)
    assert(torch.equal(got, wanted))

    got = gb2.x(1)
    wanted = torch.tensor([[0., 0., 1., 0.],
                           [0., 0., 0., 1.],
                           [1., 0., 0., 0.],
                           [0., 1., 0., 0.]], dtype=torch.cfloat).to(dev)
    assert(torch.equal(got, wanted))


def test_build_rnot(gb2, dev):
    got = torch.mm(gb2.rnot(0), gb2.rnot(0))
    wanted = gb2.x(0)
    assert(torch.equal(got, wanted))

    got = torch.mm(gb2.rnot(0), gb2.rnot(0))
    wanted = gb2.x(1)
    assert(torch.equal(got, wanted))


def test_build_y(gb2, dev):
    got = gb2.y(0)
    wanted = torch.tensor([[0.+0.j, 0.-1.j, 0.+0.j, 0.-0.j],
                           [0.+1.j, 0.+0.j, 0.+0.j, 0.+0.j],
                           [0.+0.j, 0.-0.j, 0.+0.j, 0.-1.j],
                           [0.+0.j, 0.+0.j, 0.+1.j, 0.+0.j]], dtype=torch.cfloat).to(dev)
    assert(torch.equal(got, wanted))

    got = gb2.y(1)
    wanted = torch.tensor([[0.+0.j, 0.+0.j, 0.-1.j, 0.-0.j],
                           [0.+0.j, 0.+0.j, 0.-0.j, 0.-1.j],
                           [0.+1.j, 0.+0.j, 0.+0.j, 0.+0.j],
                           [0.+0.j, 0.+1.j, 0.+0.j, 0.+0.j]], dtype=torch.cfloat).to(dev)
    assert(torch.equal(got, wanted))


def test_build_z(gb2):
    pass


def test_build_h(gb2):
    pass


def test_build_s(gb2, dev):
    got = gb2.s(0)
    wanted = torch.tensor([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                           [0.+0.j, 0.+1.j, 0.+0.j, 0.+0.j],
                           [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j],
                           [0.+0.j, 0.+0.j, 0.+0.j, 0.+1.j]]).to(dev)
    assert(torch.allclose(got, wanted))

    got = gb2.s(1)
    wanted = torch.tensor([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                           [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
                           [0.+0.j, 0.+0.j, 0.+1.j, 0.+0.j],
                           [0.+0.j, 0.+0.j, 0.+0.j, 0.+1.j]]).to(dev)
    assert(torch.allclose(got, wanted))


def test_build_t():
    pass


def test_build_phase():
    pass


def test_build_cu():
    pass


def test_build_cnot():
    pass


def test_build_swap():
    pass


def test_build_toffoli():
    pass
