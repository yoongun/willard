from willard.util import slice_to_range


def test_slice_to_range():
    got = slice_to_range(slice(0, 10, 1), 10)
    wanted = range(0, 10, 1)

    assert(got == wanted)
