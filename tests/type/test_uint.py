import pytest
from willard.type import qreg


@pytest.fixture
def qr():
    return qreg()


def test_inc(qr):
    q = qr.uint(3)
    q.inc()
    got = q.measure()
    want = 1
    assert(got == want)

    q.inc(2)
    got = q.measure()
    want = 3
    assert(got == want)


def test_dec(qr):
    q = qr.uint(3, 7)
    q.dec()
    got = q.measure()
    want = 6
    assert(got == want)

    q.dec(2)
    got = q.measure()
    want = 4
    assert(got == want)


# def test_add(qr):
#     q1 = qr.uint(3, 3)
#     q2 = qr.uint(3, 4)
#     q1.add(q2)
#     got = q1.measure()
#     want = 7
#     assert(got == want)

#     qr.reset()
#     q1 = qr.uint(3, 4)
#     q2 = qr.uint(3, 1)
#     q1.add(q2)
#     got = q1.measure()
#     want = 5
#     assert(got == want)


# def test_sub(qr):
#     q1 = qr.uint(3, 5)
#     q2 = qr.uint(3, 1)
#     q1.sub(q2)
#     got = q1.measure()
#     want = 4
#     assert(got == want)

#     qr.reset()
#     q1 = qr.uint(3, 2)
#     q2 = qr.uint(3, 2)
#     q1.add(q2)
#     got = q1.measure()
#     want = 0
#     assert(got == want)

#     qr.reset()
#     q1 = qr.uint(3, 3)
#     q2 = qr.uint(3, 7)
#     q1.add(q2)
#     got = q1.measure()
#     want = 0
#     assert(got == want)
