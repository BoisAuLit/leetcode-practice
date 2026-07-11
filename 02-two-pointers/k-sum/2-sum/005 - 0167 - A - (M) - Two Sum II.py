from typing import List

"""
Time complexity: O(n)
Space complexity: O(1)
"""


class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        lo = 0
        hi = len(numbers) - 1
        while lo < hi:
            curr = numbers[lo] + numbers[hi]
            if curr > target:
                hi -= 1
            elif curr < target:
                lo += 1
            else:
                return [lo + 1, hi + 1]


s = Solution()
input_ = [2, 3, 4]
result = s.twoSum(input_, 6)
print(result)
