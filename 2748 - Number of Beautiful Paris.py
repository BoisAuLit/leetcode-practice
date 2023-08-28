from typing import List
import math


class Solution:
    def countBeautifulPairs(self, nums: List[int]) -> int:
        count = 0
        for i in range(len(nums) - 1):
            for j in range(i + 1, len(nums)):
                if math.gcd(int(str(nums[i])[0]), int(str(nums[j])[-1])) == 1:
                    count += 1
        return count


s = Solution()

# Expecting 5
# input_ = [2, 5, 1, 4]

# Expecting 7
input_ = [31, 25, 72, 79, 74]


result = s.countBeautifulPairs(input_)
print(result)

"""

"""
