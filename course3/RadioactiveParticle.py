class RadioactiveParticle:
    def __init__(self, time):
        self.time = time

    def __lt__(self, obj2):
        return self.time <= obj2.time

    @staticmethod
    def execute(sim):
        print('A particle at t = %fs' % sim.time)
