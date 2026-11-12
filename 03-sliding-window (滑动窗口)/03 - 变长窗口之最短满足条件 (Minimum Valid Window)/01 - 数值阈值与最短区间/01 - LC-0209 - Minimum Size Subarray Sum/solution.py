"""LC-0209 - Minimum Size Subarray Sum

Level 1 · 03 最短满足条件 —— Minimum Valid Window（最短合法窗口）
题目在问：和 >= target 的最短连续子数组长度（不存在返回 0）

和「最长合法窗口」的根本区别（这是本层最该记住的一句）：
  - **最长合法**（0003 / 0904 / 1004）：窗口**不合法时**收缩，收缩是为了恢复合法；
    答案在「收缩完成后」更新。
  - **最短满足**（本题 / 0076）：窗口**合法时**收缩，收缩是为了找更短的；
    答案在「每次收缩前」更新，然后继续缩到不合法为止。
  两者 while 的判断条件正好相反，写反了会得到完全错误的答案。

Loop Invariant：进入内层 while 时 `cur >= target`；
      每次吐掉左端前先用当前长度更新答案，吐完如果还 >= target 就继续吐。

**正确性依赖 `nums[i] > 0`**：窗口变长和只增不减，所以
  「以 right 结尾的最短合法窗口」的左端随 right 单调右移，left 不用回退 ⇒ O(n)。
  **一旦允许负数，这个单调性就没了** —— 见同目录的 LC-0862，
  那时要改用「前缀和 + 单调队列」。

坑：
  - 没有任何合法窗口时返回 0，不是 -1 也不是 inf
  - 内层是 while 不是 if
  - 答案更新要在吐掉左端**之前**（此时窗口还是合法的）
"""

from typing import List


##################################################################################################
##### ! Solution 1: 变长窗口，合法时收缩
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：全正数数组上「和 >= target 的最短区间」的标准答案
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        left = 0
        cur = 0
        best = len(nums) + 1
        for right, x in enumerate(nums):
            cur += x
            while cur >= target:                 # ! 合法就收缩，边缩边记
                best = min(best, right - left + 1)
                cur -= nums[left]
                left += 1
        return best if best <= len(nums) else 0


##################################################################################################
##### ! Solution 2: 前缀和 + 二分
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：题目追问 O(n log n) 解法时给它；前缀和递增（全正数）才能二分
##################################################################################################


class Solution_2:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        import bisect
        pre = [0]
        for x in nums:
            pre.append(pre[-1] + x)
        best = len(nums) + 1
        for i in range(len(nums) + 1):
            # ! 找最小的 j 使 pre[j] >= pre[i] + target
            j = bisect.bisect_left(pre, pre[i] + target)
            if j <= len(nums):
                best = min(best, j - i)
        return best if best <= len(nums) else 0


if __name__ == "__main__":
    import random
    cases = [(7, [2, 3, 1, 2, 4, 3], 2), (4, [1, 4, 4], 1), (11, [1, 1, 1, 1, 1, 1, 1, 1], 0),
             (1, [1], 1), (100, [], 0)]
    sols = [Solution_1(), Solution_2()]
    for sol in sols:
        for t, nums, want in cases:
            got = sol.minSubArrayLen(t, nums[:])
            assert got == want, f"{type(sol).__name__} t={t} {nums}: got {got}, want {want}"
    rng = random.Random(209)
    for _ in range(3000):
        nums = [rng.randint(1, 9) for _ in range(rng.randint(0, 10))]
        t = rng.randint(1, 25)
        want = min((j - i + 1 for i in range(len(nums)) for j in range(i, len(nums))
                    if sum(nums[i:j + 1]) >= t), default=0)
        for sol in sols:
            assert sol.minSubArrayLen(t, nums[:]) == want, (type(sol).__name__, t, nums, want)
    print("2 个解法全过（含 3000 组随机对拍）")
