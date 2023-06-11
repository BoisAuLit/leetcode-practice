from typing import List

"""
Time complexity: O(n)
Space complexity: O(1)
"""


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        i = 0
        pointer = 0

        while i < len(nums) - 1:
            tmp = nums[i]
            while i < len(nums) - 1 and nums[i] == nums[i + 1]:
                i += 1
            nums[pointer] = tmp
            pointer += 1
            i += 1

        if i == len(nums):
            return pointer
        nums[pointer] = nums[-1]
        return pointer + 1


s = Solution()
# input_ = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
# input_ = [1, 1, 2]
input_ = [1, 1]
result = s.removeDuplicates(input_)
print(result)
print(input_)


"""
Runtime
- 97 ms
- Beats 66.96%

Memory
- 17.9 MB
- Beats 46.32%
"""
