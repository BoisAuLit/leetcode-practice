from typing import List
import heapq


class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        max_heap = []

        for x, y in points:
            distance = x * x + y * y
            if len(max_heap) <= k - 1:
                heapq.heappush(max_heap, (-distance, [x, y]))
            else:
                heapq.heappushpop(max_heap, (-distance, [x, y]))
        return [x[1] for x in max_heap]


s = Solution()
points = [[3, 3], [5, -1], [-2, 4]]
k = 2
result = s.kClosest(points, k)
print(result)
