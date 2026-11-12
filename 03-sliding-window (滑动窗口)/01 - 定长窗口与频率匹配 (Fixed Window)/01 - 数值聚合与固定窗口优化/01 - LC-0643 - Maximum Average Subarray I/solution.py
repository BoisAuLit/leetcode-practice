"""LC-0643 - Maximum Average Subarray I

Level 1 · 01 定长窗口 —— 最标准的 Fixed-size Sliding Window（定长滑动窗口）
题目在问：长度恰好为 k 的连续子数组里，平均值最大是多少

决定性观察：长度固定 ⇒ **最大平均值等价于最大和**，除法只在最后做一次。
      相邻两个窗口只差两个元素：右边进一个、左边出一个，所以窗口和可以 O(1) 更新。

Loop Invariant（循环不变量）：处理完下标 i 时，`cur` 恰好等于 `nums[i-k+1 .. i]` 的和。
      只要「先加右、再减左」的顺序不乱，这条就一直成立。

Window Expansion / Shrinking Rule：定长窗口**没有收缩判断** ——
      每一步都是「进一个、出一个」，窗口长度恒为 k。这是它和变长窗口最大的区别：
      变长窗口的 left 由约束驱动，定长窗口的 left 由 right 机械地决定（`left = right - k + 1`）。

Answer Update Timing：窗口刚好满 k 个元素时（`i >= k - 1`）更新答案。

坑：
  - 用 `float` 返回；先求整数和、最后除一次，避免逐步累加浮点误差
  - 答案初值不能设 0（数组可以全是负数），要用第一个窗口的和或者 -inf
  - `i >= k - 1` 的边界：写成 `i >= k` 会漏掉第一个窗口
"""

from typing import List


##################################################################################################
##### ! Solution 1: 定长窗口，进一个出一个
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：所有定长窗口题的骨架；1456、1052、2461 都是在这上面加一个额外的窗口状态
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        cur = sum(nums[:k])          # ! 第一个窗口单独算
        best = cur
        for i in range(k, len(nums)):
            cur += nums[i] - nums[i - k]   # ! 进一个、出一个，O(1) 更新
            best = max(best, cur)
        return best / k              # ! 除法只做一次


##################################################################################################
##### ! Solution 2: 前缀和（Prefix Sum）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：窗口长度会变、或者要多次查询任意区间时用它；定长窗口的场景下它多花了 O(n) 空间
##################################################################################################


class Solution_2:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        pre = [0]
        for x in nums:
            pre.append(pre[-1] + x)
        best = max(pre[i + k] - pre[i] for i in range(len(nums) - k + 1))
        return best / k


if __name__ == "__main__":
    import random
    cases = [([1, 12, -5, -6, 50, 3], 4, 12.75), ([5], 1, 5.0),
             ([-1, -2, -3], 2, -1.5), ([0, 4, 0, 3, 2], 1, 4.0)]
    sols = [Solution_1(), Solution_2()]
    for sol in sols:
        for nums, k, want in cases:
            got = sol.findMaxAverage(nums[:], k)
            assert abs(got - want) < 1e-9, f"{type(sol).__name__} {nums} k={k}: got {got}, want {want}"
    rng = random.Random(643)
    for _ in range(3000):
        n = rng.randint(1, 10); k = rng.randint(1, n)
        nums = [rng.randint(-10, 10) for _ in range(n)]
        want = max(sum(nums[i:i + k]) for i in range(n - k + 1)) / k   # 暴力
        for sol in sols:
            assert abs(sol.findMaxAverage(nums[:], k) - want) < 1e-9, (type(sol).__name__, nums, k)
    print("2 个解法全过（含 3000 组随机对拍）")
