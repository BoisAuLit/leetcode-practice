from typing import List
import heapq

"""
M --> Number of calls to add()
N --> Length of nums

Time complexity: O(N﹒log(N) + M﹒log(k))
Space complexity: O(N)
"""

class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.minHeap = nums
        heapq.heapify(self.minHeap)
        while len(self.minHeap) > k:
            heapq.heappop(self.minHeap)

    def add(self, val: int) -> int:
        heapq.heappush(self.minHeap, val)
        if len(self.minHeap) > self.k:
            heapq.heappop(self.minHeap)
        return self.minHeap[0]



s = KthLargest(3, [4, 5, 8, 2])
print(s.add(3))
print(s.add(5))
print(s.add(10))
print(s.add(9))
print(s.add(4))


"""
Runtime
- 82ms
- Beats 96.97%

Memory
20.34mb
- Beats 67.18%
"""
