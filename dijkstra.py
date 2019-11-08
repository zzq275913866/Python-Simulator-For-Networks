import heapq as hq


def di(weight_g, s):

    dis = {s: 0}
    pre = {s: None}

    for v in weight_g:
        if v != s:
            dis[v] = float("inf")

    S = set()
    p_queue = []
    hq.heappush(p_queue, (0, s))
    while len(p_queue) > 0:
        min_v = hq.heappop(p_queue)
        dist = min_v[0]
        u = min_v[1]
        S.add(u)
        adj_nodes = weight_g[u].keys()
        for v in adj_nodes:
            if v not in S:
                if dist + weight_g[u][v] < dis[v]:
                    if (dis[v], v) not in p_queue:
                        dis[v] = dist + weight_g[u][v]
                        hq.heappush(p_queue, (dis[v], v))
                    else:
                        index = p_queue.index((dis[v], v))
                        dis[v] = dist + weight_g[u][v]
                        p_queue[index] = (dis[v], v)
                    pre[v] = u
    path = {}
    for v in weight_g:
        if v == s:
            continue
        path[v] = []

    for v in weight_g:
        if v == s:
            path[v] = v
            continue
        path[v].append(v)
        parent = pre[v]
        path[v].insert(0, parent)
        while parent is not s:
            parent = pre[parent]
            path[v].insert(0, parent)

    return path
