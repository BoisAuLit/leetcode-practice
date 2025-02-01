from typing import List
from collections import Counter
import heapq


# ! Using max heap
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        counter = Counter(nums)
        data = [(-count, num) for num, count in counter.items()]
        heapq.heapify(data)
        result = []
        for _ in range(k):
            top = heapq.heappop(data)[1]
            result.append(top)
        return result



# ! Using python builtin functions
# class Solution:
#     def topKFrequent(self, nums: List[int], k: int) -> List[int]:
#         counter = Counter(nums)

#         print(counter.most_common(k))
#         return [x[0] for x in counter.most_common(k)]

s = Solution()


nums = [1,1,1,2,2,3]
k = 2


result = s.topKFrequent(nums, k)
print(result)
