from willard.type import qreg


# def test_teleportation():
#     q = qreg(3)
#     q.x(0)
#     q.h(0).phase(idx=0, deg=45).h(0)
#     q.teleport(a=0, ch=1, b=2)
#     q.h(2).phase(deg=-45, idx=2).h(2)
#     got = q.measure(2)
#     want = 1
#     assert(got == want)

#     q = qreg(3)
#     q.x(1)
#     q.h(1).phase(idx=1, deg=45).h(1)
#     q.teleport(a=1, ch=2, b=0)
#     q.h(0).phase(deg=-45, idx=0).h(0)
#     got = q.measure(0)
#     want = 1
#     assert(got == want)
def test_teleportation():
    qr = qreg(3)
    alice = qr.int(1)
    channel = qr.int(1)
    bob = qr.int(1)

    # Preparing payload
    alice.x(0).h(0).phase(45, 0).h(0)

    # Send
    channel.h(0)
    qr.cx(channel[0], bob[0])
    qr.cx(alice[0], channel[0])
    alice.h(0)
    a_result = alice.measure(0)
    ch_result = channel.measure(0)

    # Resolve
    if ch_result:
        bob.x(0)
    if a_result:
        bob.phase(180, 0)

    # Verify
    bob.h(0).phase(-45, 0).h(0)
    result = bob.measure(0)

    assert(result == 1)
