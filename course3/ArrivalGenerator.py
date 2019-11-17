from Event import Event
import random


class ArrivalGenerator(Event):
    def __init__(self, time):
        self.time = time

    def execute(self, sim):
        print('An arrival at t = %f s' % sim.time)
        if (self.time < 100):
            self.time = sim.now() + random.expovariate(100)
            sim.insertEv(self)
