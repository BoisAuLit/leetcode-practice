from collections import deque

from typing import List


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
