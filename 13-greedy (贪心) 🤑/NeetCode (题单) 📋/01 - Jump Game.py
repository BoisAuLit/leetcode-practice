from typing import List
from functools import lru_cache

"""
Preferred solution
"""
class Solution:
    def canJump(self, nums: List[int]) -> bool:
        """
        goal 的含义最靠左的可以最终抵达终点的 index
        只要今后的某一个在 goal 左边的点(设为 j)能够抵达 goal 所代表的 index,
        那么说明 j 也可以最终抵达终点

        所以我们只需要一直维护 goal 就可以了
        """
        goal = len(nums) - 1

        for i in range(len(nums) - 2, -1, -1):
            if i + nums[i] >= goal:
                goal = i

        return goal == 0

class Solution_1_Top_Down_Memoization:
    def canJump(self, nums: List[int]) -> bool:
        n = len(nums)

        @lru_cache
        def dfs(i):
            if i == n - 1:
                return True
            for j in range(1, nums[i] + 1):
                if dfs(i + j):
                    return True
            return False

        return dfs(0)


class Solution_2_Bottom_Up_Iteration:
    def canJump(self, nums: List[int]) -> bool:
        n = len(nums)
        dp = [False] * n
        dp[-1] = True
        for i in range(n - 2, -1, -1):
            dp[i] = any(dp[i + j] 
                        for j in range(1, nums[i] + 1) 
                        if i + j <= n - 1
                    )
        return dp[0]


