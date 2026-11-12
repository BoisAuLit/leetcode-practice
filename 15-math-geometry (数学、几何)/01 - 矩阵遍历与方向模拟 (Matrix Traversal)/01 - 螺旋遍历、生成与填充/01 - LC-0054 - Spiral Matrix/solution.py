from typing import List


class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        m, n = len(matrix), len(matrix[0])
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        d = 0
        x, y = 0, -1                      # 起点:第一格的门口(沿用你的设计,很聪明)
        visited = set()
        res = []
        for _ in range(m * n):            # 恰好走 m*n 步,走满即止
            nx, ny = x + dirs[d][0], y + dirs[d][1]
            if not (0 <= nx < m and 0 <= ny < n) or (nx, ny) in visited:
                d = (d + 1) % 4           # 撞墙:右转一次(一次必然够)
                nx, ny = x + dirs[d][0], y + dirs[d][1]
            x, y = nx, ny
            visited.add((x, y))
            res.append(matrix[x][y])
        return res

s = Solution()
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
result = s.spiralOrder(matrix)
print(result)
