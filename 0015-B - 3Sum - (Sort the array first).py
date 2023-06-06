from typing import List

"""
Time complexity: O(n2)
Space complexity: From O(logn) to O(n)
"""

class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        start = 0
        end = len(numbers) - 1
        result = []
        while True and start < end:
            sum_ = numbers[start] + numbers[end]
            if sum_ > target:
                end -= 1
            elif sum_ < target:
                start += 1
            else:
                result.append([numbers[start], numbers[end]])
                while start < len(numbers) - 1 and numbers[start] == numbers[start + 1]:
                    start += 1
                while end > 0 and numbers[end] == numbers[end - 1]:
                    end -= 1
                start += 1
                end -= 1
        return result

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        result = []
        nums = sorted(nums)
        i = 0
        while i < len(nums) - 1:
            twoSumResult = self.twoSum(nums[i + 1 :], -nums[i])
            result.extend([nums[i], item[0], item[1]] for item in twoSumResult)
            while i < len(nums) - 1 and nums[i] == nums[i + 1]:
                i += 1
            i += 1
        return result


# ⭐️⭐️⭐️⭐️ Testing twoSum ⭐️⭐️⭐️
# s = Solution()
# input_ = [1, 3, 3, 5]
# result = s.twoSum(input_, 6)
# print(result)

# ⭐️⭐️⭐️⭐️ Testing threeSum ⭐️⭐️⭐️
s = Solution()
input_ = [-1, 0, 1, 2, -1, -4]
result = s.threeSum(input_)
print(result)
