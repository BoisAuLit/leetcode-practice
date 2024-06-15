from typing import List

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def jump(self, nums: List[int]) -> int:
        res = 0
        l = r = 0
        while r < len(nums) - 1:
            farthest = 0
            for i in range(l, r + 1):
                farthest = max(farthest, nums[i])
            l = r + 1
            r = farthest
            res += 1
        return res


s = Solution()
nums = [2, 3, 0, 1, 4]
result = s.jump(nums)
print(result)
