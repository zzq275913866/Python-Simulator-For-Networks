from Event import Event


class Counter(Event):
    def __init__(self, time):
        self.time = time

    def execute(self, sim):
        print('The time is %f'% sim.time)

        if (self.time < 10):
            self.time = self.time + 2
            sim.insertEv(self)
