from Multi_interface import *
import dijkstra

random.seed(1)

doc = open('new_delay.txt', 'w')
data_set = open('data_set.txt', 'a')
throughput = open('throughput.txt', 'w')

# topology:
# n1----n2---n3---n4---n5
#  |    |    |    |    |
# n16---n17--n18--n19--n6
#  |    |    |    |    |
# n15---n20--n21--n22--n7
#  |    |    |    |    |
# n14---n23--n24--n25--n8
#  |    |    |    |    |
# n13---n12--n11--n10--n9

weight_g = {
        1: {2: 1, 16: 1},
        2: {1: 1, 3: 1, 17: 1},
        3: {2: 1, 4: 1, 18: 1},
        4: {3: 1, 5: 1, 19: 1},
        5: {4: 1, 6: 1},
        6: {5: 1, 7: 1, 19: 1},
        7: {6: 1, 8: 1, 22: 1},
        8: {7: 1, 9: 1, 25: 1},
        9: {8: 1, 10: 1},
        10: {9: 1, 11: 1, 25: 1},
        11: {10: 1, 12: 1, 24: 1},
        12: {11: 1, 13: 1, 23: 1},
        13: {12: 1, 14: 1},
        14: {13: 1, 15: 1, 23: 1},
        15: {14: 1, 16: 1, 20: 1},
        16: {1: 1, 15: 1, 17: 1},
        17: {2: 1, 16: 1, 18: 1, 20: 1},
        18: {3: 1, 17: 1, 19: 1, 21: 1},
        19: {4: 1, 6: 1, 18: 1, 22: 1},
        20: {15: 1, 17: 1, 21: 1, 23: 1},
        21: {18: 1, 20: 1, 22: 1, 24: 1},
        22: {7: 1, 19: 1, 21: 1, 25: 1},
        23: {12: 1, 14: 1, 20: 1, 24: 1},
        24: {11: 1, 21: 1, 23: 1, 25: 1},
        25: {8: 1, 10: 1, 22: 1, 24: 1}
    }

# 得到各节点对的最短路径
P = {}
for i in weight_g:
    P[i] = dijkstra.di(weight_g, i)  # p[i][j]为i到j路径[i,..j]

# 得到各节点对的最短路径下一跳
next_node = {}
for i in weight_g:
    next_node[i] = {}
for i in weight_g:
    for j in weight_g:
        p = P[i][j]
        if isinstance(p, int):
            next_node[i][j] = i
        else:
            next_node[i][j] = p[1]

sim = Simulator()
sim.event_list = EventList()
sim.sim_limit = 100

# 创建节点
Nodelist = {}
for i in weight_g:
    Nodelist[i] = Node(i)
    Nodelist[i].doc = doc
    Nodelist[i].weight_g = weight_g

# 获得各节点的接口数以及相邻节点
interface_no = {}
for i in weight_g:
    interface_no[i] = len(weight_g[i])
    for j in weight_g[i]:
        Nodelist[i].interface[j] = j

# 定义每个节点上路由表的下一跳及下一跳对应的接口
for i in weight_g:
    Nodelist[i].node = Nodelist
    for j in weight_g:
        if i == j:
            Nodelist[i].rt[i] = 0
        else:
            Nodelist[i].rt[j] = next_node[i][j]

# 创建16个发包器，对应16条流
G = {}
for i in (list(weight_g.keys())[0:16]):
    j = random.choice(list(weight_g.keys())[0:16])
    while j == i:
        j = random.choice(list(weight_g.keys())[0:16])
    G[i] = GenePoisEv(i, j)
    G[i].node = Nodelist
    G[i].weight_g = weight_g
    G[i].time = i
    G[i].rate = 100


# 存放队列和服务器
Q = {}
S = {}

# 根据各节点的接口数产生相应的队列及服务器
for i in weight_g:
    Q[i] = {}
    S[i] = {}
    for j in weight_g[i]:
        Q[i][j] = Que()
        S[i][j] = ServExpEv()

# 将各节点上接口的队列和服务器相关
for i in weight_g:
    for j in Nodelist[i].interface:
        Nodelist[i].q[j] = Q[i][j]
        Nodelist[i].q[j].s = S[i][j]
        S[i][j].q = Q[i][j]

# 将各个接口上服务器与下一跳节点关联，包到达下一节点，该节点对包进行处理
for i in weight_g:
    for j in weight_g[i]:
        S[i][j].node = Nodelist[j]

# 创建一个beep,定时获取数据
# B = Beep()
# B.sim_limit = 100
# B.time = 1.2
# B.node = Nodelist
# B.next_node = next_node
# B.weight_g = weight_g
# sim.insert_ev(B)

# R = Calcuroute()
# R.sim_limit = 100
# R.time = 2
# R.node = Nodelist
# R.next_node = next_node
# R.weight_g = weight_g
# sim.insert_ev(R)

for i in G:
    sim.insert_ev(G[i])
sim.do_all_events()
doc.close()
data_set.close()
print(Nodelist[1].throughout/(sim.sim_limit*1000), file=throughput)
throughput.close()
