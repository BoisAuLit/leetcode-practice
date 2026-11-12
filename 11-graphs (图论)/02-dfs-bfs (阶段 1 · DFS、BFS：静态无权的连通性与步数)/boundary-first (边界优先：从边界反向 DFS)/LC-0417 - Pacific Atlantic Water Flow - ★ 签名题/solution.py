"""LC-0417 - Pacific Atlantic Water Flow

阶段 1 · DFS、BFS（静态无权的连通性与步数）· 边界优先（从边界反向 DFS）★ 签名题
题目在问：哪些格子的水既能流到太平洋（上边、左边）又能流到大西洋（下边、右边）
点是什么：一个格子   边是什么：反向看，从 (x, y) 爬到不比它矮的邻居（水能从邻居流到这里）
和签名题比改了哪一行：本题就是边界反向 DFS 签名题；从两边海岸分别往高处爬，两个 seen 取交集
"""
from typing import List
from collections import deque


##################################################################################################
##### ! Solution 1: 从两边海岸多源 BFS 往高处爬，取交集
##### ! 时间复杂度: O(m·n)   空间复杂度: O(m·n)
##### ! 适用：和 DFS 等价、不怕递归深度；两条海岸线各自当多源起点一起入队（函数名叫 dfs，其实是用 deque 的 BFS）
##################################################################################################


class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        m = len(heights)
        n = len(heights[0])
        pacific = [(0, y) for y in range(n)] + [(x, 0) for x in range(1, m)]
        atlantic = [(m - 1, y) for y in range(n)] + [(x, n - 1) for x in range(m - 1)]

        def dfs(points):
            q = deque(points)
            seen = set(points)
            while q:
                x, y = q.popleft()
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < m and 0 <= ny < n and (nx, ny) not in seen and heights[nx][ny] >= heights[x][y]:
                        seen.add((nx, ny))
                        q.append((nx, ny))
            return seen

        return list(dfs(pacific) & dfs(atlantic))


##################################################################################################
##### ! Solution 2: 从两边海岸递归 DFS 往高处爬，取交集
##### ! 时间复杂度: O(m·n)   空间复杂度: O(m·n)（两张 seen 表 + 递归栈）
##### ! 适用：手册里的模板名就是边界反向 DFS，最短最常考；m·n ≤ 4e4，LeetCode 递归上限够用
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_2:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        m, n = len(heights), len(heights[0])
        pac = [[False] * n for _ in range(m)]
        atl = [[False] * n for _ in range(m)]

        def dfs(x: int, y: int, seen: List[List[bool]]) -> None:
            seen[x][y] = True
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                # ! 反向爬：只走不比当前矮的邻居，这样邻居的水才流得到这里
                if 0 <= nx < m and 0 <= ny < n and not seen[nx][ny] and heights[nx][ny] >= heights[x][y]:
                    dfs(nx, ny, seen)

        for x in range(m):  # ! 左边一列属于太平洋，右边一列属于大西洋
            dfs(x, 0, pac)
            dfs(x, n - 1, atl)
        for y in range(n):  # ! 上边一行属于太平洋，下边一行属于大西洋
            dfs(0, y, pac)
            dfs(m - 1, y, atl)

        return [[x, y] for x in range(m) for y in range(n) if pac[x][y] and atl[x][y]]  # ! 取交集


s = Solution()
# fmt: off
input_ = [
  [4,2,7,3,4],
  [7,4,6,4,7],
  [6,3,5,3,6]
]
# fmt: on
result = s.pacificAtlantic(input_)
print(result)
