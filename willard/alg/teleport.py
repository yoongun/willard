from willard.type import qint


def teleport(self, alice: qint, channel: qint, bob: qint):
    # Preparing payload
    alice.h(0).phase(45, 0).h(0)

    # Send
    channel.h(0)
    self.cx(channel[0], bob[0])
    self.cx(alice[0], channel[0])
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
    self.h(channel).cx(c=channel, d=bob)
    self.cx(c=alice, d=channel).h(alice)
    a_result = self.measure(alice)
    ch_result = self.measure(channel)
    if ch_result:
        self.x(bob)
    if a_result:
        self.phase(deg=180, idx=bob)
    return self
