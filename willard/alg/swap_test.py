from willard.type import qreg, quint


def swap_test(input1: quint, input2: quint, output: quint):
    """
    0 or 1 with 0.5 probability if input1 != input2
    1 if input1 == input2
    """
    output[0].h()
    output[0].cswap(input1[0], input2[0])
    output[0].h()
    output[0].x()
