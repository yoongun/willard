import pytest
import numpy as np
from willard.type import qreg


def test_init_qreg():
    from willard.type import qubit, qucrumb
    got = qreg(1)
    wanted = qubit()
    assert(np.array_equal(got.state, wanted.state))

    got = qreg(2)
    wanted = qucrumb()
    assert(np.array_equal(got.state, wanted.state))

    with pytest.raises(ValueError):
        qreg(0)

    with pytest.raises(ValueError):
        qreg(-1)


# def test_x_gate():
#     # Case 1: Apply X gate on the first qubit
#     q = qreg(2)
#     q.x(0)
#     assert(np.array_equal(q.state, np.array([[0.], [1.], [0.], [0.]])))

#     # Case 2: Apply X gate on the second qubit
#     q = qreg(2)
#     q.x(1)
#     assert(np.array_equal(q.state, np.array([[0.], [0.], [1.], [0.]])))

#     # Checks whether the code checks index range
#     q = qreg(2)
#     with pytest.raises(IndexError):
#         q.x(2)


# def test_y_gate():
#     # Case 1: Apply Y gate on the first qubit
#     q = qreg(2)
#     q.y(0)
#     assert(np.array_equal(q.state, np.array([[0.], [1.j], [0.], [0.]])))

#     # Case 2: Apply Y gate on the second qubit
#     q = qreg(2)
#     q.y(1)
#     assert(np.array_equal(q.state, np.array([[0.], [0.], [1.j], [0.]])))

#     # Checks whether the code checks index range
#     q = qreg(2)
#     with pytest.raises(IndexError):
#         q.y(2)


# def test_z_gate():
#     # Case 1: Apply Z gate on the first qubit
#     q = qreg(2)
#     q.z(0)
#     assert(np.array_equal(q.state, np.array([[1.], [0.], [0.], [0.]])))

#     # Case 2: Apply Z gate on the second qubit
#     q = qreg(2)
#     q.z(1)
#     assert(np.array_equal(q.state, np.array([[1.], [0.], [0.], [0.]])))

#     # Checks whether the code checks index range
#     q = qreg(2)
#     with pytest.raises(IndexError):
#         q.z(2)


# def test_h_gate():
#     # Case 1: Apply H gate on the first qubit
#     q = qreg(2)
#     q.h(0)
#     assert(np.array_equal(q.state, np.array(
#         [[1. / np.sqrt(2)], [1. / np.sqrt(2)], [0.], [0.]])))

#     # Case 2: Apply H gate on the second qubit
#     q = qreg(2)
#     q.h(1)
#     assert(np.array_equal(q.state, np.array(
#         [[1. / np.sqrt(2)], [0.], [1. / np.sqrt(2)], [0.]])))

#     # Checks whether the code checks index range
#     q = qucrumb()
#     with pytest.raises(IndexError):
#         q.h(2)


# def test_s_gate():
#     # Case 1: Apply S gate on the first qubit
#     q = qreg(2)
#     q.s(0)
#     assert(np.array_equal(q.state, np.array([[1.], [0.], [0.], [0.]])))

#     # Case 2: Apply S gate on the second qubit
#     q = qreg(2)
#     q.s(1)
#     assert(np.array_equal(q.state, np.array([[1.], [0.], [0.], [0.]])))

#     # Checks whether the code checks index range
#     q = qucrumb()
#     with pytest.raises(IndexError):
#         q.z(2)


# def test_t_gate():
#     # Case 1: Apply S gate on the first qubit
#     q = qreg(2)
#     q.t(0)
#     assert(np.array_equal(q.state, np.array([[1.], [0.], [0.], [0.]])))

#     # Case 2: Apply S gate on the second qubit
#     q = qreg(2)
#     q.t(1)
#     assert(np.array_equal(q.state, np.array([[1.], [0.], [0.], [0.]])))

#     # Checks whether the code checks index range
#     q = qreg(2)
#     with pytest.raises(IndexError):
#         q.z(2)


# def test_cnot():
#     # Case 1: Test on the first qubit
#     q = qreg(2)
#     q.h(0).cnot(c=0, d=1)
#     assert(np.array_equal(q.state, np.array(
#         [[1. / np.sqrt(2)], [0.], [0.], [1. / np.sqrt(2)]])))

#     # Case 2: Test on the second qubit
#     q = qreg(2)
#     q.h(1).cnot(c=1, d=0)
#     assert(np.array_equal(q.state, np.array(
#         [[1. / np.sqrt(2)], [0.], [0.], [1. / np.sqrt(2)]])))

#     # Checks whether the code checks index range
#     q = qreg(2)
#     with pytest.raises(IndexError):
#         q.cnot(c=2, d=2)


# def test_swap():
#     # Case 1: From qubit0 to qubit1
#     q = qreg(2)
#     q.x(0).swap()
#     assert(np.array_equal(q.state, np.array(
#         [[0.], [0.], [1.], [0.]])))

#     # Case 1: From qubit1 to qubit0
#     q = qucrumb()
#     q.x(1).swap()
#     assert(np.array_equal(q.state, np.array(
#         [[0.], [1.], [0.], [0.]])))
