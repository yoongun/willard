from willard.type import qreg
from willard import alg


def test_simon():
    qr = qreg(4)
    x = qr.bits('00')
    y = qr.bits('00')

    def period_11(x, y):
        x[0].cx(y[0]).cx(y[1])
        x[1].cx(y[0]).cx(y[1])
    alg.simon(x, y, period_11)
    got = x.measure()
    want1 = '00'
    want2 = '11'
    assert(got == want1 or got == want2)
    
