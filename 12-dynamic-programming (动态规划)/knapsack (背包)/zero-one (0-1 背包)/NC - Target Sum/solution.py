from functools import lru_cache
from typing import List


class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        S = sum(nums)
        # 设正号集合和为 P，负号集合和为 N：P - N = target, P + N = S  => P = (S + target) / 2
        if abs(target) > S or (S + target) % 2:
            return 0
        goal = (S + target) // 2
        n = len(nums)

        @lru_cache(maxsize=None)
        def dp(i: int, remain: int) -> int:
            if remain < 0:
                return 0
            if i == n:
                return 1 if remain == 0 else 0
            return dp(i + 1, remain - nums[i]) + dp(i + 1, remain)  # 选 / 不选

        return dp(0, goal)


class Solution_2:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        S = sum(nums)
        if abs(target) > S or (S + target) % 2:
            return 0
        goal = (S + target) // 2
        n = len(nums)
        dp = [[0] * (goal + 1) for _ in range(n + 1)]  # 第1步：key (i, remain) → 二维数组
        dp[n][0] = 1  # 第2步：base case "i==n 且 remain==0 → 1"
        #（其余 base 都是 0，开数组时已就位）
        for i in range(n - 1, -1, -1):  # 第4步：dp[i] 读 dp[i+1] → i 从大到小
            for remain in range(goal + 1):  # remain 维度没被同行读取 → 方向随意！
                skip = dp[i + 1][remain]  # 第3步：dp(i+1, remain) → dp[i+1][remain]
                # "remain<0 返回 0" 翻译成这个 if-else
                take = dp[i + 1][remain - nums[i]] if remain >= nums[i] else 0
                dp[i][remain] = skip + take  # 第3步：return 表达式 → 写入
        return dp[0][goal]  # 顶层调用 dp(0, goal) → 那个格子


s = Solution()
nums = [2, 2, 2]
target = 2
# nums = [1, 0]
# target = 1
result = s.findTargetSumWays(nums, target)
print(result)
