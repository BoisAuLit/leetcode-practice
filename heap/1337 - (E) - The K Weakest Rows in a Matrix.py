from typing import List
import heapq


class Solution:
    def kWeakestRows(self, mat: List[List[int]], k: int) -> List[int]:
        data = []
        m = len(mat)
        n = len(mat[0])
        for row in range(m):
            soldiers = 0
            for col in range(n):
                if mat[row][col] == 1:
                    soldiers += 1
            data.append([soldiers, row])
        print(data)
        heapq.heapify(data)
        result = []
        for _ in range(k):
            smallest = heapq.heappop(data)[1]
            result.append(smallest)
        return result


s = Solution()
mat = [
    [1, 1, 0, 0, 0],
    [1, 1, 1, 1, 0],
    [1, 0, 0, 0, 0],
    [1, 1, 0, 0, 0],
    [1, 1, 1, 1, 1],
]
k = 3
result = s.kWeakestRows(mat, 3)
print(result)
