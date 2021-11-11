from willard.type import quint, qreg


def teleport(alice: quint, channel: quint, bob: quint):
    # Preparing payload
    alice[0].h().phase(45).h()

    # Send
    channel[0].h().cx(bob[0])
    alice[0].cx(channel[0])
    alice[0].h()
    a_result = alice[0].measure()
    ch_result = channel[0].measure()

    # Resolve
    if ch_result:
        bob[0].x()
    if a_result:
        bob[0].phase(180)

    # Verify
    bob[0].h().phase(-45).h()
