from typing import List
from collections import defaultdict

"""
Time complexity: O(n)
Space complexity: O(n)
"""

class Solution:
    def findErrorNums(self, nums: List[int]) -> List[int]:
        sum2 = 0
        occurrences = defaultdict(int)
        n = len(nums)
        for num in nums:
            sum2 += num
            occurrences[num] += 1
            if occurrences[num] == 2:
                a = num
        b =  a +  n * (n+1) // 2 - sum2
        return [a, b]
        
        

s = Solution()
input_ = [1,2,2,4]
result = s.findErrorNums(input_)
print(result)

