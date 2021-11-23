import pytest
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

    with pytest.raises(AttributeError):
        qr = qreg(4)
        x = qr.bits('00')
        y = qr.bits('00')
        assert(alg.deutsch(x, y, balanced))


def test_deutsch_jozsa():
    qr = qreg(4)
    x = qr.bits('000')
    y = qr.bits('0')

    # Case 1: Balanced
    def balanced(x, y):
        x[0].cx(y[:])
    assert(alg.deutsch_jozsa(x, y, balanced))

    # Case 2: Constant-1
    qr.reset()

    def constant1(x, y):
        y.x()
    assert(not alg.deutsch_jozsa(x, y, constant1))

    # Case 3: Constant-2
    def constant2(x, y):
        y.h().z()
    assert(not alg.deutsch_jozsa(x, y, constant2))

    with pytest.raises(AttributeError):
        qr = qreg(4)
        x = qr.bits('00')
        y = qr.bits('00')
        assert(alg.deutsch_jozsa(x, y, balanced))


def test_bernstein_vazirani():
    qr = qreg(4)
    x = qr.bits('000')
    y = qr.bits('0')

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
    got = alg.bv(x, y, s_101)
    want = '101'
    assert(got == want)


def test_simon():
    qr = qreg(4)
    x = qr.bits('00')
    y = qr.bits('00')

    def period_11(x, y):
        x[0].cx(y[0]).cx(y[1])
        x[1].cx(y[0]).cx(y[1])
    alg.simon(x, y, period_11)
    got = x.measure()
    want1 = '00'
    want2 = '11'
    assert(got == want1 or got == want2)


def test_shor():
    pass


def test_grover():
    # qr = qreg(3)
    # q = qr.bits('000')
    # q.grover(oracle1)

    # qr.reset()
    # q.grover(oracle2)
    pass
