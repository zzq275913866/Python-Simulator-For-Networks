import abc


class Event:
    time = 0

    def lt(self, obj2):
        return (self.time <= obj2.time)

    @abc.abstractmethod
    def execute(self, sim):
        pass
