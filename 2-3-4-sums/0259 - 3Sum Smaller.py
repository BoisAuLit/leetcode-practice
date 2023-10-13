from typing import List

"""
Time complexity: O(N²)
Space complexity: O(1)
"""

class Solution:
    def threeSumSmaller(self, nums: List[int], target: int) -> int:
        nums.sort()
        count = 0
        for i in range(len(nums)-2):
            lo, hi = i + 1, len(nums) - 1
            if nums[lo] + nums[lo+1] + nums[i] >= target:
                continue
            if nums[hi] + nums[hi-1] + nums[i] < target:
                count += (hi-lo+1) * (hi-lo) // 2
                continue
            while lo < hi:
                sum_ = nums[i] + nums[lo] + nums[hi]
                if sum_ < target:
                    count += hi - lo
                    lo += 1
                else:
                    hi -= 1
                    
        return count

s = Solution()

# Expection 2
nums = [-2,0,1,3]
target = 2

# Expection 3
nums = [-2,0,1,3]
target = 4


result = s.threeSumSmaller(nums, target)
print(result)
