import numpy as np


class rsa:
    def __init__(self, p, q) -> None:
        if not self._is_prime(p) or not self._is_prime(q):
            raise ValueError("p, q should be a prime number.")
        self.n = p * q
        self.phi = (p - 1) * (q - 1)
        self.e = max(self.coprimes(self.phi))
        self.d = self.modinv(self.e, self.phi)
        self.public_key = (self.e, self.n)
        self.private_key = (self.d, self.n)

    def _is_prime(self, a):
        if a == 2:
            return True
        elif a < 2 or a % 2 == 0:
            return False
        elif a > 2:
            for i in range(3, int(np.sqrt(a)) + 1, 2):
                if a % i == 0:
                    return False
        return True

    def coprimes(self, a):
        l = []
        for x in range(2, a):
            if self.gcd(a, x) == 1 and self.modinv(x, self.phi) is not None:
                l.append(x)
        for x in l:
            if x == self.modinv(x, self.phi):
                l.remove(x)
        return l

    def gcd(self, a, b):
        while b != 0:
            c = a % b
            a = b
            b = c
        return a

    def modinv(self, a, m):
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return None

    def encrypt_block(self, m):
        c = self.modinv(m ** self.e, self.n)
        if c is None:
            print('No modular multiplicative inverse for block ' + str(m) + '.')
        return c

    def decrypt_block(self, c):
        m = self.modinv(c ** self.d, self.n)
        if m is None:
            print('No modular multiplicative inverse for block ' + str(c) + '.')
        return m

    def encrypt(self, s):
        return ''.join([chr(self.encrypt_block(ord(x))) for x in list(s)])

    def decrypt(self, s):
        return ''.join([chr(self.decrypt_block(ord(x))) for x in list(s)])
