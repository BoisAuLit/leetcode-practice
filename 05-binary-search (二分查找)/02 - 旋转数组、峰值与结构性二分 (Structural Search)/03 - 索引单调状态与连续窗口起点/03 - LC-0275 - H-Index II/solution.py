"""LC-0275 - H-Index II（第二轮自主新增）

Level 1 · 02 结构性二分 —— 在「下标与值的关系」上定义单调谓词
题目在问：citations 已**升序排列**，求 h-index：
         有 h 篇论文各自至少被引用 h 次（其余不超过 h 次）。

为什么新增它：
  本章前面的题（153/33/162/540）都在找**数组自身结构**上的特殊点。
  这道题的谓词建立在「**下标和值的关系**」上，而不是值本身 —— 和 LC-1539 是同一家族
  （1539 用 `missing(i) = arr[i] - (i+1)`，本题用 `n - i <= citations[i]`），
  但 1539 求的是「第一个达到 k」，本题求的是「第一个成立的位置换算出的答案」。
  两题并排，能把「自己构造一个单调函数再二分」这件事讲透。它是 LeetCode Top Interview 150 题。

决定性观察：
  1. 数组升序 ⟹ 从下标 i 开始，右边有 `n - i` 篇论文，它们的引用数**都 >= citations[i]**。
  2. 定义谓词 `P(i) = (citations[i] >= n - i)`：
     「从 i 往右这 n-i 篇，每篇都至少被引 n-i 次」。
  3. **P 是单调的**：i 增大时，`n - i` 减小而 `citations[i]` 不减，
     所以 P 一旦为真就一直为真 —— 形如 `F F F T T T`。
  4. 要最大化 h = n - i，就要找**最小的**满足 P 的 i ⟹ 标准 First True（Lower Bound）。
     答案 = `n - lo`；若没有任何 i 满足，`lo == n`，答案 0，公式照样成立。

单调性证明（这一步必须自己确认，不能默认）：
      设 P(i) 成立，即 `citations[i] >= n - i`。
      对 i+1：`citations[i+1] >= citations[i] >= n - i > n - (i+1)`，
      所以 P(i+1) 也成立。∎

复杂度：O(log n) 时间，O(1) 空间。
      （LC-0274 H-Index I 数组无序，需要排序或计数排序，是另一道题。）

边界：
  - [0,1,3,5,6] → 3
  - [0,0,0] → 0（谁都不满足，lo 走到 n）
  - [100] → 1（1 篇被引 100 次，h=1，不是 100）
  - [1,1,1] → 1
  - [] → 0
"""

from typing import List


##################################################################################################
##### ! Solution 1: 在「citations[i] >= n - i」这个单调谓词上做 First True 二分
##### ! 时间复杂度: O(log n)   空间复杂度: O(1)
##### ! 适用：自己构造下标相关的单调谓词再二分；和 LC-1539 同一家族
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def hIndex(self, citations: List[int]) -> int:
        n = len(citations)
        lo, hi = 0, n                      # ! 左闭右开，hi = n 表示「一个都不满足」
        while lo < hi:
            mid = (lo + hi) // 2
            if citations[mid] >= n - mid:  # ! P(mid) 成立 → 答案在左边（含 mid）
                hi = mid
            else:
                lo = mid + 1
        return n - lo                      # ! 没有满足的时候 lo == n，结果 0，公式自洽


##################################################################################################
##### ! Solution 2: 从右往左线性扫描（基准答案，也是面试里可以先说的 O(n) 版）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：正确性参照；没有「已排序」条件时也是 LC-0274 的做法基础
##################################################################################################


class Solution_2:
    def hIndex(self, citations: List[int]) -> int:
        n = len(citations)
        h = 0
        for i in range(n - 1, -1, -1):
            if citations[i] >= n - i:      # ! 往左走，n-i 越来越大，一旦不满足就停
                h = n - i
            else:
                break
        return h


##################################################################################################
##### ! Solution 3: 直接按定义枚举 h（基准答案，用来对拍）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(1)
##### ! 适用：正确性参照 —— 直接翻译题面定义，最不容易理解错
##################################################################################################


class Solution_3:
    def hIndex(self, citations: List[int]) -> int:
        n = len(citations)
        best = 0
        for h in range(n + 1):
            if sum(1 for c in citations if c >= h) >= h:   # ! 至少 h 篇被引 >= h 次
                best = h
        return best


if __name__ == "__main__":
    import random

    cases = [[0, 1, 3, 5, 6], [0, 0, 0], [100], [1, 1, 1], [], [1, 2, 100]]
    for c in cases:
        a = Solution_1().hIndex(c)
        assert a == Solution_2().hIndex(c) == Solution_3().hIndex(c), (c, a)
        print(f"{c} -> {a}")

    for _ in range(1000):                # ! 随机升序数组对拍
        c = sorted(random.randint(0, 8) for _ in range(random.randint(0, 9)))
        assert Solution_1().hIndex(c) == Solution_2().hIndex(c) == Solution_3().hIndex(c), c
    print("随机对拍 1000 组通过 ✓")
