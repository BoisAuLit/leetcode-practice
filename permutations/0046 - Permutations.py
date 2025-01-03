from typing import List


class Solution:
    cache = {}

    def dfs(self, nums: List[int]) -> List[List[int]]:
        if len(nums) == 1:
            return [nums]

        nums_hash = tuple(nums)
        if nums_hash in self.cache:
            return self.cache[nums_hash]

        result = []
        for i in range(len(nums)):
            new_array = [
                number for index, number in enumerate(nums) if index != i
            ]
            result.extend(
                [nums[i]] + x for x in self.dfs(new_array)
            )

        self.cache[nums_hash] = result
        return result

    def permute(self, nums: List[int]) -> List[List[int]]:
        return self.dfs(nums)


s = Solution()
input_ = [1, 2, 3, 4, 5, 6]
result = s.permute(input_)
print(result)
