from typing import List
import heapq


class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)
        dist = [[float("inf")] * n for _ in range(n)]
        dist[0][0] = grid[0][0]
        heap = [(grid[0][0], 0, 0)]  # (到达此格所需水位, x, y)

        while heap:
            cost, x, y = heapq.heappop(heap)
            if x == n - 1 and y == n - 1:
                return cost  # 第一次弹出终点，cost 就是答案
            if cost > dist[x][y]:
                continue  # 过期条目
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n:
                    new_cost = max(cost, grid[nx][ny])  # ← 唯一的本质修改
                    if new_cost < dist[nx][ny]:
                        dist[nx][ny] = new_cost
                        heapq.heappush(heap, (new_cost, nx, ny))


s = Solution()
# fmt: off
grid = [
  [0,1,2,10],
  [9,14,4,13],
  [12,3,8,15],
  [11,5,7,6]
]
# fmt: on
result = s.swimInWater(grid)
print(result)
