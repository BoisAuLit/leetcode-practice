"""LC-1091 - Shortest Path in Binary Matrix

合并自 4 个解法文件:
  1. 1091 - A - Shortest Path in Binary - BFS 最好用 ✅ - 别用 DFS, 无解 ❌.py
  2. 1091 - B - Shortest Path in Binary - BFS 最好用 ✅ - Level by Level.py
  3. 1091 - C - Shortest Path in Binary - DFS Recursive (TODO, empty).py
  4. 1091 - D - Shortest Path in Binary - BFS Queue - 更快 🚀 (TODO, empty).py

阶段 1 · BFS 层数 = 步数 ○ 核心题
题目在问：n x n 的 0/1 网格，从左上角走到右下角、八方向、只能踩 0，最短路径含几个格子（起点算 1）；走不到 -1
点是什么：一个格子   边是什么：八方向相邻且是 0
和签名题比改了哪一行：994 的"多源一起入队"变回"单源 (0, 0) 入队"；四方向改八方向；
    答案是格子数不是步数，所以起点带 d = 1 入队；起点或终点本身是 1 直接 -1
注意：Solution_1_DFS 这个类名是合并脚本按原文件名起的，里面写的其实是 BFS（原文件名就写着"别用 DFS"）；
    参数名 grid_1 / grid_2 也是合并脚本改的，贴回 LeetCode 时要叫 grid
"""

from typing import List

from collections import deque
from heapq import heappush, heappop  # Solution_3 的 A* 用


# ============================================================================
# Solution 1: DFS    (原文件: 1091 - A - Shortest Path in Binary - BFS 最好用 ✅ - 别用 DFS, 无解 ❌.py)
# ============================================================================

grid_1 = [[0, 0, 0], [1, 1, 0], [1, 1, 0]]

##################################################################################################
##### ! Solution 1: BFS，队列里带距离 (x, y, d)（类名叫 DFS，其实是 BFS）
##### ! 时间复杂度: O(n²)  每格最多进队一次、看 8 个邻居   空间复杂度: O(n²)  队列 + seen
##### ! 适用：单源无权最短路的默认写法；距离跟着格子走，不用按层数圈
##################################################################################################


class Solution_1_DFS:
    def shortestPathBinaryMatrix(self, grid_1: List[List[int]]) -> int:
        if grid_1[0][0] + grid_1[-1][-1] != 0:
            return -1
        n = len(grid_1)
        directions = [
            (dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy
        ]
        queue = deque([(0, 0, 1)])
        seen = {(0, 0)}
        while queue:
            x, y, d = queue.popleft()
            if (x, y) == (n - 1, n - 1):
                return d
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < n
                    and 0 <= ny < n
                    and grid_1[nx][ny] == 0
                    and (nx, ny) not in seen
                ):
                    seen.add((nx, ny))
                    queue.append((nx, ny, d + 1))
        return -1

# ============================================================================
# Solution 2: Level_by_Level    (原文件: 1091 - B - Shortest Path in Binary - BFS 最好用 ✅ - Level by Level.py)
# ============================================================================

grid_2 = [[0, 0, 0], [1, 1, 0], [1, 1, 0]]

##################################################################################################
##### ! Solution 2: BFS 按层计数，for _ in range(len(queue)) 圈出一层
##### ! 时间复杂度: O(n²)   空间复杂度: O(n²)
##### ! 适用：本文件夹的模板"层数 = 步数"，和 994 / 286 同一套写法；两种 BFS 并列时选它，因为它和签名题长得一样
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_2_Level_by_Level:
    def shortestPathBinaryMatrix(self, grid_2: List[List[int]]) -> int:
        if grid_2[0][0] + grid_2[-1][-1] != 0:
            return -1
        n = len(grid_2)
        directions = [
            (dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy
        ]
        queue = deque([(0, 0, 1)])
        seen = {(0, 0)}
        while queue:
            for _ in range(len(queue)):
                x, y, d = queue.popleft()
                if x == y == n-1:
                    return d
                for dx, dy in directions:
                    nx = x + dx
                    ny = y + dy
                    if 0 <= nx < n and 0 <= ny < n and grid_2[nx][ny] == 0 and (nx, ny) not in seen:
                        seen.add((nx, ny))
                        queue.append((nx, ny, d+1))
        return -1

# ============================================================================
# Solution 3: DFS_Recursive_TODO_empty    (原文件: 1091 - C - Shortest Path in Binary - DFS Recursive (TODO, empty).py)
# ============================================================================

# ============================================================================
# Solution 4: TODO_empty    (原文件: 1091 - D - Shortest Path in Binary - BFS Queue - 更快 🚀 (TODO, empty).py)
# ============================================================================


##################################################################################################
##### ! Solution 3: A*，启发函数 = 切比雪夫距离 max(n-1-x, n-1-y)
##### ! 时间复杂度: O(n² log n)  堆操作   空间复杂度: O(n²)
##### ! 适用：起点终点都已知、想少扩一些格子时；八方向一步能同时缩短行差和列差，所以切比雪夫距离永远不高估（可采纳），
##### !       A* 的答案和 BFS 一样是最优的；0/1 网格上障碍少时它比 BFS 看的格子少得多，障碍多时退化成 Dijkstra
##################################################################################################


class Solution_3:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        n = len(grid)
        if grid[0][0] or grid[n - 1][n - 1]:
            return -1

        def h(x: int, y: int) -> int:
            return max(n - 1 - x, n - 1 - y)  # ! 切比雪夫距离：八方向下到终点至少还要走这么多步

        best = {(0, 0): 1}  # 到每格已知的最短格子数
        heap = [(1 + h(0, 0), 1, 0, 0)]  # ! (f = g + h, g, x, y)，g = 已走的格子数
        while heap:
            f, g, x, y = heappop(heap)
            if (x, y) == (n - 1, n - 1):
                return g  # ! h 可采纳 + 一致，第一次弹出终点就是最优
            if g > best[(x, y)]:
                continue  # 过期票
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nx, ny = x + dx, y + dy
                    if (
                        (dx or dy)
                        and 0 <= nx < n
                        and 0 <= ny < n
                        and grid[nx][ny] == 0
                        and g + 1 < best.get((nx, ny), float("inf"))
                    ):
                        best[(nx, ny)] = g + 1
                        heappush(heap, (g + 1 + h(nx, ny), g + 1, nx, ny))
        return -1



if __name__ == "__main__":

    # --- Solution 1: DFS ---
    s = Solution_1_DFS()
    result = s.shortestPathBinaryMatrix(grid_1)
    print(result)

    # --- Solution 2: Level_by_Level ---
    s = Solution_2_Level_by_Level()
    result = s.shortestPathBinaryMatrix(grid_2)
    print(result)

    # --- Solution 3: A* ---
    s = Solution_3()
    result = s.shortestPathBinaryMatrix([[0, 0, 0], [1, 1, 0], [1, 1, 0]])
    print(result)  # 4
    result = s.shortestPathBinaryMatrix([[1, 0, 0], [1, 1, 0], [1, 1, 0]])
    print(result)  # -1
