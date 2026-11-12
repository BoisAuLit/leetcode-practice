"""
0-1 BFS: 双端队列, 0 放队头 1 放队尾

画面:   走迷宫, 顺着箭头走免费, 逆着箭头走要花 1 块;
        免费到达的格子插队到队头 (和当前同一层), 花钱的排到队尾 (下一层)。
        队列里永远只有 "当前价" 和 "当前价 + 1" 两种票, 天然有序, 所以不需要堆。
动作:   ① 定起点 (dist[src] = 0, 入队)
        ② 取队头 (popleft, 用 dist[u] 当它的距离)
        ③ 松弛 (nd = dist[u] + w, 比 dist[v] 小就更新)
        ④ 分流 (w == 0 放队头 appendleft, w == 1 放队尾 append)
动作对代码: 见下面 # ! 注释
签名题: LC-1368 Minimum Cost to Make at Least One Valid Path in a Grid
决策句: 边权只有 0 和 1 (或只有两种值) 用它, O(V + E); 权有更多种就老实用 08 Dijkstra。
改一行: 和 08 Dijkstra 比, 堆换成双端队列, heappush 换成 "0 放队头 1 放队尾", 作废票检查可以省掉。
        和 03 BFS 比, 只多了 "权为 0 时 appendleft" 这一行。
        LC-2290 Minimum Obstacle Removal: 走进障碍格 w = 1, 空格 w = 0。
"""
from collections import deque
from typing import List, Tuple

INF = float("inf")


def zero_one_bfs(n: int, adj: List[List[Tuple[int, int]]], src: int) -> List[float]:
    dist = [INF] * n
    dist[src] = 0
    dq = deque([src])                                   # ! ① 定起点
    while dq:
        u = dq.popleft()                                # ! ② 取队头
        for v, w in adj[u]:
            nd = dist[u] + w                            # ! ③ 松弛
            if nd < dist[v]:
                dist[v] = nd
                if w == 0:
                    dq.appendleft(v)                    # ! ④ 免费: 插到队头
                else:
                    dq.append(v)                        # ! ④ 花钱: 排到队尾
    return dist


def min_cost_valid_path(grid: List[List[int]]) -> int:
    """LC-1368: 1 右 2 左 3 下 4 上; 顺着箭头走 0 元, 改箭头 1 元"""
    rows, cols = len(grid), len(grid[0])
    DIRS = {1: (0, 1), 2: (0, -1), 3: (1, 0), 4: (-1, 0)}
    dist = [[INF] * cols for _ in range(rows)]
    dist[0][0] = 0
    dq = deque([(0, 0)])                                # ! ①
    while dq:
        r, c = dq.popleft()                             # ! ②
        for sign, (dr, dc) in DIRS.items():
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            w = 0 if grid[r][c] == sign else 1          # 顺箭头免费, 否则花 1 块
            nd = dist[r][c] + w                         # ! ③
            if nd < dist[nr][nc]:
                dist[nr][nc] = nd
                if w == 0:
                    dq.appendleft((nr, nc))             # ! ④
                else:
                    dq.append((nr, nc))                 # ! ④
    return dist[rows - 1][cols - 1]


if __name__ == "__main__":
    adj = [[(1, 0), (2, 1)], [(3, 1)], [(3, 0)], []]
    print(zero_one_bfs(4, adj, 0))                                          # [0, 0, 1, 1]
    print(min_cost_valid_path([[1, 1, 1, 1], [2, 2, 2, 2], [1, 1, 1, 1], [2, 2, 2, 2]]))  # 3
    print(min_cost_valid_path([[1, 1, 3], [3, 2, 2], [1, 1, 4]]))           # 0
