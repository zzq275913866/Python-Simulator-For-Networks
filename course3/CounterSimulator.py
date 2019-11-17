from Counter import Counter
from Simulator import Simulator
from EventList import EventList

sim = Simulator()
sim.event_list = EventList()
sim.insertEv(Counter(0))
sim.doAllEvents()
