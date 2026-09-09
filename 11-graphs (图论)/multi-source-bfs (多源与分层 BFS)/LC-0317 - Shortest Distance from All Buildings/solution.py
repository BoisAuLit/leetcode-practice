from collections import deque
from typing import List


class Solution:
    def shortestDistance(self, grid: List[List[int]]) -> int:
        # 四个方向
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        rows, cols = len(grid), len(grid[0])
        # 记录每个空地到所有房子的总距离
        total = [[0] * cols for _ in range(rows)]

        empty_land_value = 0
        min_dist = float("inf")

        for row in range(rows):
            for col in range(cols):
                # 从每一栋房子做一次 BFS
                if grid[row][col] == 1:
                    min_dist = float("inf")
                    q = deque([(row, col)])
                    steps = 0

                    while q:
                        steps += 1
                        for _ in range(len(q)):
                            cr, cc = q.popleft()

                            for dr, dc in dirs:
                                nr, nc = cr + dr, cc + dc

                                # 只访问当前“轮次”还没访问过的空地
                                if (
                                    0 <= nr < rows
                                    and 0 <= nc < cols
                                    and grid[nr][nc] == empty_land_value
                                ):
                                    grid[nr][nc] -= 1
                                    total[nr][nc] += steps
                                    q.append((nr, nc))
                                    min_dist = min(min_dist, total[nr][nc])

                    # 下一栋房子只会走到 grid 值为 empty_land_value 的格子
                    empty_land_value -= 1

        return -1 if min_dist == float("inf") else min_dist
