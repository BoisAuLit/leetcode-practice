"""LC-0907 - Sum of Subarray Minimums

Level 1 · 02 单调边界、矩形与贡献计算 —— Contribution Counting（贡献计数）的标准题
题目在问：所有非空连续子数组的最小值之和，对 1e9+7 取模。

决定性观察（换枚举方向，这是全题的灵魂）：
  1. 不要枚举「每个子数组 → 它的最小值」（那是 O(n^2) 甚至 O(n^3)）。
     要枚举「**每个元素 → 它是多少个子数组的最小值**」。
  2. 对 nums[i]，设它作为最小值时能覆盖的最大区间是 (left, right)（开区间）：
         left  = 左边第一个「更小」的下标
         right = 右边第一个「更小」的下标
     那么起点可以是 left+1 .. i，共 **(i - left)** 种；
     终点可以是 i .. right-1，共 **(right - i)** 种；
     左右是独立选的，所以相乘。
  3. 贡献 = nums[i] * (i - left) * (right - i)，全部加起来就是答案。

重复元素的 Tie Breaking（这题最容易错的地方）：
  如果左右都用「严格更小」，那么 [1,1] 里两个 1 都会把整段 [1,1] 算成自己的，**重复计数**。
  必须一边严格、一边非严格，把相等的情况**只判给其中一侧**。本文件采用：
        left  = Previous **Strictly** Smaller   （左边第一个 nums[j] <  nums[i]）
        right = Next **Smaller or Equal**       （右边第一个 nums[j] <= nums[i]）
  等价说法：一串相等的元素里，只有**最左边那个**有权把整串算进自己的区间。
  必须用 [1,1] 和 [2,2,2] 验证：
        [1,1]   → 子数组 [1],[1],[1,1] 的最小值和 = 3
        [2,2,2] → 6 个子数组，最小值都是 2 → 12

单调栈怎么一次扫完：维护**单调递增**的索引栈，
  Pop 条件用 `nums[stack[-1]] > cur`（**严格大于**才弹，相等的留在栈里）。
  这正好实现了上面的约定：相等时后来者不把前面的弹掉 → 前面那个保住了更大的区间。
  被弹出的 j 结算时：right = 当前 i，left = 弹完之后的新栈顶（没有就是 -1）。
  末尾补一个 -inf 哨兵（Sentinel），把栈清空。

复杂度：O(n) 时间（每个下标最多入栈出栈各一次），O(n) 空间。
取模：答案可能极大，最后对 1e9+7 取模。注意 LC-2104 **不**取模，两题不要混。
"""

from typing import List

MOD = 10**9 + 7


##################################################################################################
##### ! Solution 1: 单调递增索引栈，一次扫描边弹边结算贡献
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：所有「所有子数组的 min/max 之和 / 之积 / 计数」类题；贡献法的标准模板
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def sumSubarrayMins(self, arr: List[int]) -> int:
        n = len(arr)
        stack: List[int] = []            # ! 存下标，对应值单调不减
        total = 0
        for i in range(n + 1):
            cur = float("-inf") if i == n else arr[i]      # ! 末尾哨兵，负无穷把栈全部清空
            while stack and arr[stack[-1]] > cur:          # ! 严格大于才弹 → 相等留栈里，避免重复计数
                j = stack.pop()
                left = stack[-1] if stack else -1          # ! 左边第一个严格更小
                total += arr[j] * (j - left) * (i - j)     # ! 右边第一个「更小或相等」就是 i
            stack.append(i)
        return total % MOD


##################################################################################################
##### ! Solution 2: 先用两趟单调栈分别求出 left[] / right[]，再统一求和（分步更好读）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：第一次学贡献法时用这版把「两个边界」看清楚；也方便改成 max 版本
##################################################################################################


class Solution_2:
    def sumSubarrayMins(self, arr: List[int]) -> int:
        n = len(arr)
        left = [-1] * n                  # ! Previous Strictly Smaller
        right = [n] * n                  # ! Next Smaller or Equal
        stack: List[int] = []
        for i in range(n):               # ! 左边界：弹掉所有 >= 的，剩下栈顶就是严格更小
            while stack and arr[stack[-1]] >= arr[i]:
                stack.pop()
            left[i] = stack[-1] if stack else -1
            stack.append(i)
        stack.clear()
        for i in range(n - 1, -1, -1):   # ! 右边界：弹掉所有 > 的，剩下栈顶是「更小或相等」
            while stack and arr[stack[-1]] > arr[i]:
                stack.pop()
            right[i] = stack[-1] if stack else n
            stack.append(i)
        total = sum(arr[i] * (i - left[i]) * (right[i] - i) for i in range(n))
        return total % MOD


##################################################################################################
##### ! Solution 3: 暴力枚举所有子数组（基准答案，用来对拍）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(1)
##### ! 适用：正确性参照，特别是重复元素的 Tie Breaking
##################################################################################################


class Solution_3:
    def sumSubarrayMins(self, arr: List[int]) -> int:
        n = len(arr)
        total = 0
        for i in range(n):
            cur = arr[i]
            for j in range(i, n):
                cur = min(cur, arr[j])
                total += cur
        return total % MOD


if __name__ == "__main__":
    import random

    cases = [[3, 1, 2, 4], [11, 81, 94, 43, 3], [1, 1], [2, 2, 2], [1], [3, 1, 2, 4, 1]]
    for arr in cases:
        a = Solution_1().sumSubarrayMins(arr)
        assert a == Solution_2().sumSubarrayMins(arr) == Solution_3().sumSubarrayMins(arr), arr
        print(f"{arr} -> {a}")

    for _ in range(500):                 # ! 小值域随机对拍，专门压重复元素
        arr = [random.randint(1, 4) for _ in range(random.randint(1, 12))]
        assert (Solution_1().sumSubarrayMins(arr)
                == Solution_2().sumSubarrayMins(arr)
                == Solution_3().sumSubarrayMins(arr)), arr
    print("随机对拍 500 组通过 ✓")
