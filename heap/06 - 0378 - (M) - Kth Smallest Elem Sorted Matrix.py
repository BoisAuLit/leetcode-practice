from typing import List
import heapq


class Solution:
    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
        n = len(matrix)
        max_heap = []
        for i in range(n):
            for j in range(n):
                if len(max_heap) <= k - 1:
                    heapq.heappush(max_heap, -matrix[i][j])
                else:
                    heapq.heappushpop(max_heap, -matrix[i][j])
        return -max_heap[0]


s = Solution()
matrix = [[1, 5, 9], [10, 11, 13], [12, 13, 15]]
k = 8
result = s.kthSmallest(matrix, k)
print(result)
