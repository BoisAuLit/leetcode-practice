from typing import List
from collections import defaultdict, deque
from math import inf


class Solution:
    def minMoves(self, matrix: List[str]) -> int:
        m, n = len(matrix), len(matrix[0])
        teleports = defaultdict(list)
        for r in range(m):
            for c in range(n):
                if matrix[r][c].isalpha():
                    teleports[matrix[r][c]].append((r, c))

        dist = [[inf] * n for _ in range(m)]
        dist[0][0] = 0
        dq = deque([(0, 0, 0)])  # (距离, r, c)
        directions = ((0, 1), (0, -1), (1, 0), (-1, 0))
        while dq:
            d, r, c = dq.popleft()
            if d > dist[r][c]:  # 过期条目
                continue
            if (r, c) == (m - 1, n - 1):
                return d
            ch = matrix[r][c]
            if ch in teleports:  # ! 0 权边：同字母的所有格子放队头，距离不变；这种字母用完就删
                for nr, nc in teleports.pop(ch):
                    if d < dist[nr][nc]:
                        dist[nr][nc] = d
                        dq.appendleft((d, nr, nc))
            for dr, dc in directions:  # ! 1 权边：放队尾
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] != "#" and d + 1 < dist[nr][nc]:
                    dist[nr][nc] = d + 1
                    dq.append((d + 1, nr, nc))
        return -1


# Test case 1: Expecting 2
s = Solution()
matrix = ["A..", ".A.", "..."]
result = s.minMoves(matrix)
print(result)

# Test case 2: Expecting 0 (Special case)
s = Solution()
matrix = ["."]
result = s.minMoves(matrix)
print(result)

# Test case 3: Expecting 1 (Special case)
s = Solution()
matrix = [".A", "CA"]
result = s.minMoves(matrix)
print(result)

# Test case 4: Expecting 3 (Special case)
s = Solution()
matrix = ["..G", "C.D", ".EE"]
result = s.minMoves(matrix)
print(result)
