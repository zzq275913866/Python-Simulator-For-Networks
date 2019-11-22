from Counter import Counter
from Simulator import Simulator

sim = Simulator()

sim.insert_ev(Counter(0))

sim.do_all_events()
