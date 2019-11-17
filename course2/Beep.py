from Event import Event


class Beep(Event):
    def __init__(self, time):
        self.time = time

    def execute(self, sim):
        print('The time is %fs' % sim.time )
