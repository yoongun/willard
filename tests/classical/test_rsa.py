import pytest
from willard.classical import rsa


def test_rsa():
    crypto = rsa(p=13, q=17)
    encrypted = crypto.encrypt("Message.")
    got = crypto.decrypt(encrypted)
    wanted = "Message."
    assert(got == wanted)

    with pytest.raises(ValueError):
        crypto = rsa(p=15, q=18)
