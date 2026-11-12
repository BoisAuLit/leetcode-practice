"""LC-0162 - Find Peak Element

Level 1 · 02 结构性二分 —— Peak Search（峰值查找），**不要求数组全局有序**
题目在问：找任意一个峰值元素（严格大于两侧邻居）的下标；`nums[-1] = nums[n] = -∞`。

【本文件的来历】原 solution.py 是一次自动合并的产物，文件头自己标注了
「⚠️ 自动合并失败 … 需要手工整理」：里面有一段**残缺的驱动代码**
（`input_ = ` 后面没有值、`s.XXXXXXXXXXXXX(input_)` 是占位符），导致整个文件**无法运行**。
本次重构按要求整理：
  - 三段原始实现的**函数体一字未改**，分别保留为 Solution_1 / Solution_2；
  - 原文件里 `03 - ... A - BST.py` 和 `03 - ... B - Linear Scan.py` 两段**内容完全相同**
    （都是线性扫描），所以合并为一个 Solution_2，不再重复；
  - 只删掉了那几行无法运行的占位驱动代码，并补上可运行的测试；
  - 整理前的原文件已原样留档为 `solution.py.orig-broken.txt`。

决定性观察：
  1. **为什么不需要全局有序**：只要比较 `nums[mid]` 和 `nums[mid+1]` 就能决定往哪边走。
  2. **往高处走一定能找到峰**：若 `nums[mid] < nums[mid+1]`（上坡），
     从 mid+1 继续往右，要么一路升到数组末尾（末尾右边是 -∞，所以末元素就是峰），
     要么中途开始下降（下降的那个点就是峰）。两种情况右半都**保证有峰**，
     所以丢掉左半是安全的。下坡时对称。
  3. 题目保证相邻元素不相等，所以不存在「平台」的歧义。

Loop Invariant：`[lo, hi]` 区间内**保证至少有一个峰**。
      这是本题和普通二分最大的不同 —— 不变量说的不是「target 在区间内」，
      而是「区间内一定存在一个解」。

Pop / 边界更新：
      - `nums[mid] < nums[mid+1]` （上坡）→ `lo = mid + 1`（峰在右边，mid 自己不是峰）
      - 否则（下坡）→ `hi = mid`（峰在左边或就是 mid，**不能丢 mid**）
      收敛时 `lo == hi` 就是一个峰。

为什么用 `mid+1` 而不是 `mid-1`：
      `mid = (lo + hi) // 2` 向下取整，当 `lo < hi` 时必有 `mid + 1 <= hi`，**不会越界**。
      写成和 `nums[mid-1]` 比较则 mid=0 时越界，要额外判断。

复杂度：O(log n) 时间，O(1) 空间。

边界：
  - [1,2,3,1] → 2
  - [1,2,1,3,5,6,4] → 1 或 5（任意一个峰都算对）
  - 严格递增 [1,2,3] → 2（最后一个）
  - 严格递减 [3,2,1] → 0（第一个）
  - 单元素 [1] → 0
"""

from typing import List


##################################################################################################
##### ! Solution 1: 二分 —— 比较 nums[mid] 与 nums[mid+1]，朝更高的一侧走（用户原有实现）
##### ! 时间复杂度: O(log n)   空间复杂度: O(1)
##### ! 适用：找局部最大 / 局部最小；不需要全局有序，只需要「边界外是 -∞」这个约定
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def findPeakElement(self, nums: List[int]) -> int:
        left =0
        right = len(nums)-1
        while left < right:
            mid = left + (right - left ) //2
            if nums[mid] > nums[mid+1]: # True Condition # Dec function # go left # Find First True i.e first elem where this condition will be True
                right = mid # include mid # mid is potential solution 
            else:
                left = mid +1
        return left


##################################################################################################
##### ! Solution 2: 线性扫描 —— 找第一个开始下降的位置（用户原有实现，两份原文件内容相同）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：正确性参照；也最能说明「峰一定存在」这件事 —— 一路不降就到末尾
##################################################################################################


class Solution_2:
    def findPeakElement(self, nums):
        for i in range(len(nums) - 1):
            if nums[i] > nums[i + 1]:
                return i
        return len(nums) - 1


if __name__ == "__main__":
    import random

    def is_peak(nums, i):
        left = nums[i - 1] if i - 1 >= 0 else float("-inf")
        right = nums[i + 1] if i + 1 < len(nums) else float("-inf")
        return left < nums[i] > right

    cases = [[1, 2, 3, 1], [1, 2, 1, 3, 5, 6, 4], [1, 2, 3], [3, 2, 1], [1]]
    for nums in cases:
        a = Solution_1().findPeakElement(nums)
        b = Solution_2().findPeakElement(nums)
        assert is_peak(nums, a) and is_peak(nums, b), (nums, a, b)
        print(f"{nums} -> Solution_1={a}  Solution_2={b}  (都是合法的峰)")

    for _ in range(1000):                # ! 随机对拍：生成相邻不相等的数组，验证返回的确实是峰
        n = random.randint(1, 12)
        nums = [random.randint(0, 20)]
        while len(nums) < n:
            v = random.randint(0, 20)
            if v != nums[-1]:
                nums.append(v)
        a = Solution_1().findPeakElement(nums)
        b = Solution_2().findPeakElement(nums)
        assert is_peak(nums, a), (nums, a)
        assert is_peak(nums, b), (nums, b)
    print("随机对拍 1000 组通过 ✓（两个解法返回的都是合法峰值）")
