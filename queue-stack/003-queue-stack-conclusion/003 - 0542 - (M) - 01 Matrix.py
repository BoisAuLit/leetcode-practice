from typing import List
from collections import deque


class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        m = len(mat)
        n = len(mat[0])
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        visited = {(x, y) for x in range(m) for y in range(n) if mat[x][y] == 0}
        queue = deque(visited)
        distance = 0
        while queue:
            new_queue = deque()
            while queue:
                x, y = queue.popleft()
                mat[x][y] = distance
                for dx, dy in directions:
                    x1, y1 = x + dx, y + dy
                    if 0 <= x1 < m and 0 <= y1 < n and (x1, y1) not in visited:
                        visited.add((x1, y1))
                        new_queue.append((x1, y1))
            queue = new_queue
            distance += 1

        return mat


s = Solution()


# Test case 1: Expecting [[0,0,0],[0,1,0],[1,2,1]]
input_ = [[0, 0, 0], [0, 1, 0], [1, 1, 1]]


result = s.updateMatrix(input_)
print(result)
