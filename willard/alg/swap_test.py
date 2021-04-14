from willard.type import qreg, qint


def swap_test(qr: qreg, input1: qint, input2: qint, output: qint):
    """
    0 or 1 with 0.5 probability if input1 != input2
    1 if input1 == input2
    """
    output.h(0)
    qr.cswap(c=output[0], d1=input1[0], d2=input2[0])
    output.h(0)
    output.x(0)
