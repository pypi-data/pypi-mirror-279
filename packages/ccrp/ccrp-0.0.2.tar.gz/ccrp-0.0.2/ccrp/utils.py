def split_two_bytes(n: int):
    assert n >= 0 and n < 65536
    nH = (n >> 8) & 0xFF
    nL = n & 0xFF
    return nH, nL
