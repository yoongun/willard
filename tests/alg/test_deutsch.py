from willard.type import qreg
from willard import alg


def test_deutsch():
    qr = qreg(2)
    x = qr.bits('0')
    y = qr.bits('0')

    # Case 1: Balanced
    def balanced(x, y):
        x.cx(y)
    assert(alg.deutsch(x, y, balanced))

    # Case 2: Constant-1
    qr.reset()

    def constant1(x, y):
        y.x()
    assert(not alg.deutsch(x, y, constant1))

    # Case 3: Constant-2
    def constant2(x, y):
        x.x()
    assert(not alg.deutsch(x, y, constant2))
