"""LC-2104 - Sum of Subarray Ranges

Level 1 · 02 单调边界、矩形与贡献计算 —— LC-0907 的直接延伸
题目在问：所有连续子数组的 range（= max - min）之和。**本题不取模**（和 LC-0907 的区别之一）。

（原文件里只有一个空的 `class Solution` 占位，没有函数体，这里补全；没有删除任何已有实现。）

决定性观察：
  1. 求和可以拆开：
         Σ (max - min) = Σ max − Σ min
     于是问题拆成两个独立的子问题，都用 LC-0907 的贡献法（Contribution Counting）。
  2. Σ min 完全复用 LC-0907；Σ max 只需要把所有比较符号反过来（递减栈 / 更大边界）。

两边的 Tie Breaking 必须各自一致（否则重复元素会重复计数）：
        Σ min：left = Previous Strictly Smaller，right = Next Smaller or Equal
        Σ max：left = Previous Strictly Greater，right = Next Greater or Equal
  实现上就是：求 min 用「严格大于才弹」的递增栈；求 max 用「严格小于才弹」的递减栈。
  用 [2,2,2] 验证：Σmax = Σmin = 12 → 答案 0（所有子数组的 max==min）。

和 LC-0907 的三个区别（容易混，单独记）：
  1. 907 要对 1e9+7 取模，**2104 不取模**。
  2. 907 只算 min，2104 要 max 和 min 两套边界。
  3. 2104 原题 n <= 1000，**O(n^2) 暴力本来就能过**；O(n) 单调栈是进阶要求。
     两种解法都保留在下面，面试里被追问 follow-up 时要能给出 O(n) 版。

复杂度：Solution_1 O(n) 时间 / O(n) 空间；Solution_2 O(n^2) 时间 / O(1) 空间。
"""

from typing import List


##################################################################################################
##### ! Solution 1: 贡献法 —— Σmax − Σmin，各跑一次单调栈
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：n 很大时的正解；也是把 LC-0907 的模板「照镜子」复用一次的练习
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def subArrayRanges(self, nums: List[int]) -> int:
        return self._sum_of_extreme(nums, want_max=True) - self._sum_of_extreme(nums, want_max=False)

    @staticmethod
    def _sum_of_extreme(nums: List[int], want_max: bool) -> int:
        """want_max=True 求 Σ(所有子数组的 max)，False 求 Σ(所有子数组的 min)。"""
        n = len(nums)
        stack: List[int] = []
        total = 0
        for i in range(n + 1):
            if i == n:
                cur = float("inf") if want_max else float("-inf")   # ! 哨兵，方向相反
            else:
                cur = nums[i]
            # ! 求 max 用递减栈（严格小于才弹）；求 min 用递增栈（严格大于才弹）
            while stack and (nums[stack[-1]] < cur if want_max else nums[stack[-1]] > cur):
                j = stack.pop()
                left = stack[-1] if stack else -1
                total += nums[j] * (j - left) * (i - j)
            stack.append(i)
        return total


##################################################################################################
##### ! Solution 2: O(n^2) 枚举左端点，右端点滚动维护 max / min
##### ! 时间复杂度: O(n^2)   空间复杂度: O(1)
##### ! 适用：原题 n <= 1000，这版足够通过；写起来几乎不会错，也是对拍基准
##################################################################################################


class Solution_2:
    def subArrayRanges(self, nums: List[int]) -> int:
        n = len(nums)
        total = 0
        for i in range(n):
            lo = hi = nums[i]
            for j in range(i + 1, n):          # ! 从 j=i+1 开始：长度为 1 的子数组 range 恒为 0
                lo = min(lo, nums[j])
                hi = max(hi, nums[j])
                total += hi - lo
        return total


if __name__ == "__main__":
    import random

    cases = [[1, 2, 3], [1, 3, 3], [4, -2, -3, 4, 1], [2, 2, 2], [5], [1, 1]]
    for nums in cases:
        a = Solution_1().subArrayRanges(nums)
        assert a == Solution_2().subArrayRanges(nums), (nums, a, Solution_2().subArrayRanges(nums))
        print(f"{nums} -> {a}")

    for _ in range(500):                 # ! 含负数 + 重复值的随机对拍
        nums = [random.randint(-3, 3) for _ in range(random.randint(1, 12))]
        assert Solution_1().subArrayRanges(nums) == Solution_2().subArrayRanges(nums), nums
    print("随机对拍 500 组通过 ✓")
