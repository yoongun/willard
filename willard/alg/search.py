import math
import random
from willard.type import qreg
from willard.type import qbits
from willard.const import GateType
import numpy as np


def deutsch(x: qbits, y: qbits, f):
    if len(x) != 1 or len(y) != 1:
        raise AttributeError(
            f"Length of x and y should be 1. Given x: {len(x)}, y: {len(y)}")
    x.h()
    y.x().h()
    f(x, y)
    x.h()
    return bool(int(x.measure(), 2))


def deutsch_jozsa(x: qbits, y: qbits, f):
    if len(y) != 1:
        raise AttributeError(
            f"Length of y should be 1. Given y: {len(y)}")
    x.h()
    y.x().h()
    f(x, y)
    x.h()
    return bool(int(x.measure(), 2))


def bv(x: qbits, y: qbits, f: GateType):
    """
    bernstein vazirani
    """
    x.h()
    y.h().z()
    f(x, y)
    x.h()
    return x.measure()


def simon(x: qbits, y: qbits, f: GateType):
    if len(x) != len(y):
        raise AttributeError(
            f"The length of x and y should be equal. Got x: {len(x)}, y: {len(y)}.")
    x.h()
    f(x, y)
    y.measure()
    x.h()


def shor2(N):
    attempts = 0
    while attempts < 100:
        a = 2
        # a = random.randint(2, N - 1)
        # k = math.gcd(a, N)
        # if k != 1:
        #     return k

        # Period finding
        qr = qreg()
        x = qr.uint(4)
        y = qr.bits(4, '0001')
        x.h()
        for i in range(len(x)):
            for _ in range(2 ** i):
                x[i].cswap(y[2], y[3])
                x[i].cswap(y[1], y[2])
                x[i].cswap(y[0], y[1])
        x.invqft()
        r = x.measure()

        if r % 2 != 0:
            attempts += 1
            continue
        if (a ** (r // 2)) % N == N - 1:
            attempts += 1
            continue
        if r == 0:
            attempts += 1
            continue
        r = r // 2
        cand1 = math.gcd(a ** r - 1, N)
        cand2 = math.gcd(a ** r + 1, N)
        if cand1 == 1 or cand2 == 1:
            attempts += 1
            continue
        return sorted((cand1, cand2))


def grover(x: qbits, f: GateType):
    x.h()
    rep = round(np.sqrt(len(x)) * np.pi / 4)

    for _ in range(rep):
        f(x)
        x.aa()
    return int(x.measure(), 2)
