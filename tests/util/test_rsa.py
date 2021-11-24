import pytest
from willard.util import rsa


def test_rsa():
    crypto = rsa(p=13, q=17)
    encrypted = crypto.encrypt("Message.")
    got = crypto.decrypt(encrypted)
    want = "Message."
    assert(got == want)

    with pytest.raises(ValueError):
        crypto = rsa(p=15, q=18)
