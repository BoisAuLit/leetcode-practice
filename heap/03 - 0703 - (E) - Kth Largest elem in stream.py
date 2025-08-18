from typing import List
import heapq


class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.heap = []
        for num in nums:
            self.add(num)

    def add(self, val: int) -> int:
        if len(self.heap) <= self.k - 1:
            heapq.heappush(self.heap, val)
        else:
            heapq.heappushpop(self.heap, val)
        return self.heap[0]


k = 3
nums = [4, 5, 8, 2]

s = KthLargest(k, nums)
print(s.add(3))
print(s.add(5))
print(s.add(10))
print(s.add(9))
print(s.add(4))
