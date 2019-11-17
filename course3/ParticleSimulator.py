from RadioactiveParticle import RadioactiveParticle
from Simulator import Simulator
from EventList import EventList
import random

random.seed(1)

sim = Simulator()
sim.event_list = EventList()

sim.insertEv(RadioactiveParticle(random.expovariate(2)))
sim.insertEv(RadioactiveParticle(random.expovariate(2)))
sim.insertEv(RadioactiveParticle(random.expovariate(2)))
sim.insertEv(RadioactiveParticle(random.expovariate(2)))

sim.doAllEvents()
