from Event import Event


class RadioactiveParticle(Event):
    def __init__(self, time):
        self.time = time

    def execute(self, sim):
        print('A particle at t = %fs' % sim.time)
