from Simulator import Simulator
from Beep import Beep


sim = Simulator()

sim.insert_ev(Beep(4.0))

sim.insert_ev(Beep(6.0))

sim.insert_ev(Beep(6.2))

sim.insert_ev(Beep(5))

sim.insert_ev(Beep(2))

sim.insert_ev(Beep(1))

sim.do_all_events()
