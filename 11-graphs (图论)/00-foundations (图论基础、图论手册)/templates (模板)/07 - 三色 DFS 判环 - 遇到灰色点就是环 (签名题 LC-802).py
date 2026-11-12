"""
三色 DFS 判环: 遇到灰色点就是环

画面:   走迷宫时给房间贴标签: 没进过的白, 正在走还没退出来的灰, 走完退出来的黑。
        推开一扇门发现里面是灰房间, 说明绕回了自己的来路: 有环。
动作:   ① 刷白 (color 全 0)
        ② 进门刷灰 (color[u] = 1)
        ③ 推门看色 (邻居灰 = 有环; 黑 = 已算完, 跳过; 白 = 递归进去)
        ④ 出门刷黑 (color[u] = 2, 顺手把 u 压进 post)
        ⑤ 倒序 (post 反转 = 拓扑序)
动作对代码: 见下面 # ! 注释
签名题: LC-802 Find Eventual Safe States (安全点 = 能刷黑的点; 卡在灰的点都在环上或能走进环)
决策句: 有向图判环, 或者要 "每个点自己能不能走进环" 用它; 只要一个顺序且怕递归太深, 用 06 Kahn。
改一行: 和 02 DFS 比, visited 从 "两种状态" 变成 "三种颜色", 多出来的灰色就是判环的全部。
        和 06 Kahn 比, 拓扑序不用 indeg, 把 post 反过来就是 (后序倒过来 = 拓扑序)。
        LC-207: has_cycle 取反就是答案。LC-210: topo_order_dfs 直接返回。
"""
from typing import List
import sys

sys.setrecursionlimit(10 ** 6)

WHITE, GRAY, BLACK = 0, 1, 2


def has_cycle(n: int, adj: List[List[int]]) -> bool:
    color = [WHITE] * n                                 # ! ① 刷白

    def dfs(u: int) -> bool:
        color[u] = GRAY                                 # ! ② 进门刷灰
        for v in adj[u]:
            if color[v] == GRAY:                        # ! ③ 推门看到灰: 有环
                return True
            if color[v] == WHITE and dfs(v):
                return True
        color[u] = BLACK                                # ! ④ 出门刷黑
        return False

    return any(color[u] == WHITE and dfs(u) for u in range(n))


def topo_order_dfs(n: int, adj: List[List[int]]) -> List[int]:
    """有环返回 []"""
    color = [WHITE] * n                                 # ! ①
    post = []

    def dfs(u: int) -> bool:
        color[u] = GRAY                                 # ! ②
        for v in adj[u]:
            if color[v] == GRAY or (color[v] == WHITE and dfs(v)):  # ! ③
                return True
        color[u] = BLACK                                # ! ④
        post.append(u)                                  # ! ④ 后序入栈
        return False

    for u in range(n):
        if color[u] == WHITE and dfs(u):
            return []
    return post[::-1]                                   # ! ⑤ 倒序 = 拓扑序


def eventual_safe_nodes(graph: List[List[int]]) -> List[int]:
    """LC-802: graph[u] 是 u 的出边; 返回所有安全点 (升序)"""
    n = len(graph)
    color = [WHITE] * n                                 # ! ①

    def safe(u: int) -> bool:
        if color[u] != WHITE:
            return color[u] == BLACK                    # ! ③ 灰 = 在环上或走进环, 不安全; 黑 = 安全
        color[u] = GRAY                                 # ! ②
        for v in graph[u]:
            if not safe(v):
                return False                            # ! 这里不刷黑, u 永远留灰 = 不安全
        color[u] = BLACK                                # ! ④ 所有出口都安全才刷黑
        return True

    return [u for u in range(n) if safe(u)]


if __name__ == "__main__":
    print(has_cycle(3, [[1], [2], [0]]))                                    # True
    print(has_cycle(3, [[1], [2], []]))                                     # False
    print(topo_order_dfs(4, [[1, 2], [2], [], [2]]))                        # [3, 0, 1, 2]
    print(eventual_safe_nodes([[1, 2], [2, 3], [5], [0], [5], [], []]))     # [2, 4, 5, 6]
