from typing import List


class Solution:
    def largestDivisibleSubset(self, nums: List[int]) -> List[int]:
        nums.sort()
        mapping = dict()
        max_length = 1
        target_number = nums[-1]

        for i in range(len(nums) - 1, -1, -1):
            mapping[nums[i]] = {"next": None, "max_length": 1}

            max_succ_length = 0
            for j in range(i + 1, len(nums)):
                if (
                    nums[j] % nums[i] == 0
                    and mapping[nums[j]]["max_length"] > max_succ_length
                ):
                    max_succ_length = mapping[nums[j]]["max_length"]
                    mapping[nums[i]]["next"] = nums[j]
            mapping[nums[i]]["max_length"] = max_succ_length + 1

            if mapping[nums[i]]["max_length"] > max_length:
                max_length = mapping[nums[i]]["max_length"]
                target_number = nums[i]
        result = []
        current_number = target_number
        while current_number in mapping:
            result.append(current_number)
            current_number = mapping[current_number]["next"]
        return result


s = Solution()
nums = [2, 3, 6, 12, 18, 24, 36, 54, 120, 240, 480, 486, 960, 972, 1440, 2880]
result = s.largestDivisibleSubset(nums)
print(result)
