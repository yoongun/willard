class qint:
    def __init__(self, qreg, size: int, offset: int, init_value: int) -> None:
        self.qreg = qreg
        self.size = size
        self.offset = offset
        b = format(init_value, 'b')
        if len(b) > size:
            raise ValueError("init_value is bigger than the size of qint.")
        b_rev = b[::-1]
        for i, elem in enumerate(b_rev):
            if elem == '1':
                self.x(i)

    def __getitem__(self, idx):
        self._check_idx(idx)
        return self.offset + idx

    def x(self, idx):
        self._check_idx(idx)
        self.qreg.x(self.offset + idx)
        return self

    def rnot(self, idx):
        self._check_idx(idx)
        self.qreg.rnot(self.offset + idx)
        return self

    def y(self, idx):
        self._check_idx(idx)
        self.qreg.y(self.offset + idx)
        return self

    def z(self, idx):
        self._check_idx(idx)
        self.qreg.z(self.offset + idx)
        return self

    def h(self, idx):
        self._check_idx(idx)
        self.qreg.h(self.offset + idx)
        return self

    def s(self, idx):
        return self.phase(deg=90, idx=idx)

    def s_dg(self, idx):
        return self.phase_dg(deg=90, idx=idx)

    def t(self, idx):
        return self.phase(deg=45, idx=idx)

    def t_dg(self, idx):
        return self.phase_dg(deg=45, idx=idx)

    def phase(self, deg, idx):
        self._check_idx(idx)
        self.qreg.phase(deg, self.offset + idx)
        return self

    def phase_dg(self, *, deg, idx):
        return self.phase(deg=-deg, idx=idx)

    def measure(self, idx):
        self._check_idx(idx)
        return self.qreg.measure(self.offset + idx)

    def measure_all(self):
        result = ''
        for i in range(self.size):
            result.insert(0, self.qreg.measure(self.offset + i))
        return int(result, 2)

    def cu(self, *, c, d, u):
        """
        c: index of the condition qubit
        d: index of the destination qubit
        """
        self._check_idx(c)
        self._check_idx(d)
        if c == d:
            raise IndexError(f'Index ({c},{d}) is not valid')
        self.qreg.cu(c=self.offset + c, d=self.offset + d, u=u)
        return self

    def cx(self, c, d):
        """
        c: index of the condition qubit
        d: index of the destination qubit
        """
        return self.cu(c=c, d=d, u=gate.x)

    def cphase(self, deg, c, d):
        """
        c: index of the condition qubit
        d: index of the destination qubit
        """
        return self.cu(c=c, d=d, u=gate.phase(deg))

    def swap(self, c, d):
        self.cx(c, d).cx(d, c).cx(c, d)

    def toffoli(self, *, c1, c2, d):
        self._check_idx(c1)
        self._check_idx(c2)
        self._check_idx(d)
        if 3 > len(set([c1, c2, d])):
            raise IndexError(f'Index ({c1},{c2},{d}) is not valid')
        self.qreg.toffoli(c1=self.offset + c1,
                          c2=self.offset + c2, d=self.offset + d)
        return self

    def cswap(self, *, c, d1, d2):
        return self.toffoli(c1=c, c2=d1, d=d2).toffoli(c1=c, c2=d2, d=d1).toffoli(c1=c, c2=d1, d=d2)

    def swap_test(self, *, input1: int, input2: int, output: int):
        """
        0 if input1 != input2
        1 if input1 == input2
        1 or 0 when input1 and input2 resembles
        """
        self.h(output)
        self.cswap(c=output, d1=input1, d2=input2)
        self.h(output)
        self.x(output)
        return self

    def inc(self):
        pass

    def _check_idx(self, idx):
        if idx < 0 or idx >= self.size:
            raise IndexError(f'Index {idx} is out of the range')
