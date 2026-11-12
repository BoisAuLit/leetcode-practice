"""
Floyd: 所有点对, 点数小于等于 100

画面:   一张城市票价表, 依次让每个城市 k 当 "中转站": 看 i 经 k 转到 j 会不会比现在便宜, 便宜就改表。
        所有城市轮一遍当过中转站, 表上就是任意两点的最便宜价。
动作:   ① 开表 (对角线 0, 有边填 w, 其余 inf)
        ② 挑中转站 k (最外层循环, 顺序不能挪到里面)
        ③ 改表 (dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]))
动作对代码: 见下面 # ! 注释
签名题: LC-1334 Find the City With the Smallest Number of Neighbors at a Threshold Distance
决策句: 点数小于等于 100 左右且要所有点对最短路, 三层循环直接写 O(V^3); 点多或只要单源, 用 08 Dijkstra (多源就跑 n 次)。
改一行: 和 10 Bellman-Ford 比, 松弛顺序从 "按边扫 V - 1 轮" 换成 "按中转点扫 n 轮", 距离从一维数组变成二维表。
        LC-1462 Course Schedule IV: 把 min 换成 or, 表里存 "能否到达", 就是传递闭包。
"""
from typing import List

INF = float("inf")


def floyd(n: int, edges: List[List[int]], directed: bool = False) -> List[List[float]]:
    dist = [[INF] * n for _ in range(n)]                # ! ① 开表
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)                 # 重边取最小
        if not directed:
            dist[v][u] = min(dist[v][u], w)
    for k in range(n):                                  # ! ② 中转站必须在最外层
        for i in range(n):
            if dist[i][k] == INF:
                continue                                # 小剪枝: i 到不了 k, 这行不用算
            for j in range(n):
                nd = dist[i][k] + dist[k][j]            # ! ③ 改表
                if nd < dist[i][j]:
                    dist[i][j] = nd
    return dist


def find_the_city(n: int, edges: List[List[int]], threshold: int) -> int:
    """LC-1334: 距离不超过 threshold 的邻居最少的城市, 并列取编号最大的"""
    dist = floyd(n, edges)
    best_cnt, best_city = n + 1, -1
    for i in range(n):
        cnt = sum(1 for j in range(n) if j != i and dist[i][j] <= threshold)
        if cnt <= best_cnt:                             # <= 让并列时取编号大的
            best_cnt, best_city = cnt, i
    return best_city


def transitive_closure(n: int, edges: List[List[int]]) -> List[List[bool]]:
    """LC-1462 变体: reach[i][j] = i 能否到 j; min 换成 or"""
    reach = [[False] * n for _ in range(n)]             # ! ①
    for u, v in edges:
        reach[u][v] = True
    for k in range(n):                                  # ! ②
        for i in range(n):
            if not reach[i][k]:
                continue
            for j in range(n):
                if reach[k][j]:
                    reach[i][j] = True                  # ! ③ 改表: i 到 k 且 k 到 j
    return reach


if __name__ == "__main__":
    print(find_the_city(4, [[0, 1, 3], [1, 2, 1], [1, 3, 4], [2, 3, 1]], 4))                    # 3
    print(find_the_city(5, [[0, 1, 2], [0, 4, 8], [1, 2, 3], [1, 4, 2], [2, 3, 1], [3, 4, 1]], 2))  # 0
    print(transitive_closure(3, [[0, 1], [1, 2]])[0][2])                                        # True
