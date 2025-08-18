from typing import List
import heapq


class Solution:
    def connectSticks(self, sticks: List[int]) -> int:
        heap = sticks
        heapq.heapify(heap)
        cost = 0
        while heap:
            if len(heap) == 1:
                return cost
            x = heapq.heappop(heap)
            y = heapq.heappop(heap)
            heapq.heappush(heap, x + y)
            cost += x + y


s = Solution()
sticks = [1, 8, 3, 5]
result = s.connectSticks(sticks)
print(result)
