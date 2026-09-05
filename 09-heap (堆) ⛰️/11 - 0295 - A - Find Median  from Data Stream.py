from heapq import heappush, heappop

"""
When a new number arrives, we need to decide:

Should it go to the "smaller half" (lo) or "larger half" (hi)?
How do we maintain the balance between the two heaps?

*****************************************************************

Initial state:
lo (max heap): [35, 4]     hi (min heap): [41, 62]
                ↑                          ↑
              largest                   smallest
              in lo                     in hi

Add 100 (a large number that should end in upper half):
1. lo = [100, 35, 4]  ← 100 becomes the new largest
2. Move largest (100) to hi: lo = [35, 4], hi = [41, 62, 100]
3. Balance if needed

Add 10 (a small number that should end in lower half):  
1. lo = [35, 10, 4]  ← 35 is still the largest
2. Move largest (35) to hi: lo = [10, 4], hi = [35, 41, 62]
3. Balance: move 35 back to lo = [35, 10, 4], hi = [41, 62]
"""


class MedianFinder:
    def __init__(self):
        self.lo = []
        self.hi = []

    def addNum(self, num):
        """
        This sequence ensures that:

        If num is small, it stays in lo (smaller half)
        If num is large, it gets "bubbled up" and moved to hi (larger half)
        """
        heappush(self.lo, -num)  
        heappush(self.hi, -self.lo[0])
        heappop(self.lo)

        if len(self.lo) < len(self.hi):
            heappush(self.lo, -self.hi[0])
            heappop(self.hi)

    def findMedian(self):
        """
        The median is always either:

        The top of lo (if lo has more elements)
        The average of the tops of both heaps (if they have equal size)
        """
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        else:
            return (self.hi[0] - self.lo[0]) / 2  # - as low has -ve values
