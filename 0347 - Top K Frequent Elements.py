from typing import List
from collections import Counter
import heapq

"""
Time complexity: O(NlogK)
Space complexity: O()
"""



class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]: 
        # O(1) time 
        if k == len(nums):
            return nums
        
        # 1. Build hash map: character and how often it appears
        # O(N) time
        count = Counter(nums)   
        # 2-3. Build heap of top k frequent elements and
        # convert it into an output array
        # O(N log k) time
        return heapq.nlargest(k, count.keys(), key=count.get) 


s = Solution()
input_ = [1, 1, 1, 2, 2, 3]
result = s.topKFrequent(input_, 2)
print(result)
