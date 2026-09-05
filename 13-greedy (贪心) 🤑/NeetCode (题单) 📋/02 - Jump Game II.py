from typing import List
from functools import lru_cache


class Solution_1:
    def jump(self, nums: List[int]) -> int:
        # 已经跳了几次
        jumps = 0 
        # 当前 jumps 能够覆盖到的最右边界
        currentEnd = 0
        # 当前这一层所有位置，下一跳最远可以到哪里。
        # 换言之: 如果再跳一次, 目前发现最远能够到哪里
        farthest = 0 

        """
        对于当前这一跳能够到达的所有位置，
        把它们全部检查一遍，
        然后记住下一跳最远能够扩展到哪里。
        """
        for i in range(len(nums) - 1):

            farthest = max(farthest, i + nums[i])

            if i == currentEnd:
                jumps += 1
                currentEnd = farthest

        return jumps


class Solution_2:
    def jump(self, nums: List[int]) -> int:
        n = len(nums)

        @lru_cache
        def dfs(i):
            if i >= n - 1:
                return 0
            if nums[i] == 0:
                return float("inf")
            return 1 + min(dfs(i + j) for j in range(1, nums[i] + 1) if i + j <= n - 1)

        return dfs(0)


class Solution_3:
    def jump(self, nums: List[int]) -> int:
        n = len(nums)
        dp = [float("inf")] * n
        dp[-1] = 0
        for i in range(n - 2, -1, -1):
            if nums[i] == 0:
                continue
            dp[i] = 1 + min(dp[i + j] for j in range(1, nums[i] + 1) if i + j <= n - 1)
        return dp[0]


s = Solution_3()
input_ = [2, 4, 1, 1, 1, 1]
input_ = [2, 3, 0, 1, 4]
result = s.jump(input_)
print(result)
