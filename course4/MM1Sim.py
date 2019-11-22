from MM1 import *


random.seed(1)

doc = open('out.txt', 'w')

sim = Simulator()
sim.event_list = EventList()
sim.sim_limit = 10000

g = GenePoisEv()
q = Que()
s = ServExpEv()

g.q = q
q.s = s
s.q = q

g.time = 2
sim.insert_ev(g)

sim.do_all_events()
doc.close()
