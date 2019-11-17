class ratnum:
    _n = ''
    _d = ''

    def __init__(self, numerator, denomenator):
        self._n = numerator
        self._d = denomenator

    def disp(self):
        if(self._d != 1):
            print('%d/%d\n' %(self._n, self._d))
        else:
            print('%d\n' % self._n)

    def add(self, r1, r2):
         self._n = r1._n * r2._d + r2._n * r1._d
         self._d = r1._d * r2._d

    def getn(self):
        return self._n

    def setn(self, num):
        self._n = num
