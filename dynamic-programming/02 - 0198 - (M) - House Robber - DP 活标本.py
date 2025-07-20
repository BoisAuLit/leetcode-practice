from typing import List

class Solution_Top_Down_Recursion:
    def rob(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return sum(nums)

        def dp(i: int) -> int:
            if i == 0:
                return nums[0]
            if i == 1:
                return max(nums[0], nums[1])
            if i not in memo:
                memo[i] = max(nums[i] + dp(i - 2), dp(i - 1))
            return memo[i]

        memo = {}
        return dp(len(nums) - 1)



class Solution_Bottom_Up_Iteration:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return nums[0]
        """
        这里dp的意思是:
        dp[0]: 如果只抢劫位于index=0 位置的这一家, 最多能抢多少钱
        dp[1]: 若谷之前借 index<= 1 位置的这些家, 最多能抢多少钱
        """
        dp = [0] * n
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])
        for i in range(2, n):
            dp[i] = max(nums[i] + dp[i - 2], dp[i - 1])
        return dp[n - 1]


s = Solution_Top_Down_Recursion()
nums = [1, 2, 3, 1]
result = s.rob(nums)
print(result)
