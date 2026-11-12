"""LC-0611 - Valid Triangle Number

合并自 2 个解法文件:
  1. 04 - 0611 - A - Valid Triangle Number - Binary Seaarch 🐢.py
  2. 04 - 0611 - B - Valid Triangle Number - Linear Scan 🚀.py

Level 1 · 01 对撞指针与贪心 / 02 有序计数与双端构造 —— 一次比较批量计数
题目在问：数组里有多少个三元组能构成三角形

决定性观察：排序之后，三条边 `a <= b <= c` 只需要验证 **`a + b > c`** 一个不等式
      （另外两个 `a + c > b`、`b + c > a` 因为 c 最大而自动成立）。
      这一步把「三个约束」压成「一个约束」，是整道题的起点。

批量计数（本目录要练的东西）：**固定最大边 `nums[k]`，剩下两条边用对撞指针。**
      若 `nums[i] + nums[j] > nums[k]`，那么把左边换成任意 `i' ∈ [i, j-1]` 都有
      `nums[i'] >= nums[i]`，和同样 > `nums[k]` ⇒ **一次加 `j - i` 个**，然后 `j -= 1`。
      否则 `i += 1`。每个 k 内部 O(n)，总共 O(n²)。

和 LC-0259 - 3Sum Smaller 是同一个手法：满足条件时一次加一整段，而不是逐个枚举。
这也是双指针用于**计数**（而不是找一组解）时的统一套路。

坑：
  - 排序不能忘；`nums[i] == 0` 时不可能构成三角形，要跳过
  - 计数是 `j - i` 不是 `j - i + 1`（j 自己已经被当成第二条边用掉了）
  - 固定最大边要从后往前枚举 `k`，固定最小边的写法也能做但推进逻辑更绕
"""

from typing import List


##################################################################################################
##### ! Solution 1: 固定 i、j，二分找第一个 >= nums[i]+nums[j] 的位置
##### ! 时间复杂度: O(n^2 log n)   空间复杂度: O(1) 额外
##### ! 适用：原解法（04 - 0611 - A - ... - Binary Seaarch 🐢.py）；思路直接，但多一个 log
##################################################################################################


class Solution_1:
    def triangleNumber(self, nums: List[int]) -> int:
        n = len(nums)
        def binary_search(l: int, r: int, x: int) -> int:
            # Find the first index >= x in the range [l, r]
            while r >= l and r < n:
                mid = (l + r) // 2
                if nums[mid] >= x:
                    r = mid - 1
                else:
                    l = mid + 1
            return l

        nums.sort()
        res = 0

        for i in range(n - 2):
            k = i + 2
            for j in range(i + 1, n - 1):
                if nums[i] == 0:
                    break
                k = binary_search(k, n - 1, nums[i] + nums[j])
                res += k - j - 1

        return res


##################################################################################################
##### ! Solution 2: 固定最小边 i，k 单调不回退地往前推
##### ! 时间复杂度: O(n^2)   空间复杂度: O(1) 额外
##### ! 适用：原解法（04 - 0611 - B - ... - Linear Scan 🚀.py）；把二分换成「k 不回退」的摊还
##################################################################################################


class Solution_2:
    def triangleNumber(self, nums: List[int]) -> int:
        nums.sort()
        n = len(nums)
        count = 0

        for i in range(n - 2):
            if nums[i] == 0:
                continue   # 0 不能作为三角形最小边

            k = i + 2
            for j in range(i + 1, n - 1):
                # 线性推进 k，不回退
                while k < n and nums[i] + nums[j] > nums[k]:
                    k += 1

                # [j+1, k-1] 都可以作为第三条边
                count += k - j - 1

        return count


##################################################################################################
##### ! Solution 3: 固定最大边 k + 对撞指针，命中一次加一整段
##### ! 时间复杂度: O(n^2)   空间复杂度: O(1) 额外
##### ! 适用：本目录的标准答案；和 LC-0259 共用「满足条件就一次加 j - i」的批量计数手法
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_3:
    def triangleNumber(self, nums: List[int]) -> int:
        nums.sort()
        cnt = 0
        for k in range(len(nums) - 1, 1, -1):      # ! 固定最大边，从后往前
            i, j = 0, k - 1
            while i < j:
                if nums[i] + nums[j] > nums[k]:
                    cnt += j - i                   # ! i..j-1 配 j 全都成立，一次加完
                    j -= 1
                else:
                    i += 1                         # ! 最小的都不够大，它配谁都不行
        return cnt


if __name__ == "__main__":
    import random
    from itertools import combinations
    cases = [([2, 2, 3, 4], 3), ([4, 2, 3, 4], 4), ([0, 0, 0], 0), ([1], 0),
             ([1, 1, 1, 1], 4), ([0, 1, 1], 0)]   # [0,1,1]: 0+1 > 1 不成立，所以是 0
    sols = [Solution_1(), Solution_2(), Solution_3()]
    for sol in sols:
        for nums, want in cases:
            got = sol.triangleNumber(nums[:])
            assert got == want, f"{type(sol).__name__} {nums}: got {got}, want {want}"

    def brute(nums):   # ! 枚举所有三元组
        return sum(1 for a, b, c in combinations(sorted(nums), 3) if a + b > c)

    rng = random.Random(611)
    for _ in range(3000):
        nums = [rng.randint(0, 8) for _ in range(rng.randint(0, 9))]
        want = brute(nums)
        for sol in sols:
            assert sol.triangleNumber(nums[:]) == want, (type(sol).__name__, nums, want)
    print("3 个解法全过（含 3000 组随机对拍 vs 穷举三元组）")
