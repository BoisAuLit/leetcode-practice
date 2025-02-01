from typing import List
import heapq


class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        heapq.heapify(nums)
        self.data = nums

        while True:
            if len(self.data) > self.k:
                heapq.heappop(self.data)
            else:
                break

    def add(self, val: int) -> int:
        heapq.heappush(self.data, val)
        if len(self.data) > self.k:
            heapq.heappop(self.data)
        return self.data[0]



s = KthLargest(3, [4, 5, 8, 2])
print(s.add(3))
print(s.add(5))
print(s.add(10))
print(s.add(9))
print(s.add(4))
