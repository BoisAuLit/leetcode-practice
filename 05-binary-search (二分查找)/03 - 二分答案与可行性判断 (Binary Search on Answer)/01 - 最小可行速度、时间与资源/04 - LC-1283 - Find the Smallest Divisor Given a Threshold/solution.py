"""LC-1283 - Find the Smallest Divisor Given a Threshold

Level 1 · 03 二分答案与可行性判断 —— Minimum Feasible Answer，可行性是「向上取整求和」
题目在问：选一个正整数除数 d，把每个 nums[i] 除以 d **向上取整**后求和，
         要求这个和 <= threshold，求最小的 d。

二分答案三件套：
  1. **答案空间**：`lo = 1`（最小正整数除数），`hi = max(nums)`
     （d = max(nums) 时每项都变成 1，总和 = n，题目保证 `threshold >= n`，所以一定可行）。
  2. **feasible(d)** = `sum(ceil(x / d) for x in nums) <= threshold`。
  3. **单调性**：d 越大，每一项的 ⌈x/d⌉ 越小 ⟹ 总和不增 ⟹ `F F F T T T` ⟹ First True。

向上取整的正确写法（这题最容易出错的地方）：
      ```python
      (x + d - 1) // d        # ✓ 整数运算，不会有浮点误差
      -(-x // d)              # ✓ 等价写法
      math.ceil(x / d)        # ✗ 大整数时浮点会掉精度
      ```
      本仓库统一用 `(x + d - 1) // d`。

为什么上界取 `max(nums)` 就够：
      当 `d >= max(nums)` 时，所有 ⌈x/d⌉ 都等于 1（x >= 1），总和恒为 n，
      再增大 d 也不会更小，所以答案不可能超过 `max(nums)`。

复杂度：**O(n · log(max(nums)))**，空间 O(1)。

和 LC-0875 Koko 的关系：Koko 求的是 `sum(ceil(pile/speed)) <= h` 的最小 speed。
      **这两题的 feasible 函数在数学上完全一样**，只是变量名从 speed 换成 divisor、
      从 h 换成 threshold。把它们并排放，就能看出「二分答案」真正的模板性在哪里。

边界：
  - nums=[1,2,5,9], threshold=6 → 5
  - nums=[44,22,33,11,1], threshold=5 → 44
  - 全 1 → 答案 1
  - threshold == n → 答案 max(nums)
  - 单元素
"""

from typing import List


##################################################################################################
##### ! Solution 1: 二分答案 + 整数向上取整求和（First True）
##### ! 时间复杂度: O(n · log(max(nums)))   空间复杂度: O(1)
##### ! 适用：和 LC-0875 Koko 共用同一个 feasible；记住一个就等于记住两个
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def smallestDivisor(self, nums: List[int], threshold: int) -> int:
        def total(d: int) -> int:
            return sum((x + d - 1) // d for x in nums)   # ! 整数向上取整，别用 math.ceil

        lo, hi = 1, max(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if total(mid) <= threshold:      # ! 可行 → 试更小的除数
                hi = mid
            else:
                lo = mid + 1
        return lo


##################################################################################################
##### ! Solution 2: 闭区间 + 显式记录候选答案（等价写法）
##### ! 时间复杂度: O(n · log(max(nums)))   空间复杂度: O(1)
##### ! 适用：不习惯左闭右开时；显式 ans 让「找最小可行」这件事更直白
##################################################################################################


class Solution_2:
    def smallestDivisor(self, nums: List[int], threshold: int) -> int:
        def total(d: int) -> int:
            return sum(-(-x // d) for x in nums)         # ! 另一种整数向上取整写法

        lo, hi, ans = 1, max(nums), max(nums)
        while lo <= hi:
            mid = (lo + hi) // 2
            if total(mid) <= threshold:
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1
        return ans


##################################################################################################
##### ! Solution 3: 从 1 开始逐个试（基准答案，用来对拍）
##### ! 时间复杂度: O(n · max(nums))   空间复杂度: O(1)
##### ! 适用：正确性参照，同时验证 feasible 的单调性
##################################################################################################


class Solution_3:
    def smallestDivisor(self, nums: List[int], threshold: int) -> int:
        for d in range(1, max(nums) + 1):
            if sum((x + d - 1) // d for x in nums) <= threshold:
                return d
        return max(nums)


if __name__ == "__main__":
    import random

    cases = [([1, 2, 5, 9], 6), ([44, 22, 33, 11, 1], 5), ([1, 1, 1], 3), ([19], 5), ([2, 3, 5, 7, 11], 11)]
    for nums, th in cases:
        a = Solution_1().smallestDivisor(nums, th)
        assert a == Solution_2().smallestDivisor(nums, th) == Solution_3().smallestDivisor(nums, th), (nums, th)
        print(f"nums={nums}, threshold={th} -> {a}")

    for _ in range(500):                 # ! 随机对拍（threshold >= n，符合题目约束）
        n = random.randint(1, 8)
        nums = [random.randint(1, 30) for _ in range(n)]
        th = random.randint(n, n * 10)
        assert (Solution_1().smallestDivisor(nums, th)
                == Solution_2().smallestDivisor(nums, th)
                == Solution_3().smallestDivisor(nums, th)), (nums, th)
    print("随机对拍 500 组通过 ✓")
