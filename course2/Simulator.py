from EventList import EventList


class Simulator:
    time = 0
    event_list = EventList()

    def now(self):
        return self.time

    def insert_ev(self, ev):
        self.event_list.ins(ev)

    def do_all_events(self):
        ev = self.event_list.remove_first()
        while ev is not None:
            self.time = ev.time
            ev.execute(self)
            ev = self.event_list.remove_first()
