import pytest
import numpy as np
from willard.type import qreg


def test_init_qreg():
    from willard.type import qubit, qucrumb
    got = qreg(1)
    want = qubit()
    assert(np.array_equal(got.state, want.state))

    got = qreg(2)
    want = qucrumb()
    assert(np.array_equal(got.state, want.state))

    with pytest.raises(ValueError):
        qreg(0)

    with pytest.raises(ValueError):
        qreg(-1)
