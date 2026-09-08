"""
📌 信号→模式: 有重复值的子集 → 排序 + 同层跳过相同值
📅 首次: 2026-09-04 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 未排期
"""
from typing import List


class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        res = []

        def backtrack(i, curr):
            res.append(curr.copy())
            for j in range(i, len(nums)):
                if j > i and nums[j] == nums[j - 1]:
                    continue
                curr.append(nums[j])
                backtrack(j + 1, curr)
                curr.pop()

        backtrack(0, [])
        return res


s = Solution()
input_ = [1, 2, 1]
result = s.subsetsWithDup(input_)
print(result)
