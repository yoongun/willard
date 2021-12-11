import numpy as np


class rsa:
    def __init__(self, p, q) -> None:
        if not self._is_prime(p) or not self._is_prime(q):
            raise ValueError("p, q should be a prime number.")
        self.n = p * q
        self.phi = (p - 1) * (q - 1)
        self.e = max(self._coprimes(self.phi))
        self.d = self._modinv(self.e, self.phi)
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

    def _coprimes(self, a):
        l = []
        for x in range(2, a):
            if self._gcd(a, x) == 1 and self._modinv(x, self.phi) is not None:
                l.append(x)
        for x in l:
            if x == self._modinv(x, self.phi):
                l.remove(x)
        return l

    def _gcd(self, a, b):
        while b != 0:
            c = a % b
            a = b
            b = c
        return a

    def _modinv(self, a, n):
        for x in range(1, n):
            if (a * x) % n == 1:
                return x
        return None

    def _encrypt_block(self, m):
        c = self._modinv(m ** self.e, self.n)
        if c is None:
            print('No modular multiplicative inverse for block ' + str(m) + '.')
        return c

    def _decrypt_block(self, c):
        m = self._modinv(c ** self.d, self.n)
        if m is None:
            print('No modular multiplicative inverse for block ' + str(c) + '.')
        return m

    def encrypt(self, s):
        return ''.join([chr(self._encrypt_block(ord(x))) for x in list(s)])

    def decrypt(self, s):
        return ''.join([chr(self._decrypt_block(ord(x))) for x in list(s)])
