from typing import List

"""
Time complexity: O()
Space complexity: O()

1. 从后往前, 找到第一个降序 A(x)
2. 从后往前, 找到第一个比 A(x) 大的数 A(y)
3. 交换 A(x), A(y)
4. 将 x 之后的数字重新排序
"""


class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        i = len(nums) - 2
        while i >= 0 and nums[i + 1] <= nums[i]:
            i -= 1
        if i == -1:
            nums.reverse()
            return
        j = len(nums) - 1
        while j >= 0 and nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]
        nums[i + 1 :] = nums[len(nums) - 1 : i : -1]


s = Solution()

# Expecting [1,5,8,5,1,3,4,6,7]
input_ = [1, 5, 8, 4, 7, 6, 5, 3, 1]
result = s.nextPermutation(input_)

print(input_)

"""

"""
