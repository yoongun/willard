from willard.type import qint, qreg


def teleport(qr: qreg, alice: qint, channel: qint, bob: qint):
    if qr != alice.qreg or qr != channel.qreg or qr != bob.qreg:
        raise ValueError(
            "alice, channel, bob should be in the qreg passed with.")
    # Preparing payload
    alice.h(0).phase(45, 0).h(0)

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
