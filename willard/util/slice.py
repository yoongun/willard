

def slice_to_range(s: slice, max_size: int):
    indices = s.indices(max_size)
    return range(indices[0], indices[1], indices[2])
