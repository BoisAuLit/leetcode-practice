from typing import List


class Solution:
    def maximumUniqueSubarray(self, nums: List[int]) -> int:
        left = 0
        sum_ = nums[0]
        max_ = sum_
        seen = set([nums[0]])
        for right in range(1, len(nums)):
            num = nums[right]
            if num in seen:
                while nums[left] != num:
                    sum_ -= nums[left]
                    seen.remove(nums[left])
                    left += 1
                left += 1
            else:
                sum_ += num
                seen.add(num)
                max_ = max(max_, sum_)
        return max_


s = Solution()
nums = [5, 2, 1, 2, 5, 2, 1, 2, 5]
result = s.maximumUniqueSubarray(nums)
print(result)
