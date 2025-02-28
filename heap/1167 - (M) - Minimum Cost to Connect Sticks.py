from typing import List
import heapq


class Solution:
    def connectSticks(self, sticks: List[int]) -> int:
        heapq.heapify(sticks)
        cost = 0
        while len(sticks) != 1:
            x = heapq.heappop(sticks)
            y = heapq.heappop(sticks)
            cost += x + y
            heapq.heappush(sticks, x + y)

        return cost


s = Solution()

# Test case 1: Expecting 14
# input_ = [2, 3, 4]

# Test case 2: Expecting 30
input_ = [1,8,3,5]

result = s.connectSticks(input_)
print(result)
