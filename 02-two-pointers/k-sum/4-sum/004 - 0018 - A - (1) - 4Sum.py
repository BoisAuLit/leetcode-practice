from typing import List

"""
Time complexity: O(N3)
Space complexity: O()


本题的 twoSum() 部分之所以不采用 Leetcode 167 的解法（以下），是因为
- 本题的 twoSum（）是要考虑去重问题的
- 而 Leetcode 167 有唯一解（如下）
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
"""


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[List[int]]:
        res = []
        lo = 0
        hi = len(nums) - 1

        while lo < hi:
            curr = nums[lo] + nums[hi]
            if curr < target or (lo > 0 and nums[lo] == nums[lo - 1]):
                lo += 1
            elif curr > target or (
                hi < len(nums) - 1 and nums[hi] == nums[hi + 1]
            ):
                hi -= 1
            else:
                res.append([nums[lo], nums[hi]])
                lo += 1
                hi -= 1

        return res

    def kSum(self, nums: List[int], target: int, k: int) -> List[List[int]]:
        res = []

        if not nums:
            return res

        average_value = target // k

        if average_value < nums[0] or nums[-1] < average_value:
            return res

        if k == 2:  # Base case
            return self.twoSum(nums, target)

        for i in range(len(nums)):
            if i == 0 or nums[i - 1] != nums[i]:
                for subset in self.kSum(nums[i + 1 :], target - nums[i], k - 1):
                    res.append([nums[i]] + subset)

        return res

    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        return self.kSum(nums, target, 4)


s = Solution()

# Expecting [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]
nums = [1, 0, -1, 0, -2, 2]
target = 0

nums = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
target = 8

result = s.fourSum(nums, target)
print(result)
