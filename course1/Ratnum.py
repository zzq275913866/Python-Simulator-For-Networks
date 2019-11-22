class Ratnum:
    n = ''
    d = ''

    def __init__(self, numerator, denomenator):
        self.n = numerator
        self.d = denomenator

    def display(self):
        if self.d != 1:
            print('%d/%d\n' % (self.n, self.d))
        else:
            print('%d\n' % self.n)

    def add(self, r1, r2):
        self.n = r1.n * r2.d + r2.n * r1.d
        self.d = r1.d * r2.d

    def get_n(self):
        return self.n

    def set_n(self, num):
        self.n = num


if __name__ == '__main__':
    a = Ratnum(1, 2)
    b = Ratnum(3, 4)
    c = Ratnum(5, 6)
    c.display()
    c.add(a, b)
    c.display()
