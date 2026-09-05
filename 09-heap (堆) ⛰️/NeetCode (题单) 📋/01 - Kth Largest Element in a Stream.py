from typing import List

import heapq


class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.heap = []
        for val in nums:
            self.add(val)

    def add(self, val: int) -> int:
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, val)
        else:
            if val > self.heap[0]:
                heapq.heappop(self.heap)
                heapq.heappush(self.heap, val)
        return self.heap[0]
