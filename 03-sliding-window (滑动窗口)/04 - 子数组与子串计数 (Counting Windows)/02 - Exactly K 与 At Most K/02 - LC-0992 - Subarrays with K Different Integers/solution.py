"""LC-0992 - Subarrays with K Different Integers

Level 1 · 04 计数窗口 / 02 Exactly K 与 At Most K（P1 进阶）
题目在问：**恰好**含 K 种不同整数的子数组有多少个

和 LC-0930 是同一招，只换了 atMost 的含义：
      **exactly(K) = atMost(K) - atMost(K-1)**，
      这里的 `atMost(k)` = 「不同整数种数 <= k 的子数组个数」，
      而它的实现就是 LC-0904（最多 K 种）的窗口，把「取最大长度」换成「累加 right-left+1」。

为什么必须绕这一圈：「恰好 K 种」不单调 —— 窗口右扩可能从 K 种变成 K+1 种，
      左缩又可能掉到 K-1 种，没有一个「一直合法」的窗口可以边扫边数。
      而「至多 k 种」是单调的（右扩只增不减、左缩只减不增），所以能用标准窗口。

另一种等价思路（不用相减）：对每个 right，同时维护两个左边界
      `left_k`（最多 K 种的最小左端）和 `left_k1`（最多 K-1 种的最小左端），
      贡献就是 `left_k1 - left_k`。本质还是两个 atMost。

坑：
  - `atMost(0)` 要返回 0（K = 1 时会用到）
  - 频率归零必须 `del`，否则 `len(freq)` 失真
  - 答案可能很大，Python 无所谓，别的语言注意溢出
"""

from collections import defaultdict
from typing import List


##################################################################################################
##### ! Solution 1: atMost(K) - atMost(K-1)
##### ! 时间复杂度: O(n)（跑两遍窗口）  空间复杂度: O(K)
##### ! 适用：「恰好 K 种」的标准解；和 LC-0930 共用同一个恒等式，只换 atMost 的定义
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def subarraysWithKDistinct(self, nums: List[int], k: int) -> int:
        def at_most(m: int) -> int:
            if m <= 0:
                return 0
            freq = defaultdict(int)
            left = 0
            res = 0
            for right, x in enumerate(nums):
                freq[x] += 1
                while len(freq) > m:
                    out = nums[left]
                    freq[out] -= 1
                    if freq[out] == 0:
                        del freq[out]
                    left += 1
                res += right - left + 1
            return res
        return at_most(k) - at_most(k - 1)


##################################################################################################
##### ! Solution 2: 一次扫描，同时维护两个左边界
##### ! 时间复杂度: O(n)   空间复杂度: O(K)
##### ! 适用：只扫一遍；贡献 = left_{K-1} - left_K，看得出「相减」在几何上是什么意思
##################################################################################################


class Solution_2:
    def subarraysWithKDistinct(self, nums: List[int], k: int) -> int:
        f1 = defaultdict(int)   # 对应「最多 k 种」
        f2 = defaultdict(int)   # 对应「最多 k-1 种」
        l1 = l2 = 0
        ans = 0
        for x in nums:
            f1[x] += 1
            f2[x] += 1
            while len(f1) > k:
                f1[nums[l1]] -= 1
                if f1[nums[l1]] == 0:
                    del f1[nums[l1]]
                l1 += 1
            while len(f2) > k - 1:
                f2[nums[l2]] -= 1
                if f2[nums[l2]] == 0:
                    del f2[nums[l2]]
                l2 += 1
            ans += l2 - l1       # ! 起点落在 [l1, l2) 的窗口恰好有 k 种
        return ans


if __name__ == "__main__":
    import random
    cases = [([1, 2, 1, 2, 3], 2, 7), ([1, 2, 1, 3, 4], 3, 3), ([1], 1, 1),
             ([1, 1, 1], 1, 6), ([1, 2], 2, 1)]
    sols = [Solution_1(), Solution_2()]
    for sol in sols:
        for nums, k, want in cases:
            got = sol.subarraysWithKDistinct(nums[:], k)
            assert got == want, f"{type(sol).__name__} {nums} k={k}: got {got}, want {want}"
    rng = random.Random(992)
    for _ in range(3000):
        nums = [rng.randint(1, 4) for _ in range(rng.randint(1, 10))]
        k = rng.randint(1, 4)
        want = sum(1 for i in range(len(nums)) for j in range(i, len(nums))
                   if len(set(nums[i:j + 1])) == k)
        for sol in sols:
            assert sol.subarraysWithKDistinct(nums[:], k) == want, (type(sol).__name__, nums, k, want)
    print("2 个解法全过（含 3000 组随机对拍）")
