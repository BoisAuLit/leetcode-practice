"""LC-1856 - Maximum Subarray Min-Product

Level 1 · 02 单调边界、矩形与贡献计算 —— Monotonic Boundaries + Prefix Sum（第二轮自主新增）
题目在问：子数组的 min-product = min(子数组) * sum(子数组)，求最大的 min-product，对 1e9+7 取模。

为什么把它放进这个 Level 2（新增理由）：
  它和 LC-0084 是**同一个骨架、不同的目标函数**：
        LC-0084：以 h 为最小高度 → 价值 = h * 宽度
        LC-1856：以 x 为最小元素 → 价值 = x * 区间和
  把「宽度」换成「前缀和之差」，模板原样复用。这正是边界法最值钱的迁移点，
  练完它，以后见到「以某个元素为极值的最优区间」就知道该干什么。

决定性观察：
  1. 枚举「谁是这个子数组的最小值」。设是 nums[i]，
     则在 nums[i] 保持为最小值的前提下，**区间越大越好**（题目保证 nums[i] >= 1，
     所以元素都是正数，区间变大只会让 sum 变大，不会变小）。
  2. 因此最优区间就是 nums[i] 能统治的最大范围 (left, right)（开区间）：
        left  = 左边第一个比它小的下标
        right = 右边第一个比它小的下标
  3. 该区间的和用前缀和 O(1) 算出：sum = prefix[right] - prefix[left+1]。
     候选答案 = nums[i] * sum，取所有 i 的最大值。

元素全为正是前提：如果允许负数，「区间越大 sum 越大」就不成立，这题的贪心会崩。
      这一点必须记住 —— 不能把这个模板无条件搬到含负数的题上。

重复元素：这题只求**最大值**，不是求和，所以即使相等元素被重复统计也不会错
      （它们算出来的候选值相同）。两边都用「严格更小」或一严格一非严格都能得到正确答案。
      本文件用和 LC-0907 一致的约定（递增栈，严格大于才弹），保持模板统一。

取模的坑：**先在未取模的大整数上比较出最大值，最后才取模**。
      如果边算边取模再比大小，会把一个很大的数模成小数而选错。
      Python 整数无上限，天然不会溢出，但这个顺序在 C++/Java 里是必须的，面试要说出来。

复杂度：O(n) 时间，O(n) 空间。

边界：
  - [1,2,3,2] → 14（以 2 为最小值覆盖 [2,3,2]，2*7=14）
  - [2,3,3,1,2] → 18（以 3 为最小值覆盖 [3,3]，3*6=18）
  - [3,1,5,6,4,2] → 60（以 5 为最小值覆盖 [5,6]，5*11=55；以 4 → 4*15=60）
  - 单元素 [7] → 49
  - 全相等 [2,2,2] → 2*6 = 12
"""

from itertools import accumulate
from typing import List

MOD = 10**9 + 7


##################################################################################################
##### ! Solution 1: 单调递增索引栈求左右边界 + 前缀和 O(1) 取区间和
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：「以某元素为最小值的最优区间」一类题；LC-0084 的目标函数替换版
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def maxSumMinProduct(self, nums: List[int]) -> int:
        n = len(nums)
        prefix = [0] + list(accumulate(nums))     # ! prefix[k] = nums[0..k-1] 之和
        stack: List[int] = []                     # ! 存下标，对应值单调不减
        best = 0
        for i in range(n + 1):
            cur = float("-inf") if i == n else nums[i]        # ! 末尾哨兵，清空栈
            while stack and nums[stack[-1]] > cur:
                j = stack.pop()
                left = stack[-1] if stack else -1             # ! 左边第一个更小
                total = prefix[i] - prefix[left + 1]          # ! 开区间 (left, i) 的元素和
                best = max(best, nums[j] * total)             # ! 先比大小，不要在这里取模
            stack.append(i)
        return best % MOD                                     # ! 最后才取模


##################################################################################################
##### ! Solution 2: 两趟单调栈先算 left[] / right[]，再统一结算（分步版，更好读）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：想把「求边界」和「算价值」解耦时；改目标函数只需要动最后一行
##################################################################################################


class Solution_2:
    def maxSumMinProduct(self, nums: List[int]) -> int:
        n = len(nums)
        prefix = [0] + list(accumulate(nums))
        left = [-1] * n
        right = [n] * n
        stack: List[int] = []
        for i in range(n):
            while stack and nums[stack[-1]] >= nums[i]:
                stack.pop()
            left[i] = stack[-1] if stack else -1
            stack.append(i)
        stack.clear()
        for i in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] > nums[i]:
                stack.pop()
            right[i] = stack[-1] if stack else n
            stack.append(i)
        best = max(nums[i] * (prefix[right[i]] - prefix[left[i] + 1]) for i in range(n))
        return best % MOD


##################################################################################################
##### ! Solution 3: 暴力枚举所有子数组（基准答案，用来对拍）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(1)
##### ! 适用：正确性参照
##################################################################################################


class Solution_3:
    def maxSumMinProduct(self, nums: List[int]) -> int:
        n = len(nums)
        best = 0
        for i in range(n):
            lo = nums[i]
            total = 0
            for j in range(i, n):
                lo = min(lo, nums[j])
                total += nums[j]
                best = max(best, lo * total)
        return best % MOD


if __name__ == "__main__":
    import random

    cases = [[1, 2, 3, 2], [2, 3, 3, 1, 2], [3, 1, 5, 6, 4, 2], [7], [2, 2, 2]]
    for nums in cases:
        a = Solution_1().maxSumMinProduct(nums)
        assert a == Solution_2().maxSumMinProduct(nums) == Solution_3().maxSumMinProduct(nums), nums
        print(f"{nums} -> {a}")

    for _ in range(500):                 # ! 正整数随机对拍（题目保证 nums[i] >= 1）
        nums = [random.randint(1, 5) for _ in range(random.randint(1, 12))]
        assert (Solution_1().maxSumMinProduct(nums)
                == Solution_2().maxSumMinProduct(nums)
                == Solution_3().maxSumMinProduct(nums)), nums
    print("随机对拍 500 组通过 ✓")
