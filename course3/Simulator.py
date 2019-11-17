class Simulator:
    time = 0
    event_list=[]

    def now(self):
        return self.time

    def insertEv(self,ev):
        self.event_list.ins(ev)

    def doAllEvents(self):
        ev = self.event_list.removefirst()
        while ev is not None:
            self.time = ev.time
            ev.execute(self)
            ev = self.event_list.removefirst()

