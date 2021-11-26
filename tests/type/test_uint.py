import pytest
from willard.type import qreg


@pytest.fixture
def qr():
    return qreg()


def test_inc(qr):
    q = qr.uint(3)
    q.inc()
    got = q.measure()
    wanted = 1
    assert(got == wanted)

    q.inc(2)
    got = q.measure()
    wanted = 3
    assert(got == wanted)


def test_dec(qr):
    q = qr.uint(3, 7)
    q.dec()
    got = q.measure()
    wanted = 6
    assert(got == wanted)

    q.dec(2)
    got = q.measure()
    wanted = 4
    assert(got == wanted)


def test_add(qr):
    q1 = qr.uint(4, 3)
    q2 = qr.uint(4, 4)
    q1.add(q2)
    got = q1.measure()
    wanted = 7
    assert(got == wanted)

    qr.reset()
    q1 = qr.uint(3, 4)
    q2 = qr.uint(3, 1)
    q1.add(q2)
    got = q1.measure()
    wanted = 5
    assert(got == wanted)


# def test_sub(qr):
#     q1 = qr.uint(3, 5)
#     q2 = qr.uint(3, 1)
#     q1.sub(q2)
#     got = q1.measure()
#     wanted = 4
#     assert(got == wanted)

#     qr.reset()
#     q1 = qr.uint(3, 2)
#     q2 = qr.uint(3, 2)
#     q1.add(q2)
#     got = q1.measure()
#     wanted = 0
#     assert(got == wanted)

#     qr.reset()
#     q1 = qr.uint(3, 3)
#     q2 = qr.uint(3, 7)
#     q1.add(q2)
#     got = q1.measure()
#     wanted = 0
#     assert(got == wanted)
