from willard.type import qtype


class qbits(qtype):
    def __init__(self, qr, offset: int, init_value: str):
        super(qbits, self).__init__()
        self.qr = qr
        self.size = len(init_value)
        self.offset = offset

        init_value_rev = init_value[::-1]
        for i, elem in enumerate(init_value_rev):
            if elem == '1':
                self[i].x()
            elif elem != '0':
                raise ValueError('init_value should contain 0 or 1 only')

    def measure(self):
        result = ''
        for i in range(self.size):
            result = str(self[i].measure()[0]) + result
        return result
