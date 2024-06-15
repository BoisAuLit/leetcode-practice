from typing import List
import math

"""
Time complexity: O()
Space complexity: O()
"""

class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:  
        left = 1
        right = max(piles)
        
        while left < right:
            middle = (left + right) // 2            
            hour_spent = 0
            
            for pile in piles:
                hour_spent += math.ceil(pile / middle)
            if hour_spent <= h:
                right = middle
            else:
                left = middle + 1
        return right


s = Solution()

# 4
piles = [3, 6, 7, 11]
h = 8

# #30
# piles = [30,11,23,4,20]
# h = 5

result = s.minEatingSpeed(piles, h)
print(result)
