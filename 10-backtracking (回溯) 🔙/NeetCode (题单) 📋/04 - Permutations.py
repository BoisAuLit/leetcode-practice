from typing import List


class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        res = []

        def backtrack(curr, unique):
            if len(curr) == len(nums):
                res.append(curr.copy())
                return
            for j in range(len(nums)):
                if nums[j] in unique:
                    continue
                curr.append(nums[j])
                unique.add(nums[j])
                backtrack(curr, unique)
                curr.pop()
                unique.remove(nums[j])

        backtrack([], set())
        return res


s = Solution()
nums = [1, 2, 3]
result = s.permute(nums)
print(result)
