from typing import List

"""
Time complexity: O(n)
Space complexity: O(1)
"""


class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        start = 0
        end = len(numbers) - 1
        while start < end:
            sum_ = numbers[start] + numbers[end]
            if sum_ > target:
                end -= 1
            elif sum_ < target:
                start += 1
            else:
                return [start + 1, end + 1]


s = Solution()
input_ = [2, 3, 4]
result = s.twoSum(input_, 6)
print(result)
