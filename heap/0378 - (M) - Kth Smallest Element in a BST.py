from typing import List
import heapq


class Solution:
    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
        data = []
        n = len(matrix)
        for i in range(n):
            for j in range(n):
                heapq.heappush(data, -matrix[i][j])
                if len(data) > k:
                    heapq.heappop(data)
        return -data[0]


s = Solution()

# Test case 1: Expecting 13
matrix = [[1, 5, 9], [10, 11, 13], [12, 13, 15]]
k = 8

result = s.kthSmallest(matrix, k)
print(result)
