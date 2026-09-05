from typing import List
from collections import Counter
import heapq


class Solution_1:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        return [x[0] for x in Counter(nums).most_common(k)]


class Solution_2:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        frequency = Counter(nums)
        heap = []
        for num, count in frequency.items():
            if len(heap) <= k - 1:
                heapq.heappush(heap, (count, num))
            else:
                heapq.heappushpop(heap, (count, num))
        return [x[1] for x in heap]


class Solution_3:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = Counter(nums)
        return heapq.nlargest(k, count.keys(), key=count.get)


# s = Solution()
# nums = [1, 1, 1, 2, 2, 3]
# k = 2
# result = s.topKFrequent(nums, k)
# print(result)
