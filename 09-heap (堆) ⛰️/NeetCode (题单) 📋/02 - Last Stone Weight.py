from typing import List
import heapq


class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        heap = []
        for stone in stones:
            heapq.heappush(heap, -stone)
        while len(heap) >= 2:
            x = -heapq.heappop(heap)
            y = -heapq.heappop(heap)
            diff = abs(x - y)
            if diff > 0:
                heapq.heappush(heap, -diff)
        return -heap[0] if heap else 0
