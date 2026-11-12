"""LC-2461 - Maximum Sum of Distinct Subarrays With Length K

Level 1 · 01 定长窗口 —— Fixed Window + Frequency Map（定长窗口 + 频率表）
题目在问：长度恰好为 k、且元素**互不相同**的连续子数组，最大和是多少（没有则返回 0）

决定性观察：窗口长度固定这件事没变，变的是窗口**多带了一个状态** ——
      一张频率表。于是合法性判断变成一句话：**`len(freq) == k`**
      （k 个位置装了 k 个不同的键 ⇔ 没有重复）。

Loop Invariant：`cur` = 当前窗口的和，`freq` = 当前窗口每个值出现几次，
      且 `freq` 里只保留计数 > 0 的键 —— **计数归零必须 del**，否则 `len(freq)` 就不可信了。

和变长窗口的区别：这里**不因为出现重复而收缩**（长度必须是 k），
      只是「这个窗口不合法，跳过」。LC-0003 才是遇到重复就收缩。

坑：
  - `freq[x] == 0` 时一定要 `del freq[x]`，这是本题最常见的错
  - 没有任何合法窗口时返回 0，不是 -1
  - 和可能很大（1e5 × 1e5 = 1e10），C++/Java 要用 long long
"""

from collections import defaultdict
from typing import List


##################################################################################################
##### ! Solution 1: 定长窗口 + 频率表，用 len(freq) == k 判重
##### ! 时间复杂度: O(n)   空间复杂度: O(k)
##### ! 适用：「定长 + 额外约束」的模板；约束换成别的（元音数、奇数个数…）只改状态不改骨架
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def maximumSubarraySum(self, nums: List[int], k: int) -> int:
        freq = defaultdict(int)
        cur = best = 0
        for i, x in enumerate(nums):
            freq[x] += 1
            cur += x
            if i >= k:                      # ! 窗口超长了，吐掉最左边那个
                out = nums[i - k]
                cur -= out
                freq[out] -= 1
                if freq[out] == 0:
                    del freq[out]           # ! 必须删，否则 len(freq) 会虚高
            if i >= k - 1 and len(freq) == k:   # ! k 个格子装了 k 个不同的键 ⇔ 无重复
                best = max(best, cur)
        return best


##################################################################################################
##### ! Solution 2: 维护「最近一次重复的位置」，用 distinct_start 判断
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：另一种状态设计 —— 记住每个值上次出现的位置，合法性变成「窗口左端 >= 上次重复位置」
##################################################################################################


class Solution_2:
    def maximumSubarraySum(self, nums: List[int], k: int) -> int:
        last = {}          # 值 -> 上次出现的下标
        dup_end = -1       # 最近一次重复发生的位置：窗口左端必须 > 它
        cur = best = 0
        for i, x in enumerate(nums):
            cur += x
            if i >= k:
                cur -= nums[i - k]
            if x in last and last[x] > dup_end:
                dup_end = last[x]           # ! 这个值上次出现的位置，之后的窗口不能跨过它
            last[x] = i
            left = i - k + 1
            if left >= 0 and left > dup_end:
                best = max(best, cur)
        return best


if __name__ == "__main__":
    import random
    cases = [([1, 5, 4, 2, 9, 9, 9], 3, 15), ([4, 4, 4], 3, 0), ([1, 2, 3], 3, 6),
             ([9], 1, 9), ([1, 1, 1, 7, 8, 9], 3, 24)]
    sols = [Solution_1(), Solution_2()]
    for sol in sols:
        for nums, k, want in cases:
            got = sol.maximumSubarraySum(nums[:], k)
            assert got == want, f"{type(sol).__name__} {nums} k={k}: got {got}, want {want}"
    rng = random.Random(2461)
    for _ in range(3000):
        n = rng.randint(1, 10); k = rng.randint(1, n)
        nums = [rng.randint(1, 5) for _ in range(n)]
        want = max((sum(nums[i:i + k]) for i in range(n - k + 1)
                    if len(set(nums[i:i + k])) == k), default=0)
        for sol in sols:
            assert sol.maximumSubarraySum(nums[:], k) == want, (type(sol).__name__, nums, k, want)
    print("2 个解法全过（含 3000 组随机对拍）")
