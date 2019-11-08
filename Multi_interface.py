import abc
import random
import heapq as hq


class Event:
    time = 0

    def lt(self, obj2):
        return (self.time <= obj2.time)

    @abc.abstractmethod
    def execute(self, sim):
        pass


class EventList:
    elements = []

    def ins(self, x):
        i = 1
        length = len(self.elements)
        while (i <= length and (self.elements[i-1].time < x.time)):
            i = i + 1

        if len(self.elements) == 0:
            self.elements.append(x)
        else:
            self.elements.insert(i-1, x)

    def removefirst(self):

        if len(self.elements) == 0:
            ev = []
            return

        ev = self.elements[0]
        del self.elements[0]
        return ev


class Node:
    doc = ''
    d = []
    weight_g = None
    node = None
    throughout = 0

    def __init__(self, id):
        self.id = id
        self.interface = {}
        self.rt = {}
        self.q = {}

    def handlePacket(self, packet, sim):
        if packet.dest == self.id:
            soj_t = sim.now() - packet.created
            A = [packet.srt, packet.dest, soj_t]
            # print('%f' % soj_t, file=self.doc)
            self.d.append(soj_t)
            Node.throughout += (packet.length/1000)
            print(A[0], A[1], A[2], file=self.doc)
        else:
            index = packet.path.index(self.id)
            # packet.length = random.expovariate(0.001)
            self.rt[packet.dest] = packet.path[index + 1]
            self.q[packet.path[index + 1]].insertQ(packet, sim)


class GenePoisEv(Event):
    node = None
    weight_g = None
    next_node = None
    rate = None

    def __init__(self, id, dest):
        self.id = id
        self.dest = dest
        self.path = ''

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

            P = {}
            for i in self.weight_g:
                dis = {i: 0}
                pre = {i: None}
                for j in self.weight_g:
                    if j != i:
                        dis[j] = float("inf")
                S = set()
                p_queue = []
                hq.heappush(p_queue, (0, i))
                while len(p_queue) > 0:
                    min_v = hq.heappop(p_queue)
                    dist = min_v[0]
                    u = min_v[1]
                    S.add(u)
                    adj_nodes = self.weight_g[u].keys()
                    for v in adj_nodes:
                        if v not in S:
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
                P[i] = path

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

            p = P[self.id][self.dest]
            self.path = p
            for i in range(len(p) - 1):
                self.node[p[i]].q[p[i+1]].s.arr_rate += self.rate

        packet.path = self.path
        self.node[packet.srt].handlePacket(packet, sim)
        interarrivalTime = random.expovariate(self.rate)
        self.time = self.time + interarrivalTime
        sim.insertEv(self)


class Packet:
    def __init__(self, created):
        self.created = created
        self.sent = ''
        self.srt = ''
        self.dest = ''
        self.length = ''
        self.path = []


class Que:
    def __init__(self):
        self.que = []
        self.s = ''

    def insertQ(self, packet, sim):
        if self.s.packetBeingServed is None:
            self.s.insertServ(packet, sim)
        else:
            self.que.append(packet)

    def remove(self):
        pac = self.que[0]
        del self.que[0]
        return pac


class ServExpEv(Event):

    def __init__(self):
        self.packetBeingServed = None
        self.q = ''
        self.bw = 4 * (10**5)
        self.node = None
        self.arr_rate = 0

    def execute(self, sim):
        sim.time = self.time
        self.node.handlePacket(self.packetBeingServed, sim)
        self.packetBeingServed = None

        if len(self.q.que) != 0:
            packet = self.q.remove()
            self.insertServ(packet, sim)

    def insertServ(self, packet, sim):
        self.packetBeingServed = packet
        serviceTime = self.packetBeingServed.length / self.bw
        self.time = sim.now() + serviceTime
        sim.insertEv(self)


class Simulator:
    time = 0
    sim_limit = ''
    event_list = []

    def now(self):
        return self.time

    def insertEv(self, ev):
        self.event_list.ins(ev)

    def doAllEvents(self):
        ev = self.event_list.removefirst()
        while ev is not None:
            self.time = ev.time

            if self.time > self.sim_limit:
                break

            ev.execute(self)
            ev = self.event_list.removefirst()


class Beep(Event):
    node = None
    data_set = ''
    sim_limit = None
    next_node = None
    weight_g = None

    def execute(self, sim):
        Q_length = []
        for i in self.weight_g:
            for j in self.weight_g[i]:
                if len(self.node[i].q[j].que) == 0:
                    if self.node[i].q[j].s.packetBeingServed is None:
                        Q_length.append(0)
                    else:
                        Q_length.append(self.node[i].q[j].s.packetBeingServed.length)
                else:
                    all_paclen = self.node[i].q[j].s.packetBeingServed.length
                    for k in range(len(self.node[i].q[j].que)):
                        all_paclen += self.node[i].q[j].que[k].length
                    Q_length.append(all_paclen)
        dataset = {}
        for i in self.weight_g:
            dataset[i] = {}
            for j in list(self.weight_g.keys())[0:16]:
                if j != i:
                    dataset[i][j] = [i, j]
                    dataset[i][j].extend(Q_length)
                    dataset[i][j].append(self.node[i].rt[j])
                    for k in range(len(dataset[i][j])-1):
                        print(dataset[i][j][k], end=' ', file=self.data_set)
                    print(dataset[i][j][len(dataset[i][j])-1], end='', file=self.data_set)
                    print('\n', end='', file=self.data_set)
        interval = 0.2
        self.time = self.time + interval
        if self.time <= sim.sim_limit:
            sim.insertEv(self)


class Calcuroute(Event):
    node = None
    sim_limit = None
    next_node = None
    weight_g = None

    def execute(self, sim):
        Q_length = {}
        for i in self.weight_g:
            Q_length[i] = {}
            for j in self.weight_g[i]:
                if len(self.node[i].q[j].que) == 0:
                    if self.node[i].q[j].s.packetBeingServed is None:
                        Q_length[i][j] = 0
                    else:
                        Q_length[i][j] = self.node[i].q[j].s.packetBeingServed.length
                else:
                    all_paclen = self.node[i].q[j].s.packetBeingServed.length
                    for k in range(len(self.node[i].q[j].que)):
                        all_paclen += self.node[i].q[j].que[k].length
                    Q_length[i][j] = all_paclen

        for i in self.weight_g:
            for j in self.weight_g[i]:
                self.weight_g[i][j] = (1000 + Q_length[i][j]) / self.node[i].q[j].s.bw

        P = {}
        for i in self.weight_g:
            dis = {i: 0}
            pre = {i: None}
            for j in self.weight_g:
                if j != i:
                    dis[j] = float("inf")
            S = set()
            p_queue = []
            hq.heappush(p_queue, (0, i))
            while len(p_queue) > 0:
                min_v = hq.heappop(p_queue)
                dist = min_v[0]
                u = min_v[1]
                S.add(u)
                adj_nodes = self.weight_g[u].keys()
                for v in adj_nodes:
                    if v not in S:
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
            P[i] = path

        self.next_node = {}
        for i in self.weight_g:
            self.next_node[i] = {}
        for i in self.weight_g:
            for j in self.weight_g:
                p = P[i][j]
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
