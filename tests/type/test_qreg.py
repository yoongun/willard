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
    want = state.ket('001')
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
