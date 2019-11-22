from ArrivalGenerator import ArrivalGenerator
from Simulator import Simulator
import random

random.seed(1)

sim = Simulator()

t = random.expovariate(100)

sim.insert_ev(ArrivalGenerator(t))

sim.do_all_events()
