from typing import List


class Solution:
    def getMaxLen(self, nums: List[int]) -> int:
        max_streak = 0
        index = 0
        while index < len(nums):
            while index < len(nums) and nums[index] == 0:
                index += 1
            if index == len(nums):
                break
            start_index = index
            negative_indces = []
            while index < len(nums) and nums[index] != 0:
                if nums[index] < 0:
                    negative_indces.append(index)
                index += 1
            partial_max = -1
            if len(negative_indces) % 2 == 0:
                partial_max = index - start_index
            else:
                partial_max = max(
                    index - negative_indces[0]-1,
                    negative_indces[-1] - start_index,
                )
            max_streak = max(max_streak, partial_max)

        return max_streak

s = Solution()
input_ = [1,-2,-3,4] # Expecting 4
input_ = [0,1,-2,-3,-4] # Expecting 3
input_ = [-1,-2,-3,0,1] # Expecting 2
result = s.getMaxLen(input_)
print(result)
