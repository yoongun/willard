import pytest
from willard.type import qreg


def test_inc():
    qr = qreg(3)
    q = qr.int(3, 0)
    q.inc()
    got = q.measure_all()
    want = 1
    assert(got == want)

    q.inc()
    q.inc()
    got = q.measure_all()
    want = 3
    assert(got == want)


def test_dec():
    qr = qreg(3)
    q = qr.int(3, 7)
    q.dec()
    got = q.measure_all()
    want = 6
    assert(got == want)

    q.dec()
    q.dec()
    got = q.measure_all()
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
