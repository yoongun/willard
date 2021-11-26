import pytest
from willard.type import qreg
from willard import alg


def test_deutsch():
    qr = qreg()
    x = qr.bits(1)
    y = qr.bits(1)

    # Case 1: Balanced
    def balanced(x, y):
        x.cx(y)
    assert(alg.deutsch(x, y, balanced))

    # Case 2: Constant-1
    qr.reset()
    x = qr.bits(1)
    y = qr.bits(1)

    def constant1(x, y):
        y.x()
    assert(not alg.deutsch(x, y, constant1))

    # Case 3: Constant-2
    qr.reset()
    x = qr.bits(1)
    y = qr.bits(1)

    def constant2(x, y):
        x.x()
    assert(not alg.deutsch(x, y, constant2))

    with pytest.raises(AttributeError):
        qr = qreg()
        x = qr.bits(2)
        y = qr.bits(2)
        assert(alg.deutsch(x, y, balanced))


def test_deutsch_jozsa():
    qr = qreg()
    x = qr.bits(3)
    y = qr.bits(1)

    # Case 1: Balanced
    def balanced(x, y):
        x[0].cx(y[:])
    assert(alg.deutsch_jozsa(x, y, balanced))

    # Case 2: Constant-1
    qr.reset()
    x = qr.bits(3)
    y = qr.bits(1)

    def constant1(x, y):
        y.x()
    assert(not alg.deutsch_jozsa(x, y, constant1))

    # Case 3: Constant-2
    qr.reset()
    x = qr.bits(3)
    y = qr.bits(1)

    def constant2(x, y):
        y.h().z()
    assert(not alg.deutsch_jozsa(x, y, constant2))

    with pytest.raises(AttributeError):
        qr = qreg()
        x = qr.bits(2)
        y = qr.bits(2)
        assert(alg.deutsch_jozsa(x, y, balanced))


def test_bernstein_vazirani():
    qr = qreg()
    x = qr.bits(3)
    y = qr.bits(1)

    def s_011(x, y):
        x[0].cx(y[0])
        x[1].cx(y[0])
    got = alg.bv(x, y, s_011)
    want = '011'
    assert(got == want)

    def s_101(x, y):
        x[0].cx(y[0])
        x[2].cx(y[0])
    qr.reset()
    x = qr.bits(3)
    y = qr.bits(1)
    got = alg.bv(x, y, s_101)
    want = '101'
    assert(got == want)


def test_simon():
    qr = qreg()
    x = qr.bits(2)
    y = qr.bits(2)

    def period_11(x, y):
        x[0].cx(y[0]).cx(y[1])
        x[1].cx(y[0]).cx(y[1])
    alg.simon(x, y, period_11)
    got = x.measure()
    want1 = '00'
    want2 = '11'
    assert(got == want1 or got == want2)


def test_shor():
    got = alg.shor2(15)
    want = (3, 5)

    assert(got == want)


def test_grover():
    qr = qreg()
    q = qr.bits(4)

    def flip3(x):
        x.flip(3)
    got = alg.grover(q, flip3)
    want = 3
    assert(got == want)

    def flip6(x):
        x.flip(6)
    qr.reset()
    q = qr.bits(4)
    got = alg.grover(q, flip6)
    want = 6
    assert(got == want)
