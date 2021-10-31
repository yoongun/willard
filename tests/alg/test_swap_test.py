from willard.type import qreg, quint
from willard.alg.swap_test import swap_test


def test_swap_test():
    qr = qreg(3)
    input1 = qr.int(1, 0)
    input2 = qr.int(1, 0)
    output = qr.int(1, 0)
    swap_test(qr, input1, input2, output)
    assert(output.measure(0) == 1)

    # Test probability??
    # qr = qreg(3)
    # input1 = qr.int(1, 1)
    # input2 = qr.int(1, 0)
    # output = qr.int(1, 0)
    # swap_test(qr, input1, input2, output)
    # assert(output.measure(0) == 0)
