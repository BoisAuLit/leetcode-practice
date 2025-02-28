from typing import List
import heapq


class Solution:
    def furthestBuilding(self, heights: List[int], bricks: int, ladders: int) -> int:
        acc = 0
        data = []
        for i in range(1, len(heights)):
            if heights[i] <= heights[i-1]:
                continue
            
            jump = heights[i] - heights[i-1]
            heapq.heappush(data, -jump)
            acc += jump
            if acc <= bricks:
                continue

            if ladders == 0:
                return i-1
            biggest = -heapq.heappop(data)
            acc -= biggest
            ladders -= 1
        return len(heights) - 1




s = Solution()

# Test case 1: Expecting 7
heights = [4,12,2,7,3,18,20,3,19]
bricks = 10
ladders = 2


result = s.furthestBuilding(heights, bricks, ladders)
print(result)
