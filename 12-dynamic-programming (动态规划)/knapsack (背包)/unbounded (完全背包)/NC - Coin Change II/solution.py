from typing import List
from functools import lru_cache


class Solution_1:
    def change(self, amount: int, coins: List[int]) -> int:
        @lru_cache(maxsize=None)
        def dp(i: int, remain: int) -> int:
            if remain == 0:
                return 1
            if remain < 0 or i == len(coins):
                return 0
            return dp(i + 1, remain) + dp(i, remain - coins[i])

        return dp(0, amount)

"""
Preferred solution
"""
class Solution_2:
    def change(self, amount: int, coins: List[int]) -> int:
        n = len(coins)
        dp = [[0] * (amount + 1) for _ in range(n + 1)]  # 第1步
        for i in range(n + 1):                            # 第2步：remain==0 → 1（不分 i）
            dp[i][0] = 1

        for i in range(n - 1, -1, -1):                    # 第4步：读 i+1 行 → i 从大到小
            for remain in range(1, amount + 1):           # 第4步：同行读更小 remain → 从小到大
                skip = dp[i + 1][remain]                  # 第3步：dp(i+1, remain)
                take = dp[i][remain - coins[i]] if remain >= coins[i] else 0
                #      ↑ 同一行！i 不动 = 无限枚          # "remain<0 → 0" 化为这个 if-else
                dp[i][remain] = skip + take               # 第3步：return → 写入

        return dp[0][amount]        

s = Solution_2()
amount = 4
coins = [1, 2, 3]
result = s.change(amount, coins)
print(result)
