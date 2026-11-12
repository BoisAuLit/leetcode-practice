"""LC-0994 - Rotting Oranges

阶段 1 · DFS、BFS（静态无权的连通性与步数）· 多源 BFS（所有起点一起入队）★ 签名题
题目在问：腐烂传播到所有新鲜橘子需要几分钟，传不到就 -1
点是什么：一个橘子格   边是什么：上下左右相邻，传播一分钟
和签名题比改了哪一行：本题就是多源 BFS 签名题；所有烂橘子一开始一起进队列，一层 = 一分钟
"""
from collections import deque

from typing import List


##################################################################################################
##### ! Solution 1: 多源 BFS 按层计数
##### ! 时间复杂度: O(m·n)   空间复杂度: O(m·n)
##### ! 适用：层数 = 分钟数的标准模板；fresh 计数既用来提前停，也用来判 -1
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:

        m = len(grid)
        n = len(grid[0])
        q = deque()
        fresh = 0
        # 初始化：所有烂橘子一起作为 BFS 起点
        for x in range(m):
            for y in range(n):
                if grid[x][y] == 1:
                    fresh += 1
                elif grid[x][y] == 2:
                    q.append((x, y))

        # ! 没有新鲜橘子 - 这一点很重要
        if fresh == 0:
            return 0

        minutes = 0

        """
        while q and fresh > 0: 可以在所有新鲜橘子都已经腐烂之后，立刻停止 BFS。

        如果只写：
        也能做对，但队列里可能还剩一些“刚刚变烂的橘子”等着被弹出处理，而此时已经没有任何 fresh orange 了，这些处理其实是多余的。
        """
        while q and fresh > 0:
            for _ in range(len(q)):
                x, y = q.popleft()
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == 1:
                        grid[nx][ny] = 2
                        fresh -= 1
                        q.append((nx, ny))
            minutes += 1

        return minutes if fresh == 0 else -1


##################################################################################################
##### ! Solution 2: 多源 BFS，把腐烂时刻写进格子
##### ! 时间复杂度: O(m·n)   空间复杂度: O(m·n)
##### ! 适用：不数层，时刻直接从父格 +1 得来（和 542 一个写法）；要知道每个格子各自的时间时用它
##################################################################################################


class Solution_2:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        q = deque((x, y) for x in range(m) for y in range(n) if grid[x][y] == 2)  # ! 所有烂橘子一起入队
        minutes = 0
        while q:
            x, y = q.popleft()
            minutes = max(minutes, grid[x][y] - 2)  # ! 格子里存的是 2 + 腐烂时刻，起点的 2 就是第 0 分钟
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == 1:
                    grid[nx][ny] = grid[x][y] + 1  # ! 时刻 = 父格 + 1，写进去的同时也完成了标记
                    q.append((nx, ny))
        return -1 if any(1 in row for row in grid) else minutes  # ! 还剩 1 就是传不到


s = Solution()
# fmt: off
grid = [
    [1,1,0],
    [0,1,1],
    [0,1,2]
]
# fmt: on
result = s.orangesRotting(grid)
print(result)
