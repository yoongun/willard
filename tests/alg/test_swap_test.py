from willard.type import qreg
from willard.alg.swap_test import swap_test


def test_swap_test():
    q = qreg(3)
    swap_test(q, input1=0, input2=1, output=2)
    assert(q.measure(2) == 1)

    q = qreg(3)
    q.x(0)
    swap_test(q, input1=0, input2=1, output=2)
    assert(q.measure(2) == 0)

    q = qreg(3)
    q.h(0).h(1)
    swap_test(q, input1=0, input2=1, output=2)
    assert(q.measure(2) == 1)

    q = qreg(3)
    q.x(0).h(1)
    swap_test(q, input1=0, input2=1, output=2)
    assert(q.measure(2) == 0)
