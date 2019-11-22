class Counter:
    def __init__(self, time):
        self.time = time

    def __lt__(self, obj2):
        return self.time <= obj2.time

    def execute(self, sim):
        print('The time is %f' % sim.time)

        if self.time < 10:
            self.time = self.time + 2
            sim.insert_ev(self)
