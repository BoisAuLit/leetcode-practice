from typing import List
import heapq


class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        max_heap = [-x for x in stones]
        heapq.heapify(max_heap)

        while True:
            if len(max_heap) == 0:
                return 0
            elif len(max_heap) == 1:
                return -max_heap[0]

            x = heapq.heappop(max_heap)
            y = heapq.heappop(max_heap)
            if x != y:
                heapq.heappush(max_heap, -abs(x - y))


s = Solution()
stones = [2, 7, 4, 1, 8, 1]
result = s.lastStoneWeight(stones)
print(result)
