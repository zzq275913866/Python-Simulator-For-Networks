import abc
import random


class Event:
    time = 0

    def lt(self, obj2):
        return (self.time <= obj2.time)

    @abc.abstractmethod
    def execute(self, sim):
        pass


class EventList:
    elements = []

    def ins(self, x):
        i = 1
        length = len(self.elements)
        while (i <= length and (self.elements[i-1].time < x.time)):
            i = i + 1

        if len(self.elements) == 0:
            self.elements.append(x)
        else:
            self.elements.insert(i-1, x)

    def removefirst(self):

        if len(self.elements) == 0:
            ev = []
            return

        ev = self.elements[0]
        del self.elements[0]
        return ev


class GenePoisEv(Event):
    q = []

    def execute(self, sim):
        packet = Packet(self.time)
        self.q.insertQ(packet, sim)

        interarrivalTime = random.expovariate(0.2)
        self.time = self.time + interarrivalTime
        sim.insertEv(self)


class Packet:
    created = ''
    sent = ''
    delivd = ''

    def __init__(self, created):
        self.created = created


class Que:
    que = []
    s = []

    def insertQ(self, packet, sim):
        if self.s.packetBeingServed is None:
            self.s.insertServ(packet, sim)
        else:
            self.que.append(packet)

    def remove(self):
        pac = self.que[0]
        del self.que[0]
        return pac


class ServExpEv(Event):
    packetBeingServed = None
    q = []
    doc = ''

    def execute(self, sim):
        soj_t = self.time - self.packetBeingServed.created
        print('%f\n' % soj_t)
        print('%f' % soj_t, file=self.doc)

        self.packetBeingServed = None

        if len(self.q.que) != 0:
            packet = self.q.remove()
            self.insertServ(packet, sim)

    def insertServ(self, packet, sim):
        self.packetBeingServed = packet
        serviceTime = random.expovariate(1)
        self.time = sim.now() + serviceTime
        sim.insertEv(self)


class Simulator:
    time = 0
    sim_limit = ''
    event_list = []

    def now(self):
        return self.time

    def insertEv(self,ev):
        self.event_list.ins(ev)

    def doAllEvents(self):
        ev = self.event_list.removefirst()
        while ev is not None:
            self.time = ev.time

            if self.time > self.sim_limit:
                break

            ev.execute(self)
            ev = self.event_list.removefirst()
