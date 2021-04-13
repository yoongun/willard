from willard.type import qreg


def test_teleportation():
    q = qreg(3)
    q.x(0)
    q.h(0).phase(idx=0, deg=45).h(0)
    q.teleport(a=0, ch=1, b=2)
    q.h(2).phase(deg=-45, idx=2).h(2)
    got = q.measure(2)
    want = 1
    assert(got == want)

    q = qreg(3)
    q.x(1)
    q.h(1).phase(idx=1, deg=45).h(1)
    q.teleport(a=1, ch=2, b=0)
    q.h(0).phase(deg=-45, idx=0).h(0)
    got = q.measure(0)
    want = 1
    assert(got == want)
