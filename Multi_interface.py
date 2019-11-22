import random
import bisect
import heapq as hq


class EventList:
    elements = []

    def ins(self, x):
        bisect.insort(self.elements, x)

    def remove_first(self):
        if len(self.elements) == 0:
            return
        ev = self.elements.pop(0)
        return ev


class Node:
    doc = open('new_delay.txt', 'w')
    d = []
    weight_g = None
    node = None
    throughout = 0

    def __init__(self, _id):
        self.id = _id
        self.interface = {}
        self.rt = {}
        self.q = {}

    def handle_packet(self, packet, sim):
        if packet.dest == self.id:
            soj_t = sim.now() - packet.created
            a = [packet.srt, packet.dest, soj_t]
            # print('%f' % soj_t, file=self.doc)
            self.d.append(soj_t)
            Node.throughout += (packet.length/1000)
            print(a[0], a[1], a[2], file=self.doc)
        else:
            index = packet.path.index(self.id)
            # packet.length = random.expovariate(0.001)
            self.rt[packet.dest] = packet.path[index + 1]
            self.q[packet.path[index + 1]].insert_q(packet, sim)


class GenePoisEv:
    node = None
    weight_g = None
    next_node = None

    def __init__(self, _id, dest):
        self.id = _id
        self.dest = dest
        self.path = ''
        self.time = 0
        self.rate = 0

    def __lt__(self, obj2):
        return self.time <= obj2.time

    def execute(self, sim):
        packet = Packet(self.time)
        packet.srt = self.id
        # packet.srt = random.randint(1, len(self.node))
        packet.dest = self.dest
        packet.length = random.expovariate(0.001)
        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]  # 16条流产生的时间，在该时间重新计算路由
        if self.time in a:
            arr_rate = {}
            for i in self.weight_g:
                arr_rate[i] = {}
                for j in self.weight_g[i]:
                    arr_rate[i][j] = self.node[i].q[j].s.arr_rate + self.rate

            for i in self.weight_g:
                for j in self.weight_g[i]:
                    self.weight_g[i][j] = 1 / (self.node[i].q[j].s.bw / 1000 - arr_rate[i][j])

            r = {}
            for i in self.weight_g:
                dis = {i: 0}
                pre = {i: None}
                for j in self.weight_g:
                    if j != i:
                        dis[j] = float("inf")
                s = set()
                p_queue = []
                hq.heappush(p_queue, (0, i))
                while len(p_queue) > 0:
                    min_v = hq.heappop(p_queue)
                    dist = min_v[0]
                    u = min_v[1]
                    s.add(u)
                    adj_nodes = self.weight_g[u].keys()
                    for v in adj_nodes:
                        if v not in s:
                            if dist + self.weight_g[u][v] < dis[v]:
                                if (dis[v], v) not in p_queue:
                                    dis[v] = dist + self.weight_g[u][v]
                                    hq.heappush(p_queue, (dis[v], v))
                                else:
                                    index = p_queue.index((dis[v], v))
                                    dis[v] = dist + self.weight_g[u][v]
                                    p_queue[index] = (dis[v], v)
                                pre[v] = u

                path = {}
                for v in self.weight_g:
                    if v == i:
                        continue
                    path[v] = []

                for v in self.weight_g:
                    if v == i:
                        path[v] = v
                        continue
                    path[v].append(v)
                    parent = pre[v]
                    path[v].insert(0, parent)
                    while parent is not i:
                        parent = pre[parent]
                        path[v].insert(0, parent)
                r[i] = path

            # self.next_node = {}
            # for i in self.weight_g:
            #     self.next_node[i] = {}
            # for i in self.weight_g:
            #     for j in self.weight_g:
            #         p = P[i][j]
            #         if isinstance(p, int):
            #             self.next_node[i][j] = i
            #         else:
            #             self.next_node[i][j] = p[1]
            #
            # for i in self.weight_g:
            #     for j in self.weight_g:
            #         if i == j:
            #             self.node[i].rt[i] = 0
            #         else:
            #             self.node[i].rt[j] = self.next_node[i][j]

            p = r[self.id][self.dest]
            self.path = p
            for i in range(len(p) - 1):
                self.node[p[i]].q[p[i+1]].s.arr_rate += self.rate

        packet.path = self.path
        self.node[packet.srt].handle_packet(packet, sim)
        inter_arrival_time = random.expovariate(self.rate)
        self.time = self.time + inter_arrival_time
        sim.insert_ev(self)


class Packet:
    def __init__(self, created):
        self.created = created
        self.srt = ''
        self.dest = ''
        self.length = ''
        self.path = []


class Que:
    def __init__(self):
        self.que = []
        self.s = ''

    def insert_q(self, packet, sim):
        if self.s.packetBeingServed is None:
            self.s.insert_serv(packet, sim)
        else:
            self.que.append(packet)

    def remove(self):
        pac = self.que.pop(0)
        return pac


class ServExpEv:

    def __init__(self):
        self.packetBeingServed = None
        self.q = ''
        self.bw = 4 * (10**5)
        self.node = None
        self.arr_rate = 0
        self.time = 0

    def __lt__(self, obj2):
        return self.time <= obj2.time

    def execute(self, sim):
        sim.time = self.time
        self.node.handle_packet(self.packetBeingServed, sim)
        self.packetBeingServed = None

        if len(self.q.que) != 0:
            packet = self.q.remove()
            self.insert_serv(packet, sim)

    def insert_serv(self, packet, sim):
        self.packetBeingServed = packet
        service_time = self.packetBeingServed.length / self.bw
        self.time = sim.now() + service_time
        sim.insert_ev(self)


class Simulator:
    time = 0
    sim_limit = ''
    event_list = []

    def now(self):
        return self.time

    def insert_ev(self, ev):
        self.event_list.ins(ev)

    def do_all_events(self):
        ev = self.event_list.remove_first()
        while ev is not None:
            self.time = ev.time

            if self.time > self.sim_limit:
                break

            ev.execute(self)
            ev = self.event_list.remove_first()


class Beep:
    time = 0
    data_set = open('data_set.txt', 'a')
    node = None
    sim_limit = None
    next_node = None
    weight_g = None

    def __lt__(self, obj2):
        return self.time <= obj2.time

    def execute(self, sim):
        q_length = []
        for i in self.weight_g:
            for j in self.weight_g[i]:
                if len(self.node[i].q[j].que) == 0:
                    if self.node[i].q[j].s.packetBeingServed is None:
                        q_length.append(0)
                    else:
                        q_length.append(self.node[i].q[j].s.packetBeingServed.length)
                else:
                    all_paclen = self.node[i].q[j].s.packetBeingServed.length
                    for k in range(len(self.node[i].q[j].que)):
                        all_paclen += self.node[i].q[j].que[k].length
                    q_length.append(all_paclen)
        data_set = {}
        for i in self.weight_g:
            data_set[i] = {}
            for j in list(self.weight_g.keys())[0:16]:
                if j != i:
                    data_set[i][j] = [i, j]
                    data_set[i][j].extend(q_length)
                    data_set[i][j].append(self.node[i].rt[j])
                    for k in range(len(data_set[i][j])-1):
                        print(data_set[i][j][k], end=' ', file=self.data_set)
                    print(data_set[i][j][len(data_set[i][j])-1], end='', file=self.data_set)
                    print('\n', end='', file=self.data_set)
        interval = 0.2
        self.time = self.time + interval
        if self.time <= sim.sim_limit:
            sim.insertEv(self)


class Calcuroute:
    time = 0
    node = None
    sim_limit = None
    next_node = None
    weight_g = None

    def execute(self, sim):
        q_length = {}
        for i in self.weight_g:
            q_length[i] = {}
            for j in self.weight_g[i]:
                if len(self.node[i].q[j].que) == 0:
                    if self.node[i].q[j].s.packetBeingServed is None:
                        q_length[i][j] = 0
                    else:
                        q_length[i][j] = self.node[i].q[j].s.packetBeingServed.length
                else:
                    all_paclen = self.node[i].q[j].s.packetBeingServed.length
                    for k in range(len(self.node[i].q[j].que)):
                        all_paclen += self.node[i].q[j].que[k].length
                    q_length[i][j] = all_paclen

        for i in self.weight_g:
            for j in self.weight_g[i]:
                self.weight_g[i][j] = (1000 + q_length[i][j]) / self.node[i].q[j].s.bw

        r = {}
        for i in self.weight_g:
            dis = {i: 0}
            pre = {i: None}
            for j in self.weight_g:
                if j != i:
                    dis[j] = float("inf")
            s = set()
            p_queue = []
            hq.heappush(p_queue, (0, i))
            while len(p_queue) > 0:
                min_v = hq.heappop(p_queue)
                dist = min_v[0]
                u = min_v[1]
                s.add(u)
                adj_nodes = self.weight_g[u].keys()
                for v in adj_nodes:
                    if v not in s:
                        if dist + self.weight_g[u][v] < dis[v]:
                            if (dis[v], v) not in p_queue:
                                dis[v] = dist + self.weight_g[u][v]
                                hq.heappush(p_queue, (dis[v], v))
                            else:
                                index = p_queue.index((dis[v], v))
                                dis[v] = dist + self.weight_g[u][v]
                                p_queue[index] = (dis[v], v)
                            pre[v] = u

            path = {}
            for v in self.weight_g:
                if v == i:
                    continue
                path[v] = []

            for v in self.weight_g:
                if v == i:
                    path[v] = v
                    continue
                path[v].append(v)
                parent = pre[v]
                path[v].insert(0, parent)
                while parent is not i:
                    parent = pre[parent]
                    path[v].insert(0, parent)
            r[i] = path

        self.next_node = {}
        for i in self.weight_g:
            self.next_node[i] = {}
        for i in self.weight_g:
            for j in self.weight_g:
                p = r[i][j]
                if isinstance(p, int):
                    self.next_node[i][j] = i
                else:
                    self.next_node[i][j] = p[1]

        for i in self.weight_g:
            for j in self.weight_g:
                if i == j:
                    self.node[i].rt[i] = 0
                else:
                    self.node[i].rt[j] = self.next_node[i][j]

        interval = 2
        self.time = self.time + interval
        if self.time <= sim.sim_limit:
            sim.insertEv(self)
