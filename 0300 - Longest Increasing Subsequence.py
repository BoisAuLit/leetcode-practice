from typing import List
from bisect import bisect_left

"""
Time complexity: O()
Space complexity: O()
"""

class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        sub = []
        for num in nums:
            i = bisect_left(sub, num)

            # If num is greater than any element in sub
            if i == len(sub):
                sub.append(num)
            
            # Otherwise, replace the first element in sub greater than or equal to num
            else:
                sub[i] = num
        
        return len(sub)


s = Solution()
input_ = [10,9,2,5,3,7,101,18] # 4
# input_ = [0,1,0,3,2,3] # 4
# input_ = [7,7,7,7,7,7,7] # 1
result = s.lengthOfLIS(input_)
print(result)
