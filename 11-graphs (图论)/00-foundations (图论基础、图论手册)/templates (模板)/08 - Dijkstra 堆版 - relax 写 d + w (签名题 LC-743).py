"""
Dijkstra 堆版: relax 写 d + w

画面:   从起点泼水, 水位一寸一寸抬高; 堆里放的是 "水即将淹到某点的时刻",
        每次取最早淹到的那个点, 它的时刻就定下来了, 再去更新它邻居的时刻。
动作:   ① 定起点 (dist[src] = 0, 入堆)
        ② 取最早 (heappop 出 d 最小的点)
        ③ 撕作废票 (d > dist[u] 说明这张票过期, 跳过)
        ④ 松弛 (nd = d + w, 比 dist[v] 小就更新 + 入堆)
动作对代码: 见下面 # ! 注释
签名题: LC-743 Network Delay Time (答案 = max(dist), 有 inf 返回 -1)
决策句: 边权非负问最短路用它; 权全相等用 03 BFS; 权只有 0/1 用 09; 有负权或限制 k 条边用 10 Bellman-Ford。
改一行: 和 03 BFS 比, 队列换成堆, 层数换成 dist 数组, 多了一行作废票检查。
        LC-1631 Path With Minimum Effort (最小化路径上最大边): nd = max(d, w)
        LC-1102 Path With Maximum Minimum Value (最大化路径上最小边): nd = min(d, w), 堆存 -d 取最大
        13 Prim: nd = w (不加 d), 就变成最小生成树
"""
import heapq
from typing import List, Tuple

INF = float("inf")


def dijkstra(n: int, adj: List[List[Tuple[int, int]]], src: int) -> List[float]:
    dist = [INF] * n
    dist[src] = 0
    heap = [(0, src)]                                   # ! ① 定起点
    while heap:
        d, u = heapq.heappop(heap)                      # ! ② 取最早
        if d > dist[u]:
            continue                                    # ! ③ 撕作废票
        for v, w in adj[u]:
            nd = d + w                                  # ! ④ 松弛就改这一行: 瓶颈路 max(d, w); 最大化最小边 min(d, w)
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist


def network_delay_time(times: List[List[int]], n: int, k: int) -> int:
    """LC-743: 1-indexed, 信号从 k 出发到全部点的最晚时刻"""
    adj = [[] for _ in range(n + 1)]
    for u, v, w in times:
        adj[u].append((v, w))
    dist = dijkstra(n + 1, adj, k)
    ans = max(dist[1:])
    return -1 if ans == INF else ans


def minimum_effort_path(heights: List[List[int]]) -> int:
    """LC-1631 瓶颈路: 网格隐式图, 边权 = 相邻高度差, 最小化路径上的最大边"""
    rows, cols = len(heights), len(heights[0])
    dist = [[INF] * cols for _ in range(rows)]
    dist[0][0] = 0
    heap = [(0, 0, 0)]                                  # ! ①
    while heap:
        d, r, c = heapq.heappop(heap)                   # ! ②
        if d > dist[r][c]:
            continue                                    # ! ③
        if (r, c) == (rows - 1, cols - 1):
            return d
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols:
                nd = max(d, abs(heights[nr][nc] - heights[r][c]))   # ! ④ 唯一改动: d + w 换成 max(d, w)
                if nd < dist[nr][nc]:
                    dist[nr][nc] = nd
                    heapq.heappush(heap, (nd, nr, nc))
    return 0


if __name__ == "__main__":
    print(network_delay_time([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2))     # 2
    print(network_delay_time([[1, 2, 1]], 2, 2))                            # -1
    print(minimum_effort_path([[1, 2, 2], [3, 8, 2], [5, 3, 5]]))           # 2
