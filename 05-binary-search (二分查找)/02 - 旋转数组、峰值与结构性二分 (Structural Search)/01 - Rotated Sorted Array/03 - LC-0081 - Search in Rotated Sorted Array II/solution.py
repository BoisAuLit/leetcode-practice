"""LC-0081 - Search in Rotated Sorted Array II（第二轮自主新增）

Level 1 · 02 旋转数组、峰值与结构性二分 —— **有重复元素**时旋转数组二分的退化
题目在问：LC-0033 的加强版，数组可能含重复元素，只需判断 target 是否存在。

为什么新增它（这是全专题最重要的一个"反例"）：
  LC-0033 的正确性论证是：「`nums[lo] <= nums[mid]` ⟹ 左半段一定有序」。
  **一旦允许重复，这个论证就不成立了。**
  反例：`[3,1,3,3,3]`，lo=0, mid=2 时 `nums[lo] == nums[mid] == 3`，
  但左半段 `[3,1,3]` 根本不是有序的。
  不做任何处理直接套 033 的代码，这个用例就会返回错误答案。

  有这道题在，才能真正理解 033 的证明**依赖了哪个前提**，
  而不是把 033 当成一段背下来的代码。

决定性观察：
  1. 问题出在 `nums[lo] == nums[mid]` 时**无法判断哪半边有序**。
  2. 这种情况下唯一安全的动作是 **`lo += 1`**（去掉一个重复元素，缩小一点点）。
     为什么安全：`nums[lo] == nums[mid]`，所以丢掉 `nums[lo]` 不会丢掉唯一的 target
     —— 即使 `nums[lo] == target`，`nums[mid]` 也等于 target，我们已经检查过 mid 了。
  3. 代价：最坏情况退化成 **O(n)**。
     极端例子 `[1,1,1,1,1,0,1]` 找 0 —— 每一步只能排除一个元素。
     **这是本题的重点结论：有重复元素时，旋转数组搜索无法保证 O(log n)。**

Loop Invariant（闭区间 `[lo, hi]`）：target 如果存在，一定在 `[lo, hi]` 内。

为什么 LC-0081 只问「存在与否」而不问下标：
      有重复时 target 可能出现在多个位置，返回哪一个没有意义。

复杂度：平均 O(log n)，**最坏 O(n)**；空间 O(1)。
      这个「最坏 O(n)」必须主动说出来，面试官通常就是在考这一点。

LC-0154（Find Minimum in Rotated Sorted Array II）是同一个退化现象的另一面，
      处理办法同样是遇到相等就 `hi -= 1`。

边界：
  - [2,5,6,0,0,1,2], target=0 → True
  - [2,5,6,0,0,1,2], target=3 → False
  - [1,0,1,1,1], target=0 → True（必须靠 lo += 1 才能走到 0）
  - [1,1,1,1,1], target=2 → False（最坏情况，退化成线性）
  - [1], target=1 → True
"""

from typing import List


##################################################################################################
##### ! Solution 1: 旋转二分 + 「两端相等就收缩一格」处理重复
##### ! 时间复杂度: 平均 O(log n)，**最坏 O(n)**   空间复杂度: O(1)
##### ! 适用：允许重复元素的旋转数组；也是理解 LC-0033 前提条件的反例题
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def search(self, nums: List[int], target: int) -> bool:
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return True
            if nums[lo] == nums[mid] and nums[mid] == nums[hi]:
                # ! 两端都和 mid 相等 → 无法判断哪半有序，只能各收缩一格（退化到 O(n) 的根源）
                lo += 1
                hi -= 1
            elif nums[lo] <= nums[mid]:          # ! 左半段有序（此时能确定了）
                if nums[lo] <= target < nums[mid]:
                    hi = mid - 1
                else:
                    lo = mid + 1
            else:                                 # ! 右半段有序
                if nums[mid] < target <= nums[hi]:
                    lo = mid + 1
                else:
                    hi = mid - 1
        return False


##################################################################################################
##### ! Solution 2: 先去掉首尾的重复，再套 LC-0033 的标准旋转二分
##### ! 时间复杂度: 平均 O(log n)，最坏 O(n)   空间复杂度: O(1)
##### ! 适用：想复用 033 代码时；预处理之后 nums[lo] != nums[hi]，033 的论证重新成立
##################################################################################################


class Solution_2:
    def search(self, nums: List[int], target: int) -> bool:
        lo, hi = 0, len(nums) - 1
        while lo < hi and nums[lo] == nums[hi]:
            hi -= 1                               # ! 去掉尾部和头部相同的那一段（最坏 O(n)）
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return True
            if nums[lo] <= nums[mid]:
                if nums[lo] <= target < nums[mid]:
                    hi = mid - 1
                else:
                    lo = mid + 1
            else:
                if nums[mid] < target <= nums[hi]:
                    lo = mid + 1
                else:
                    hi = mid - 1
        return False


##################################################################################################
##### ! Solution 3: 线性扫描（基准答案，用来对拍）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：正确性参照 —— 本题最坏情况下二分并不比它快
##################################################################################################


class Solution_3:
    def search(self, nums: List[int], target: int) -> bool:
        return target in nums


if __name__ == "__main__":
    import random

    cases = [([2, 5, 6, 0, 0, 1, 2], 0), ([2, 5, 6, 0, 0, 1, 2], 3), ([1, 0, 1, 1, 1], 0),
             ([1, 1, 1, 1, 1], 2), ([1], 1), ([1], 0), ([3, 1, 3, 3, 3], 1)]
    for nums, t in cases:
        a = Solution_1().search(nums, t)
        assert a == Solution_2().search(nums, t) == Solution_3().search(nums, t), (nums, t)
        print(f"{nums}, target={t} -> {a}")

    for _ in range(2000):                # ! 随机旋转 + 大量重复元素对拍
        n = random.randint(1, 10)
        base = sorted(random.randint(0, 4) for _ in range(n))
        k = random.randint(0, n - 1)
        nums = base[k:] + base[:k]
        t = random.randint(-1, 5)
        assert (Solution_1().search(nums, t)
                == Solution_2().search(nums, t)
                == Solution_3().search(nums, t)), (nums, t)
    print("随机对拍 2000 组通过 ✓（重复元素密集）")
