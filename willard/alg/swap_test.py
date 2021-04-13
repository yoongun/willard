from willard.type import qreg


def swap_test(q: qreg, *, input1: int, input2: int, output: int) -> qreg:
    """
    0 if input1 != input2
    1 if input1 == input2
    1 or 0 when input1 and input2 resembles
    """
    q.h(output)
    q.cswap(c=output, d1=input1, d2=input2)
    q.h(output)
    q.x(output)
    result = q.measure(output)
    return result
