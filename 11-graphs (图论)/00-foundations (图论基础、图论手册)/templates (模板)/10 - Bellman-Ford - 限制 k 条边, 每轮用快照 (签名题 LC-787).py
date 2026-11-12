"""
Bellman-Ford: 限制 k 条边, 每轮用快照

画面:   广播: 每一轮, 每条边都喊一次 "我这头到起点的距离 + 边权", 对面比这大就改。
        一轮过后 "最多 1 条边能到" 的距离就对了; 跑 k 轮就是 "最多 k 条边"。
        用快照是为了一轮里不能连着传两步, 否则 k 的限制就失效。
动作:   ① 定起点 (dist[src] = 0)
        ② 拍快照 (prev = dist[:], 这一轮只读 prev 写 dist)
        ③ 扫所有边 (prev[u] + w < dist[v] 就改 dist[v])
        ④ 定轮数 (k 次中转 = 最多 k + 1 条边 = 跑 k + 1 轮)
        ⑤ 验收 (普通版: V - 1 轮后再扫一轮还能松弛 = 有负环)
动作对代码: 见下面 # ! 注释
签名题: LC-787 Cheapest Flights Within K Stops
决策句: 限制 "最多 k 条边" 或者有负权边时用它 O(kE); 边权非负且不限边数, 08 Dijkstra 快得多。
改一行: 和 08 Dijkstra 比, 不要堆也不要邻接表, 直接 for 循环扫边列表; 多出来的是 "拍快照" 这一行 (dist[:])。
        普通版 (不限 k): 跑 V - 1 轮, 快照可省, 某一轮没有任何变化就提前 break。
"""
from typing import List, Optional

INF = float("inf")


def find_cheapest_price(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
    """LC-787: 最多 k 次中转 = 最多 k + 1 条边"""
    dist = [INF] * n
    dist[src] = 0                                       # ! ① 定起点
    for _ in range(k + 1):                              # ! ④ 跑 k + 1 轮
        prev = dist[:]                                  # ! ② 拍快照
        for u, v, w in flights:
            if prev[u] + w < dist[v]:                   # ! ③ 只读快照 prev, 写 dist (inf + w 还是 inf, 不用特判)
                dist[v] = prev[u] + w
    return -1 if dist[dst] == INF else dist[dst]


def bellman_ford(n: int, edges: List[List[int]], src: int) -> Optional[List[float]]:
    """普通版: 允许负权边; 有负环返回 None"""
    dist = [INF] * n
    dist[src] = 0                                       # ! ①
    for _ in range(n - 1):                              # ! ④ 最短路最多 n - 1 条边, 所以跑 n - 1 轮
        changed = False
        for u, v, w in edges:                           # ! ③ 不拍快照: 同一轮多传几步也没关系, 只会更快收敛
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    for u, v, w in edges:                               # ! ⑤ 验收: 还能松弛就是负环
        if dist[u] + w < dist[v]:
            return None
    return dist


if __name__ == "__main__":
    flights = [[0, 1, 100], [1, 2, 100], [0, 2, 500]]
    print(find_cheapest_price(3, flights, 0, 2, 1))                         # 200
    print(find_cheapest_price(3, flights, 0, 2, 0))                         # 500
    print(bellman_ford(3, [[0, 1, 4], [0, 2, 5], [1, 2, -3]], 0))           # [0, 4, 1]
    print(bellman_ford(3, [[0, 1, 1], [1, 2, -1], [2, 1, -1]], 0))          # None
