from typing import List


class Solution:
    def twoSumII(
        self, i: int, nums: List[int], result: List[int]
    ) -> List[List[int]]:
        lo, hi = i + 1, len(nums) - 1
        while lo < hi:
            sum = nums[i] + nums[lo] + nums[hi]
            if sum < 0:
                lo += 1
            elif sum > 0:
                hi -= 1
            else:
                # ! 这里很容易出错，不要携程[i, lo, hi]
                result.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                hi -= 1

                # ! 这里的剪枝很容易忘记
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        result = []

        # ! 这里很容易出错，很容易忘记 sort
        nums.sort()
        for i in range(len(nums) - 2):

            # ! 这里的剪枝很容易忘记
            if nums[i] > 0:
                break
            # ! 这里的剪枝也很容易忘记
            if i == 0 or nums[i] != nums[i - 1]:
                self.twoSumII(i, nums, result)
        return result
