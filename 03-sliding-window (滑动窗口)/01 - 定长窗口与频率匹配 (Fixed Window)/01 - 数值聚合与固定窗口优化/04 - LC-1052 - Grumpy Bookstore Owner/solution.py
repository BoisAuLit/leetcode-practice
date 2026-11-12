"""LC-1052 - Grumpy Bookstore Owner

Level 1 · 01 定长窗口 —— Baseline + Delta（基础值 + 窗口内增量）
题目在问：老板在 grumpy[i] == 1 的分钟会气走当分钟的 customers[i] 个顾客。
      他可以用一次「保持冷静」的技能覆盖**连续 k 分钟**，求最多能让多少顾客满意

决定性观察（本题的教学点）：把答案拆成两部分 ——
      **固定的基础值**（本来就满意的：`grumpy[i] == 0` 的那些）
      **+ 窗口内能额外挽回的增量**（窗口里 `grumpy[i] == 1` 的那些）。
      基础值和技能用在哪无关，所以只需要最大化「长度为 k 的窗口里被气走的人数」。

这一步「拆成不变量 + 可优化量」是定长窗口题里非常通用的套路，
和 LC-0643 的区别在于：窗口维护的不是原数组的和，而是**一个派生数组**
（`customers[i] * grumpy[i]`）的和。想清楚「窗口里到底该累加什么」比写循环重要。

Loop Invariant：`cur` = 窗口内 `customers[i] * grumpy[i]` 之和 = 这段时间用技能能多救的人。

坑：
  - 基础值要在**整个数组**上算，不是只在窗口外算（窗口内 grumpy==0 的人本来就满意，别漏）
  - k 可能大于等于 n，此时整段都能救
  - 别把 `customers[i]` 无条件加进窗口，只有 `grumpy[i] == 1` 的才算增量
"""

from typing import List


##################################################################################################
##### ! Solution 1: 基础值 + 定长窗口求最大增量
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：「有一次 / 有限次改变机会」的定长窗口题；先算不受影响的部分，再窗口里最大化收益
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def maxSatisfied(self, customers: List[int], grumpy: List[int], minutes: int) -> int:
        base = sum(c for c, g in zip(customers, grumpy) if g == 0)   # ! 和技能用在哪无关
        cur = best = 0
        for i, (c, g) in enumerate(zip(customers, grumpy)):
            cur += c * g                     # ! 只有被气走的才是「能挽回的增量」
            if i >= minutes:
                j = i - minutes
                cur -= customers[j] * grumpy[j]
            best = max(best, cur)
        return base + best


##################################################################################################
##### ! Solution 2: 先构造增量数组，再求定长最大子数组和
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：把「派生数组」显式写出来，更容易看清这题就是 LC-0643 换了个数组
##################################################################################################


class Solution_2:
    def maxSatisfied(self, customers: List[int], grumpy: List[int], minutes: int) -> int:
        gain = [c * g for c, g in zip(customers, grumpy)]   # ! 显式的派生数组
        base = sum(customers) - sum(gain)
        k = min(minutes, len(gain))
        cur = sum(gain[:k])
        best = cur
        for i in range(k, len(gain)):
            cur += gain[i] - gain[i - k]
            best = max(best, cur)
        return base + best


if __name__ == "__main__":
    import random
    cases = [([1, 0, 1, 2, 1, 1, 7, 5], [0, 1, 0, 1, 0, 1, 0, 1], 3, 16),
             ([1], [0], 1, 1), ([4, 10, 10], [1, 1, 0], 2, 24), ([2, 6, 6, 9], [0, 0, 1, 1], 1, 17)]
    sols = [Solution_1(), Solution_2()]
    for sol in sols:
        for c, g, k, want in cases:
            got = sol.maxSatisfied(c[:], g[:], k)
            assert got == want, f"{type(sol).__name__} {c} {g} k={k}: got {got}, want {want}"
    rng = random.Random(1052)
    for _ in range(3000):
        n = rng.randint(1, 9); k = rng.randint(1, n)
        c = [rng.randint(0, 9) for _ in range(n)]
        g = [rng.randint(0, 1) for _ in range(n)]
        # 暴力：枚举技能用在哪一段
        want = max(sum(c[i] if (g[i] == 0 or s <= i < s + k) else 0 for i in range(n))
                   for s in range(n - k + 1))
        for sol in sols:
            assert sol.maxSatisfied(c[:], g[:], k) == want, (type(sol).__name__, c, g, k, want)
    print("2 个解法全过（含 3000 组随机对拍）")
