"""LC-0410 - Split Array Largest Sum

Level 1 · 03 二分答案与可行性判断 —— **Minimize the Maximum**（最小化最大值）的原型题
题目在问：把非负整数数组切成 k 个**连续**子数组，使「各段和的最大值」尽量小，求这个最小值。

「最小化最大值」是二分答案最经典的信号词。看到它先想：
  能不能把「最小化 X」变成「给定 X，判断可行吗」？本题可以：

二分答案三件套：
  1. **答案空间**：`lo = max(nums)`（任何一段至少要装下最大的那个元素），
                  `hi = sum(nums)`（整个数组当一段）。
  2. **feasible(limit)**：贪心从左往右累加，超过 limit 就开新的一段，
     算出需要几段，判断 `<= k`。
  3. **单调性**：limit 越大，需要的段数越少 ⟹ `F F F T T T` ⟹ First True。

为什么顺序贪心分段是最优的（这一步必须讲）：
      要判断的是「能否用 <= k 段」，所以段数越少越好。
      「能塞进当前段就不开新段」是最优的：提前开新段只会让当前段留空、总段数不减。
      形式化地说，贪心产生的段数是所有合法分法中的最小值。
      **前提是元素非负** —— 若有负数，加一个元素可能让段和变小，
      「超过 limit 就断开」这个判断立刻失效。题目的非负约束是这个贪心的基础。

为什么下界必须是 `max(nums)`：
      若 `limit < max(nums)`，那个最大元素单独一段都放不下，feasible 恒 False。

为什么最小可行的 limit 就是答案：
      feasible(limit) 为真表示「存在一种分法，每段和都 <= limit」。
      最小的这种 limit，恰好等于「最优分法下的最大段和」—— 
      因为最优解 OPT 满足 feasible(OPT)，而任何 `< OPT` 的值都不可行。

复杂度：**O(n · log(sum - max))**，空间 O(1)。
      DP 解法是 O(k·n²)，在 n=1000、k=50 时明显更慢，但在面试里值得提一句。

和 LC-1011 的关系：**本质是同一道题**。
      1011 的「天数」就是这里的「段数」，「容量」就是这里的「limit」。
      唯一区别是叙事外壳。

边界：
  - nums=[7,2,5,10,8], k=2 → 18
  - nums=[1,2,3,4,5], k=2 → 9
  - k == n → 答案 max(nums)
  - k == 1 → 答案 sum(nums)
  - 含 0 元素
"""

from typing import List


##################################################################################################
##### ! Solution 1: 二分答案 + 贪心分段（First True）
##### ! 时间复杂度: O(n · log(sum - max))   空间复杂度: O(1)
##### ! 适用：一切「最小化最大段和 / 最大负载」的题；LC-1011、LC-1760 同模板
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def splitArray(self, nums: List[int], k: int) -> int:
        def segments(limit: int) -> int:
            cnt, cur = 1, 0
            for x in nums:
                if cur + x > limit:      # ! 装不下了就开新段（元素非负才能这样判断）
                    cnt += 1
                    cur = 0
                cur += x
            return cnt

        lo, hi = max(nums), sum(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if segments(mid) <= k:       # ! 段数够少 → 还能把 limit 压更小
                hi = mid
            else:
                lo = mid + 1
        return lo


##################################################################################################
##### ! Solution 2: 区间 DP —— dp[i][j] = 前 i 个元素分成 j 段的最小最大段和
##### ! 时间复杂度: O(k · n^2)   空间复杂度: O(k · n)
##### ! 适用：不依赖「非负」前提的通用解；n 较小时可用，也是面试 follow-up 的好素材
##################################################################################################


class Solution_2:
    def splitArray(self, nums: List[int], k: int) -> int:
        n = len(nums)
        prefix = [0] * (n + 1)
        for i, x in enumerate(nums):
            prefix[i + 1] = prefix[i] + x
        INF = float("inf")
        dp = [[INF] * (k + 1) for _ in range(n + 1)]
        dp[0][0] = 0
        for i in range(1, n + 1):
            for j in range(1, min(i, k) + 1):
                for t in range(j - 1, i):            # ! 最后一段是 nums[t..i-1]
                    last = prefix[i] - prefix[t]
                    if dp[t][j - 1] == INF:
                        continue
                    dp[i][j] = min(dp[i][j], max(dp[t][j - 1], last))
        return int(dp[n][k])


##################################################################################################
##### ! Solution 3: 枚举所有可能的 limit（基准答案，用来对拍）
##### ! 时间复杂度: O(n · (sum - max))   空间复杂度: O(1)
##### ! 适用：正确性参照，同时验证 feasible 的单调性
##################################################################################################


class Solution_3:
    def splitArray(self, nums: List[int], k: int) -> int:
        def segments(limit: int) -> int:
            cnt, cur = 1, 0
            for x in nums:
                if cur + x > limit:
                    cnt += 1
                    cur = 0
                cur += x
            return cnt

        for limit in range(max(nums), sum(nums) + 1):
            if segments(limit) <= k:
                return limit
        return sum(nums)


if __name__ == "__main__":
    import random

    cases = [([7, 2, 5, 10, 8], 2), ([1, 2, 3, 4, 5], 2), ([1, 4, 4], 3),
             ([0, 0, 0], 2), ([10], 1), ([2, 3, 1, 2, 4, 3], 3)]
    for nums, k in cases:
        a = Solution_1().splitArray(nums, k)
        assert a == Solution_2().splitArray(nums, k), (nums, k, a, Solution_2().splitArray(nums, k))
        assert a == Solution_3().splitArray(nums, k), (nums, k)
        print(f"nums={nums}, k={k} -> {a}")

    for _ in range(400):                 # ! 随机对拍：二分 == DP == 枚举
        n = random.randint(1, 7)
        nums = [random.randint(0, 9) for _ in range(n)]
        k = random.randint(1, n)
        a, b, c = (Solution_1().splitArray(nums, k), Solution_2().splitArray(nums, k),
                   Solution_3().splitArray(nums, k))
        assert a == b == c, (nums, k, a, b, c)
    print("随机对拍 400 组通过 ✓（二分 == 区间 DP == 枚举）")
