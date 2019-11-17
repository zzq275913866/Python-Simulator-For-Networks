from ArrivalGenerator import ArrivalGenerator
from Simulator import Simulator
from EventList import EventList
import random

random.seed(1)

sim = Simulator()
sim.event_list = EventList()
t = random.expovariate(100)
sim.insertEv(ArrivalGenerator(t))
sim.doAllEvents()
