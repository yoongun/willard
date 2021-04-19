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


def test_add():
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
