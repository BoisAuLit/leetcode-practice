from typing import List
import heapq


class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        heap = []
        for x, y in points:
            dist = x * x + y * y
            if len(heap) < k:
                heapq.heappush(heap, (-dist, x, y))
            else:
                if dist < -heap[0][0]:
                    heapq.heappop(heap)
                    heapq.heappush(heap, (-dist, x, y))
        return [(x, y) for _, x, y in heap]


s = Solution()
points = [[0,2],[2,0],[2,2]]
k = 2
result = s.kClosest(points, k)
print(result)
