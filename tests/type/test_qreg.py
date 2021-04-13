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
