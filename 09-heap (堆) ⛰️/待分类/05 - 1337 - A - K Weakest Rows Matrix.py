from typing import List
import heapq


class Solution:
    def kWeakestRows(self, mat: List[List[int]], k: int) -> List[int]:
        m = len(mat)
        n = len(mat[0])
        max_heap = []

        def score(i: int) -> int:
            return sum(mat[i]) * (max(m, n) + 1) + i

        for i in range(len(mat)):
            s = score(i)
            if len(max_heap) < k:
                heapq.heappush(max_heap, (-s, i))
            elif s < -max_heap[0][0]:
                heapq.heappushpop(max_heap, (-s, i))

        print(max_heap)
        return [x[1] for x in sorted(max_heap, reverse=True)]


s = Solution()
mat = [
    [1, 1, 0, 0, 0],
    [1, 1, 1, 1, 0],
    [1, 0, 0, 0, 0],
    [1, 1, 0, 0, 0],
    [1, 1, 1, 1, 1],
]

k = 3
result = s.kWeakestRows(mat, k)
print(result)
