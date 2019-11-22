import random


class ArrivalGenerator:
    def __init__(self, time):
        self.time = time

    def __lt__(self, obj2):
        return self.time <= obj2.time

    def execute(self, sim):
        print('An arrival at t = %f s' % sim.time)
        if self.time < 100:
            self.time = sim.now() + random.expovariate(100)
            sim.insert_ev(self)
