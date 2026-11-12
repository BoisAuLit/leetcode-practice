"""LC-0123 - Best Time to Buy and Sell Stock III

Level 1 · 07 股票与状态机 DP —— **最多 2 次交易**（k 的特例，承接 LC-0188）
题目在问：最多完成 **2 笔**交易（必须先卖再买），求最大利润。

### 从无限次到有限次：状态多一维

LC-0122（无限次）只有两个状态 `hold / free`。
**一旦限制交易次数，状态必须记录「已经用掉几次」**：

```
buy1  = 第 1 次买入后的最大利润
sell1 = 第 1 次卖出后的最大利润
buy2  = 第 2 次买入后的最大利润
sell2 = 第 2 次卖出后的最大利润

buy1  = max(buy1,  -p)            # 第 1 次买：从 0 开始
sell1 = max(sell1, buy1 + p)      # 第 1 次卖
buy2  = max(buy2,  sell1 - p)     # 第 2 次买：用第 1 次卖完的钱
sell2 = max(sell2, buy2 + p)      # 第 2 次卖
答案 = sell2
```

**为什么四行可以在同一个循环里顺序更新**（这是本题最容易被质疑的地方）：
  严格按 DP 应该用「上一轮的值」。但这里**用本轮刚更新的值也不会出错**，
  因为那相当于「同一天先买再卖」，利润是 `-p + p = 0`，
  不会让答案变大（不会凭空多出利润），也不会漏掉任何真正更优的方案。
  面试被追问时就这么解释；想稳妥也可以显式保存上一轮的四个值。

### 和 LC-0188（最多 k 次）的关系
LC-0188 就是把这四个变量变成两个长度 k+1 的数组：
```python
for p in prices:
    for t in range(1, k + 1):
        buy[t]  = max(buy[t],  sell[t-1] - p)
        sell[t] = max(sell[t], buy[t] + p)
```
**所以 LC-0123 = LC-0188 的 k=2**。写熟 188 就不用单独记 123；
但 123 用四个变量写出来更直观，适合先理解「为什么要多一维」。

**LC-0188 的一个重要优化**：当 `k >= n // 2` 时，
限制实际上不起作用（最多也只能做 n//2 笔交易），**直接退化成 LC-0122 的贪心**。
不做这个判断，k 很大时会开一个巨大的数组而 MLE / TLE。

### 另一种解法：左右分割（Solution_2）
枚举「分界点 i」，答案 = `max(左边做一次的最大利润 + 右边做一次的最大利润)`。
用两个前缀/后缀数组预处理。O(n) 时间 O(n) 空间。
思路更直白，**但只适用于 k=2**（k 一般时没法这么拆）。

复杂度：Solution_1 O(n) 时间 **O(1)** 空间；Solution_2 O(n) / O(n)。

边界：
  - 单调下降 → 0
  - 只值得做一次交易 → 答案就是那一次
  - `[1,2,3,4,5]` → 4（一次就够，第二次没必要）
  - 长度 < 2 → 0
"""

from typing import List


##################################################################################################
##### ! Solution 1: 四个状态变量（buy1 / sell1 / buy2 / sell2），O(1) 空间
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：最多 2 次交易；是 LC-0188 的 k=2 特例，但写成四个变量最直观
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def maxProfit(self, prices: List[int]) -> int:
        buy1 = buy2 = float("-inf")
        sell1 = sell2 = 0
        for p in prices:
            buy1 = max(buy1, -p)              # ! 第 1 次买入
            sell1 = max(sell1, buy1 + p)      # ! 第 1 次卖出
            buy2 = max(buy2, sell1 - p)       # ! 第 2 次买入（用第 1 次的收益）
            sell2 = max(sell2, buy2 + p)      # ! 第 2 次卖出
        return int(sell2)


##################################################################################################
##### ! Solution 2: 左右分割 —— 前缀「一次交易最大利润」+ 后缀「一次交易最大利润」
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：思路最直白，但**只适用于 k=2**；k 一般时无法这么拆
##################################################################################################


class Solution_2:
    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)
        if n < 2:
            return 0
        left = [0] * n                        # ! left[i] = 在 [0, i] 内做一次交易的最大利润
        lo = prices[0]
        for i in range(1, n):
            lo = min(lo, prices[i])
            left[i] = max(left[i - 1], prices[i] - lo)
        right = [0] * (n + 1)                 # ! right[i] = 在 [i, n-1] 内做一次交易的最大利润
        hi = prices[-1]
        for i in range(n - 2, -1, -1):
            hi = max(hi, prices[i])
            right[i] = max(right[i + 1], hi - prices[i])
        # ! 枚举分界：前 i 天做第一笔，第 i 天之后做第二笔
        return max(left[i] + right[i + 1] for i in range(n))


##################################################################################################
##### ! Solution 3: 通用 k 次交易 DP，取 k=2（也就是 LC-0188 的实现）
##### ! 时间复杂度: O(n·k)   空间复杂度: O(k)
##### ! 适用：说明 123 就是 188 的 k=2；含「k 很大时退化成贪心」的优化
##################################################################################################


class Solution_3:
    def maxProfit(self, prices: List[int], k: int = 2) -> int:
        n = len(prices)
        if n < 2 or k == 0:
            return 0
        if k >= n // 2:                       # ! 限制失效 ⟹ 退化成无限次交易的贪心
            return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, n))
        buy = [float("-inf")] * (k + 1)
        sell = [0] * (k + 1)
        for p in prices:
            for t in range(1, k + 1):
                buy[t] = max(buy[t], sell[t - 1] - p)
                sell[t] = max(sell[t], buy[t] + p)
        return int(sell[k])


if __name__ == "__main__":
    import random

    cases = [([3, 3, 5, 0, 0, 3, 1, 4], 6), ([1, 2, 3, 4, 5], 4), ([7, 6, 4, 3, 1], 0),
             ([1], 0), ([], 0), ([1, 2, 4, 2, 5, 7, 2, 4, 9, 0], 13)]
    for prices, want in cases:
        a = Solution_1().maxProfit(prices)
        b = Solution_2().maxProfit(prices)
        c = Solution_3().maxProfit(prices, 2)
        assert a == b == c == want, (prices, a, b, c, want)
        print(f"{prices} -> {a}")

    # ! 暴力基准：最多 2 次交易的穷举
    def brute(prices):
        from functools import lru_cache
        n = len(prices)

        @lru_cache(maxsize=None)
        def dfs(i, holding, used):
            if i == n or used > 2:
                return 0
            best = dfs(i + 1, holding, used)
            if holding:
                best = max(best, prices[i] + dfs(i + 1, False, used + 1))   # ! 卖出算一次交易
            elif used < 2:
                best = max(best, -prices[i] + dfs(i + 1, True, used))
            return best

        r = dfs(0, False, 0)
        dfs.cache_clear()
        return r

    for _ in range(600):
        prices = [random.randint(0, 9) for _ in range(random.randint(0, 11))]
        w = brute(tuple(prices))
        a = Solution_1().maxProfit(prices)
        b = Solution_2().maxProfit(prices)
        c = Solution_3().maxProfit(prices, 2)
        assert a == b == c == w, (prices, a, b, c, w)
    print("随机对拍 600 组通过 ✓（四变量 == 左右分割 == 通用 k 次 == 穷举）")
