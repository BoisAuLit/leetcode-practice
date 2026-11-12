"""LC-0456 - 132 Pattern

Level 1 · 01 最近更大元素与跨度 —— 从右往左扫描 + 追踪「刚刚被弹出的最大值」
题目在问：是否存在下标 i < j < k 使得 nums[i] < nums[k] < nums[j]（即 1 - 3 - 2 的形状）。

为什么它值得单独占一个 Level 2：
  前面 496/739/901 的单调栈都是「当前元素来了，解决过去元素的答案」。
  这题的不变量完全不同 —— 它要同时握住**两个**信息：
    - 栈里：候选的「3」（较大的中间值）
    - 栈外一个变量 `third`：**已经被弹出过的最大值**，它天然满足 `third < 某个还在栈里的 3`
  只要再遇到一个比 `third` 还小的数，1-3-2 就凑齐了。

决定性观察（这是全题的核心）：
  1. 从**右往左**扫。维护一个单调递减栈（从栈底到栈顶值递减）。
  2. 当 nums[i] 把栈顶弹出时，被弹出的那些值都 **< nums[i]**。
     把它们之中最大的记到 `third`。此刻的事实是：
         存在 j = i，k 在 i 右边，且 **nums[k] = third < nums[j] = nums[i]**。
     也就是「3」和「2」已经就位，只差左边一个更小的「1」。
  3. 继续往左扫，一旦遇到 `nums[i] < third`，这个 nums[i] 就是「1」，答案为 True。

Stack 里存什么：**值**（存下标也行，这里存值最省事），从栈底到栈顶单调递减。
Pop 条件：`stack[-1] < nums[i]`，弹出时 `third = max(third, 弹出的值)`。
      实际上因为栈是递减的，连续弹出的最后一个就是最大的，`third = 弹出的最后一个` 也对，
      但写成 max 更不容易出错。

为什么 Pop 安全：被弹出的值 v < nums[i]，而 v 在 nums[i] 的右边。
      对将来（更左边）的任何 i' 来说，nums[i] 是比 v 更好的「3」候选
      （更大的 3 更容易满足 1 < 2 < 3），而 v 作为「2」的价值已经被 `third` 记下了。
      所以 v 本身可以扔掉，信息没丢。

复杂度：O(n) 时间（每个元素最多入栈出栈各一次），O(n) 空间。

边界：
  - [1,2,3,4]   → False（单调递增永远凑不出 132）
  - [3,1,4,2]   → True （1 < 2 < 4）
  - [-1,3,2,0]  → True （-1 < 0 < 3，也有 -1 < 2 < 3）
  - [1,2]       → False（长度不足 3）
  - [3,3,3]     → False（需要严格 nums[i] < nums[k] < nums[j]）
"""

from typing import List


##################################################################################################
##### ! Solution 1: 从右往左单调递减栈 + third = 被弹出的最大值
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：需要「一个较大值 + 一个次大值」成对出现的模式；132 / 类似的三元组形状题
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def find132pattern(self, nums: List[int]) -> bool:
        stack: List[int] = []            # ! 值，从栈底到栈顶单调递减 —— 候选的「3」
        third = float("-inf")            # ! 已经被弹出过的最大值 —— 当前最好的「2」
        for x in reversed(nums):         # ! 必须从右往左
            if x < third:                # ! 找到「1」：x < third < 某个在 x 右边的 3
                return True
            while stack and stack[-1] < x:
                third = max(third, stack.pop())   # ! 弹出的都比 x 小，升级「2」
            stack.append(x)
        return False


##################################################################################################
##### ! Solution 2: 枚举「3」的下标 j，左边维护前缀最小值当「1」，右边用有序容器找「2」
##### ! 时间复杂度: O(n^2)（纯 Python 不用 SortedList 时）   空间复杂度: O(n)
##### ! 适用：帮助理解「1 取前缀最小一定最优」这一步；面试里仍然写 Solution_1
##################################################################################################


class Solution_2:
    def find132pattern(self, nums: List[int]) -> bool:
        n = len(nums)
        if n < 3:
            return False
        prefix_min = [nums[0]] * n
        for i in range(1, n):
            prefix_min[i] = min(prefix_min[i - 1], nums[i])   # ! 「1」取左边最小一定不吃亏
        for j in range(1, n - 1):
            lo = prefix_min[j - 1]                            # ! 候选的「1」
            if lo >= nums[j]:
                continue                                      # ! 连 1 < 3 都不满足
            for k in range(j + 1, n):
                if lo < nums[k] < nums[j]:                    # ! 「2」夹在中间
                    return True
        return False


##################################################################################################
##### ! Solution 3: 三重循环暴力（基准答案，用来对拍）
##### ! 时间复杂度: O(n^3)   空间复杂度: O(1)
##### ! 适用：正确性参照
##################################################################################################


class Solution_3:
    def find132pattern(self, nums: List[int]) -> bool:
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if nums[i] < nums[k] < nums[j]:
                        return True
        return False


if __name__ == "__main__":
    import random

    cases = [[1, 2, 3, 4], [3, 1, 4, 2], [-1, 3, 2, 0], [1, 2], [3, 3, 3], [1, 0, 1, -4, -3]]
    for nums in cases:
        a = Solution_1().find132pattern(nums)
        assert a == Solution_2().find132pattern(nums) == Solution_3().find132pattern(nums), nums
        print(f"{nums} -> {a}")

    for _ in range(500):                 # ! 小值域随机对拍，专打重复元素
        nums = [random.randint(-3, 3) for _ in range(random.randint(0, 8))]
        assert (Solution_1().find132pattern(nums)
                == Solution_2().find132pattern(nums)
                == Solution_3().find132pattern(nums)), nums
    print("随机对拍 500 组通过 ✓")
