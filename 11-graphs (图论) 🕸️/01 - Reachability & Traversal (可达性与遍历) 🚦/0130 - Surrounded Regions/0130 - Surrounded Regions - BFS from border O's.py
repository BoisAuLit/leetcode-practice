"""
📌 信号→模式: 被包围的 O 翻转 → 反向思维：从边界 O 出发 BFS/DFS 标记"不翻"，其余全翻
📅 首次: 2026-09-04 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 未排期
"""
from typing import List
from collections import deque
from pprint import pprint


class Solution:
    def solve(self, board: List[List[str]]) -> None:
        m = len(board)
        n = len(board[0])

        regions = set()
        q = deque()
        seen = set()
        for x in range(m):
            for y in range(n):
                if board[x][y] == "O":
                    regions.add((x, y))
                    if x == 0 or x == m - 1 or y == 0 or y == n - 1:
                        q.append((x, y))
                        seen.add((x, y))

        while q:
            x, y = q.popleft()
            regions.remove((x,y))
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and board[nx][ny] == "O" and (nx, ny) not in seen:
                    seen.add((nx, ny))
                    q.append((nx, ny))
        for x, y in regions:
            board[x][y] = "X"


s = Solution()
# fmt: off
input_ = [
  ["X","X","X","X"],
  ["X","O","O","X"],
  ["X","X","O","X"],
  ["X","O","X","X"]
]
# fmt: on
pprint(input_)
result = s.solve(input_)
print()
pprint(input_)
