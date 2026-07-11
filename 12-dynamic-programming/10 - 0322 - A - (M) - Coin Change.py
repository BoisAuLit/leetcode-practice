from typing import List, Tuple
from functools import cache


class Solution_Top_Down:
    def coinChange(self, coins: List[int], amount: int) -> int:
        if amount == 0:
            return 0
        coins.sort()

        @cache
        def dp(remain: int) -> Tuple[bool, int]:
            min_ = float("inf")
            for coin in coins:
                if coin < remain:
                    can_finish, length = dp(remain - coin)
                    if can_finish:
                        min_ = min(min_, length + 1)
                elif coin == remain:
                    return True, 1
                else:
                    break
            if min_ == float("inf"):
                return False, -1
            else:
                return True, min_

        can_finish, length = dp(amount)
        return length if can_finish else -1


class Solution_Bottom_Up:
    def coinChange(self, coins: List[int], amount: int) -> int:
        if amount == 0:
            return 0
        dp = [float("inf")] * (amount + 1)
        dp[0] = 1
        for i in range(1, amount + 1):
            if i in coins:
                dp[i] = 1
            else:
                dp[i] = 1 + min(
                    list(dp[i - coin] for coin in coins if i - coin >= 1),
                    default=float("inf"),
                )
        return dp[-1] if dp[-1] != float("inf") else -1


# s = Solution()
# coins = [1]
# amount = 0
# result = s.coinChange(coins, amount)
# print(result)


# s = Solution()
# coins = [1, 2, 5]
# amount = 11
# result = s.coinChange(coins, amount)
# print(result)

# s = Solution()
# coins = [2]
# amount = 3
# result = s.coinChange(coins, amount)
# print(result)
