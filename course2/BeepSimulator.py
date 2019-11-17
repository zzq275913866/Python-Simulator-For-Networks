from Beep import Beep
from EventList import EventList
from Simulator import Simulator

sim = Simulator()

sim.event_list = EventList()

sim.insertEv(Beep(4.0))

sim.insertEv(Beep(6.0))

sim.insertEv(Beep(6.2))

sim.insertEv(Beep(5))

sim.insertEv(Beep(2))

sim.insertEv(Beep(1))

sim.doAllEvents()