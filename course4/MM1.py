import random
import bisect


class EventList:
    elements = []

    def ins(self, x):
        bisect.insort(self.elements, x)

    def remove_first(self):
        if len(self.elements) == 0:
            return
        ev = self.elements.pop(0)
        return ev


class Simulator:
    time = 0
    sim_limit = 0
    event_list = ()

    def now(self):
        return self.time

    def insert_ev(self, ev):
        self.event_list.ins(ev)

    def do_all_events(self):
        ev = self.event_list.remove_first()
        while ev is not None:
            self.time = ev.time
            if self.time > self.sim_limit:
                break
            ev.execute(self)
            ev = self.event_list.remove_first()


class Packet:
    created = ''
    sent = ''

    def __init__(self, created):
        self.created = created


class GenePoisEv:
    time = 0
    q = ()

    def __lt__(self, obj2):
        return self.time <= obj2.time

    def execute(self, sim):
        packet = Packet(self.time)
        self.q.insert_q(packet, sim)

        inter_arrival_time = random.expovariate(0.2)
        self.time = self.time + inter_arrival_time
        sim.insert_ev(self)


class Que:
    que = []
    s = ()

    def insert_q(self, packet, sim):
        if self.s.packetBeingServed is None:
            self.s.insert_server(packet, sim)
        else:
            self.que.append(packet)

    def remove(self):
        pac = self.que.pop(0)
        return pac


class ServExpEv:
    doc = open('out.txt', 'w')
    packetBeingServed = None
    time = 0
    q = ()

    def __lt__(self, obj2):
        return self.time <= obj2.time

    def execute(self, sim):
        soj_t = self.time - self.packetBeingServed.created
        print('%f\n' % soj_t)
        print('%f' % soj_t, file=self.doc)
        self.packetBeingServed = None

        if len(self.q.que) != 0:
            packet = self.q.remove()
            self.insert_server(packet, sim)

    def insert_server(self, packet, sim):
        self.packetBeingServed = packet
        service_time = random.expovariate(1)
        self.time = sim.now() + service_time
        sim.insert_ev(self)
