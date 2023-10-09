from typing import List

"""
Time complexity: O(N)
Space complexity: O(N)
"""

class Solution:
    def longestConsecutive(self, nums):
        longest_streak = 0
        num_set = set(nums)

        for num in num_set:
            if num - 1 not in num_set:
                current_num = num
                current_streak = 1

                while current_num + 1 in num_set:
                    current_num += 1
                    current_streak += 1

                longest_streak = max(longest_streak, current_streak)

        return longest_streak


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        mapping = {num: {"visited": False, "acc": 1} for num in nums}
        longest = 0
        for num in nums:
            if mapping[num]['visited']:
                continue
            acc = 0
            originalNum = num
            while num in mapping:
                acc += mapping[num]["acc"]
                if mapping[num]["visited"]:
                    break
                mapping[num]["visited"] = True
                num -= 1
                
            mapping[originalNum]["acc"] = acc
            if acc > longest:
                longest = acc
        return longest




s = Solution()
# nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
nums = [100, 4, 200, 1, 3, 2, 5, 30, 40, 8, 7, 6]
result = s.longestConsecutive(nums)
print(result)

"""

"""
