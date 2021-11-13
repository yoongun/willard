import pytest
from willard.type import qreg


@pytest.fixture
def qr3():
    return qreg(3)


def test_inc(qr3):
    q = qr3.uint(3, 0)
    q.inc()
    got = q.measure()
    want = 1
    assert(got == want)

    q.inc()
    q.inc()
    got = q.measure()
    want = 3
    assert(got == want)


def test_dec(qr3):
    qr3 = qreg(3)
    q = qr3.uint(3, 7)
    q.dec()
    got = q.measure()
    want = 6
    assert(got == want)

    q.dec()
    q.dec()
    got = q.measure()
    want = 4
    assert(got == want)


# def test_add():
#     qr = qreg(6)
#     q1 = qr.int(3, 3)
#     q2 = qr.int(3, 4)
#     q1.add(q2)
#     got = q1.measure_all()
#     want = 7
#     assert(got == want)

#     qr = qreg(6)
#     q1 = qr.int(3, 4)
#     q2 = qr.int(3, 1)
#     q1.add(q2)
#     got = q1.measure_all()
#     want = 5
#     assert(got == want)