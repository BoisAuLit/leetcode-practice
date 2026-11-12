"""LC-0122 - Best Time to Buy and Sell Stock II

Level 1 · 07 股票与状态机 DP —— **无限次交易**（状态机的最简形态）
题目在问：可以买卖任意多次（但同一时刻最多持有一股），求最大利润。

### 股票系列的统一状态机（整个 Level 1 共用，背这一个就够）

```
hold  = 今天结束时「持有一股」的最大利润
free  = 今天结束时「不持有」的最大利润

hold = max(hold, free - price)      # 继续持有 / 今天买入
free = max(free, hold + price)      # 继续空仓 / 今天卖出
初始：hold = -inf（或 -prices[0]），free = 0
答案：free
```

**五道题的区别只在这个状态机上加什么限制**：

| 题 | 限制 | 状态 |
|---|---|---|
| **LC-0121** | 只能交易**一次** | `free` 不能从 `hold` 转回来（买入时必须 `-price` 而不是 `free - price`） |
| **LC-0122** 本题 | **无限次** | 上面的裸状态机 |
| **LC-0309** | 卖出后**冷却 1 天** | 买入要用 `free_prev_prev - price` |
| **LC-0714** | 每笔交易**收手续费** | 卖出时 `hold + price - fee` |
| **LC-0123 / 0188** | 最多 k 次交易 | 状态变成 `hold[k]` / `free[k]`，多一维 |

**看清这件事之后，股票系列就是一道题，不是五道。**

### 本题的额外洞察：贪心也对
无限次交易时，答案等于**所有相邻上涨差之和**：
```python
sum(max(0, prices[i] - prices[i-1]) for i in range(1, n))
```
**为什么**：任何一段上涨 `a → b`（中间可能有波动）都可以拆成逐日的小段，
拆开买卖的总利润 **不小于** 一次性买卖（`(p2-p1) + (p3-p2) = p3-p1`）。
而下跌的日子一律不参与（贡献 0）。

所以贪心和 DP 等价 —— 但**只有「无限次交易」时才等价**。
加上任何限制（次数、冷却、手续费）后贪心就不成立了，必须回到状态机。
**这一点是本题最值得记的：不要把贪心当成股票系列的通用解法。**

复杂度：O(n) 时间，O(1) 空间（两种解法都是）。

边界：
  - 单调下降 → 0
  - 单调上升 → `prices[-1] - prices[0]`
  - 单个价格 → 0
  - 全部相同 → 0
"""

from typing import List


##################################################################################################
##### ! Solution 1: 状态机 DP（hold / free 两个状态滚动）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：整个股票系列的统一骨架；加限制时只改转移，不换思路
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def maxProfit(self, prices: List[int]) -> int:
        if not prices:
            return 0
        hold, free = -prices[0], 0
        for p in prices[1:]:
            # ! 注意两行要用「上一轮的值」，所以先算完再赋值（这里用同时赋值）
            hold, free = max(hold, free - p), max(free, hold + p)
        return free


##################################################################################################
##### ! Solution 2: 贪心 —— 所有相邻上涨差之和
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：**只有无限次交易时才成立**；加任何限制（次数/冷却/手续费）后就失效
##################################################################################################


class Solution_2:
    def maxProfit(self, prices: List[int]) -> int:
        return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, len(prices)))


##################################################################################################
##### ! Solution 3: 暴力枚举所有买卖方案（基准答案，用来对拍；只适合很短的输入）
##### ! 时间复杂度: 指数级   空间复杂度: O(n)
##### ! 适用：正确性参照 —— 直接按题面「任意多次买卖」穷举
##################################################################################################


class Solution_3:
    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dfs(i: int, holding: bool) -> int:
            if i == n:
                return 0
            best = dfs(i + 1, holding)                       # ! 什么都不做
            if holding:
                best = max(best, prices[i] + dfs(i + 1, False))   # ! 卖
            else:
                best = max(best, -prices[i] + dfs(i + 1, True))   # ! 买
            return best

        res = dfs(0, False)
        dfs.cache_clear()
        return res


if __name__ == "__main__":
    import random

    cases = [([7, 1, 5, 3, 6, 4], 7), ([1, 2, 3, 4, 5], 4), ([7, 6, 4, 3, 1], 0),
             ([5], 0), ([3, 3, 3], 0)]
    for prices, want in cases:
        a = Solution_1().maxProfit(prices)
        b = Solution_2().maxProfit(prices)
        c = Solution_3().maxProfit(prices)
        assert a == b == c == want, (prices, a, b, c, want)
        print(f"{prices} -> {a}")

    for _ in range(1000):
        prices = [random.randint(0, 9) for _ in range(random.randint(1, 12))]
        a = Solution_1().maxProfit(prices)
        b = Solution_2().maxProfit(prices)
        c = Solution_3().maxProfit(prices)
        assert a == b == c, (prices, a, b, c)
    print("随机对拍 1000 组通过 ✓（状态机 == 贪心 == 穷举；贪心只在无限次交易时成立）")
