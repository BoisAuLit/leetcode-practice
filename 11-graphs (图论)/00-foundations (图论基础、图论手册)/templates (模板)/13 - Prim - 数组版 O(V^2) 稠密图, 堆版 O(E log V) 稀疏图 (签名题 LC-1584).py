"""
Prim: 数组版 O(V^2) 稠密图, 堆版 O(E log V) 稀疏图

画面:   从一个点起一个圈子; 圈子里的人都报 "把圈外某人拉进来要多少钱",
        每轮拉最便宜的那个圈外人进来, 他进来以后也开始报价 (降价)。圈子长到包住所有人为止。
动作:   ① 起圈子 (key[0] = 0, 其余 inf)
        ② 看牌 (圈外 key 最小的点: 数组版扫一遍 O(V), 堆版 heappop)
        ③ 拉进圈 (in_mst[u] = True, cost += key[u])
        ④ 降价 (圈外邻居 v: w < key[v] 就 key[v] = w)
动作对代码: 见下面 # ! 注释
签名题: LC-1584 Min Cost to Connect All Points (坐标, 稠密, 用数组版)
决策句: 稠密图 (E 接近 V^2, 比如坐标题) 用数组版 O(V^2); 稀疏图 (给边列表) 用堆版 O(E log V) 或 12 Kruskal。
改一行: 和 08 Dijkstra 是同一副骨架: 把 nd = d + w 改成 nd = w 就是 Prim
        (key 记的是 "连进圈子的最后一条边", 不是 "到起点的总长")。
        和 12 Kruskal 比, Prim 一个点一个点长, Kruskal 一条边一条边审, 结果相同。
"""
import heapq
from typing import List, Tuple

INF = float("inf")


def prim_dense(points: List[List[int]]) -> int:
    """数组版: 完全图不建边, 要边权时现算 (曼哈顿距离)"""
    n = len(points)
    key = [INF] * n
    key[0] = 0                                          # ! ① 起圈子
    in_mst = [False] * n
    cost = 0
    for _ in range(n):
        u = -1
        for i in range(n):                              # ! ② 看牌: 扫一遍找圈外最小 key
            if not in_mst[i] and (u == -1 or key[i] < key[u]):
                u = i
        in_mst[u] = True                                # ! ③ 拉进圈
        cost += key[u]
        for v in range(n):
            if not in_mst[v]:
                w = abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1])
                if w < key[v]:
                    key[v] = w                          # ! ④ 降价: 写 w, 不是 key[u] + w
    return cost


def prim_heap(n: int, adj: List[List[Tuple[int, int]]]) -> int:
    """堆版: 和 08 Dijkstra 同骨架; 图不连通返回 -1"""
    in_mst = [False] * n
    heap = [(0, 0)]                                     # ! ① 起圈子: (key, 点)
    cost, used = 0, 0
    while heap and used < n:
        k, u = heapq.heappop(heap)                      # ! ② 看牌
        if in_mst[u]:
            continue                                    # 作废票: 已经在圈里
        in_mst[u] = True                                # ! ③ 拉进圈
        cost += k
        used += 1
        for v, w in adj[u]:
            if not in_mst[v]:
                heapq.heappush(heap, (w, v))            # ! ④ 降价: Dijkstra 这里是 (k + w, v), Prim 只放 w
    return cost if used == n else -1


if __name__ == "__main__":
    pts = [[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]
    print(prim_dense(pts))                                                  # 20
    adj = [[] for _ in range(4)]
    for u, v, w in [[0, 1, 1], [1, 2, 2], [2, 3, 3], [0, 3, 10]]:
        adj[u].append((v, w))
        adj[v].append((u, w))
    print(prim_heap(4, adj))                                                # 6
    print(prim_heap(3, [[(1, 1)], [(0, 1)], []]))                           # -1
