"""LC-1423 - Maximum Points You Can Obtain from Cards

Level 1 · 01 定长窗口 —— Complementary Window（补集窗口）
题目在问：每次只能从数组最左或最右拿一张牌，恰好拿 k 张，总分最大是多少

决定性观察（整道题就靠这一句）：
      **从两端拿走 k 张 ⟺ 留下中间一段长度为 n-k 的连续区间。**
      于是「最大化拿走的分数」= `总和 - 中间那段的最小和`，
      而「长度固定为 n-k 的最小子数组和」就是最标准的定长窗口。

这个转化叫 complement（补集）转化，是滑动窗口最常见的问题变形之一。
同类：**LC-1658**（两端拿走若干个使和为 x ⟺ 中间保留一段和为 total-x 的**最长**区间）。
      两题的区别：1423 固定的是**长度**，1658 固定的是**和**，
      所以一个用定长窗口、一个用变长窗口。

Loop Invariant：扫到 i 时 `cur` = 中间窗口 `cards[i-(n-k)+1 .. i]` 的和。

坑：
  - `k == n` 时中间窗口长度为 0，答案是全部和 —— 要单独处理或让循环自然跳过
  - 另一种写法是「前缀 i 张 + 后缀 k-i 张」枚举 i，也是 O(k)，但补集窗口更能体现思想
  - 不要真的去模拟「每次选左还是选右」，那是 2^k 的搜索
"""

from typing import List


##################################################################################################
##### ! Solution 1: 补集转化 —— 求长度 n-k 的最小窗口和
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：所有「从两端取」的题；把「取走什么」翻译成「留下什么」是关键一步
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def maxScore(self, cardPoints: List[int], k: int) -> int:
        n = len(cardPoints)
        total = sum(cardPoints)
        m = n - k                       # ! 留在中间的那段的长度
        if m == 0:
            return total                # ! 全部拿走
        cur = sum(cardPoints[:m])
        worst = cur                     # 中间段的最小和
        for i in range(m, n):
            cur += cardPoints[i] - cardPoints[i - m]
            worst = min(worst, cur)
        return total - worst


##################################################################################################
##### ! Solution 2: 枚举「左边拿 i 张、右边拿 k-i 张」
##### ! 时间复杂度: O(k)   空间复杂度: O(1)
##### ! 适用：更直观的写法，复杂度更好（O(k) 而不是 O(n)）；但看不出「补集窗口」这层转化
##################################################################################################


class Solution_2:
    def maxScore(self, cardPoints: List[int], k: int) -> int:
        cur = sum(cardPoints[:k])       # 先全从左边拿
        best = cur
        for i in range(1, k + 1):       # ! 退掉左边第 k-i+1 张，改从右边拿第 i 张
            cur += cardPoints[-i] - cardPoints[k - i]
            best = max(best, cur)
        return best


if __name__ == "__main__":
    import random
    cases = [([1, 2, 3, 4, 5, 6, 1], 3, 12), ([2, 2, 2], 2, 4),
             ([9, 7, 7, 9, 7, 7, 9], 7, 55), ([1, 1000, 1], 1, 1), ([100], 1, 100)]
    sols = [Solution_1(), Solution_2()]
    for sol in sols:
        for c, k, want in cases:
            got = sol.maxScore(c[:], k)
            assert got == want, f"{type(sol).__name__} {c} k={k}: got {got}, want {want}"
    rng = random.Random(1423)
    for _ in range(3000):
        n = rng.randint(1, 9); k = rng.randint(1, n)
        c = [rng.randint(1, 20) for _ in range(n)]
        # 暴力：枚举左边拿几张
        want = max(sum(c[:i]) + sum(c[n - (k - i):] if k - i else []) for i in range(k + 1))
        for sol in sols:
            assert sol.maxScore(c[:], k) == want, (type(sol).__name__, c, k, want)
    print("2 个解法全过（含 3000 组随机对拍）")
