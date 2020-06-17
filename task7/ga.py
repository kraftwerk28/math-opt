class GenAlg(object):
    def __init__(self):
        self._numarray = [random.randint(1, 100) for _ in range(100)]

    def population(self):
        for i, el in enumerate(self._numarray):
            self._numarray[i] += random.randint(-1, 1)

    def selection(self):
        self._numarray.sort()
        ln = self._numarray.__len__()
        self._numarray = self._numarray[ln // 2:] + self._numarray[ln // 2:]

    def print_gen(self):
        print(self._numarray)

    def start(self):
        for _ in range(10):
            self.print_gen()
            self.population()
            self.selection()
        print('Final solution:')
        self.print_gen()

