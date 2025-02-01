from typing import List
import heapq


class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        data = [-x for x in stones]
        heapq.heapify(data)

        while True:
            if len(data) == 1:
                return -data[0]
            if len(data) == 0:
                return 0
            first = heapq.heappop(data)
            second = heapq.heappop(data)
            diff = abs(first - second)
            if diff != 0:
                heapq.heappush(data, -diff)


s = Solution()

# Test case 1: Expecting 1
stones = [2, 7, 4, 1, 8, 1]
result = s.lastStoneWeight(stones)
print(result)
