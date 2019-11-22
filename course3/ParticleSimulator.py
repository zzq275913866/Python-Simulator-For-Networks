from RadioactiveParticle import RadioactiveParticle
from Simulator import Simulator
import random

random.seed(1)

sim = Simulator()

for i in range(4):
    sim.insert_ev(RadioactiveParticle(random.expovariate(2)))

sim.do_all_events()
