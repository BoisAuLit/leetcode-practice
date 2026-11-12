"""LC-1658 - Minimum Operations to Reduce X to Zero

Level 1 · 06 高阶窗口 / 02 Complement Window（补集窗口）
题目在问：每次只能从数组最左或最右拿走一个数并从 x 中扣掉它，最少几次能让 x 恰好为 0

决定性观察（和 LC-1423 同一个转化，但固定的东西不同）：
      **从两端拿走若干个 ⟺ 中间留下一段连续区间。**
      拿走的总和要等于 x ⟺ **留下的那段和恰好等于 `total - x`**。
      要「拿的次数最少」⟺ 「留下的那段**最长**」。
      于是问题变成：和恰好为 `target = total - x` 的**最长**子数组。

和 LC-1423 的对照（两题必须一起记）：
  - **1423**：固定**长度**（留下 n-k 个）⇒ 定长窗口求最小和
  - **1658**：固定**和**（留下和为 total-x）⇒ 变长窗口求最长长度

为什么能用滑动窗口：`nums[i] >= 1`（全正），所以窗口和随长度单调递增，
      「和 > target 就收缩」这条规则能让 left 单调右移。
      **有负数就不行了**，那时要用前缀和 + 哈希表（解法 2，也更通用）。

坑：
  - `target < 0` 直接返回 -1；`target == 0` 的答案是 n（全拿走），窗口法天然覆盖
  - 找不到合法窗口要返回 -1，不是 0
  - 答案是 `n - 最长长度`，不是最长长度本身
"""

from typing import List


##################################################################################################
##### ! Solution 1: 补集转化 + 变长窗口求「和为 target 的最长子数组」
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：所有「从两端操作」的题；关键一步是把「拿走什么」翻译成「留下什么」
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def minOperations(self, nums: List[int], x: int) -> int:
        target = sum(nums) - x
        if target < 0:
            return -1
        left = 0
        cur = 0
        longest = -1
        for right, v in enumerate(nums):
            cur += v
            while cur > target and left <= right:   # ! 全正数，和超了就收缩
                cur -= nums[left]
                left += 1
            if cur == target:
                longest = max(longest, right - left + 1)
        if target == 0:
            longest = max(longest, 0)               # ! 空窗口也合法：全部拿走
        return len(nums) - longest if longest >= 0 else -1


##################################################################################################
##### ! Solution 2: 前缀和 + 哈希表（和为 target 的最长子数组，LC-0325 的壳）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：★ 更通用 —— 数组有负数时窗口法失效，这个仍然成立
##################################################################################################


class Solution_2:
    def minOperations(self, nums: List[int], x: int) -> int:
        target = sum(nums) - x
        if target < 0:
            return -1
        first = {0: -1}        # 前缀和 -> 第一次出现的下标（求最长，只记第一次）
        pre = 0
        # ! target == 0 时「留空窗口」就是合法答案（全部拿走），长度 0 必须先认下来
        longest = 0 if target == 0 else -1
        for i, v in enumerate(nums):
            pre += v
            if pre - target in first:
                longest = max(longest, i - first[pre - target])
            if pre not in first:
                first[pre] = i
        return len(nums) - longest if longest >= 0 else -1


if __name__ == "__main__":
    import random
    cases = [([1, 1, 4, 2, 3], 5, 2), ([5, 6, 7, 8, 9], 4, -1),
             ([3, 2, 20, 1, 1, 3], 10, 5), ([1, 1], 3, -1), ([1, 1], 2, 2), ([5, 2, 3, 1, 1], 5, 1)]
    sols = [Solution_1(), Solution_2()]
    for sol in sols:
        for nums, x, want in cases:
            got = sol.minOperations(nums[:], x)
            assert got == want, f"{type(sol).__name__} {nums} x={x}: got {got}, want {want}"
    rng = random.Random(1658)
    for _ in range(3000):
        nums = [rng.randint(1, 6) for _ in range(rng.randint(1, 9))]
        x = rng.randint(1, 20)
        # 暴力：枚举左边拿 i 个、右边拿 j 个
        best = -1
        n = len(nums)
        for i in range(n + 1):
            for j in range(n - i + 1):
                if sum(nums[:i]) + (sum(nums[n - j:]) if j else 0) == x:
                    best = i + j if best < 0 else min(best, i + j)
        for sol in sols:
            assert sol.minOperations(nums[:], x) == best, (type(sol).__name__, nums, x, best)
    print("2 个解法全过（含 3000 组随机对拍）")
