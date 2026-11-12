"""LC-0041 - First Missing Positive

Level 1 · 04 Array Index Mapping 与 In-place Marking —— Cyclic Placement（原地归位）
题目在问：未排序数组里，没出现的最小**正整数**是多少。要求 O(n) 时间、O(1) 额外空间

核心观察：长度为 n 的数组，答案一定落在 `1 .. n+1` 这个范围里 ——
      最好的情况是 1..n 全都在，答案 n+1；只要缺了一个，答案就 <= n。
      所以 n 以外的数（负数、0、大于 n 的数）全是噪声，可以无视。
      于是 n 个格子正好装 1..n：**把数字 v 放到下标 v-1 上**，数组本身就成了哈希表。

不变量：每一轮 while 结束后，`nums[i]` 要么是噪声，要么已经待在它该待的位置 `nums[i]-1` 上。
      每次 swap 至少让一个数字归位，所以总交换次数 <= n，整体仍是 O(n)。

什么时候可以改输入、什么时候不能（和 287 对照着记）：
  - 41 / 448 / 442：题目没说输入只读，**可以改**，所以能用原地归位和负号标记做到 O(1) 空间
  - 287：题目明确要求**不能修改数组**，所以不能用标记，要用 Floyd 判圈（见本层 04 号题）

坑：
  - 内层必须是 while 不是 if：换过来的新数字可能也需要继续归位
  - 循环条件要写 `nums[nums[i] - 1] != nums[i]`（比较值），不要写 `i != nums[i] - 1`（比较下标）：
    有重复数字时后者会死循环
  - 负号标记法必须先把所有 <= 0 和 > n 的数清洗成 n+1，否则负号会和原本的负数混在一起
"""

from typing import List


##################################################################################################
##### ! Solution 1: Cyclic Placement —— 把 v 换到下标 v-1 上
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：值域恰好是 1..n 的所有题（41 / 442 / 448 / 268 / 645）；归位后一次扫描就出答案
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)
        for i in range(n):
            # ! while 不是 if：换上来的数可能也要继续归位；比较的是「值」不是「下标」，防重复死循环
            while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
                j = nums[i] - 1
                nums[i], nums[j] = nums[j], nums[i]
        for i in range(n):
            if nums[i] != i + 1:  # ! 第一个「位置和值对不上」的格子，缺的就是它
                return i + 1
        return n + 1  # ! 1..n 全都在


##################################################################################################
##### ! Solution 2: 负号标记（Negative Marking）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：和 448 / 442 完全同一套；先清洗噪声，再用正负号当作「这个数出现过」的一位标记
##################################################################################################


class Solution_2:
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)
        for i in range(n):
            if nums[i] <= 0 or nums[i] > n:
                nums[i] = n + 1  # ! 清洗：噪声统一换成一个不会被标记的值
        for i in range(n):
            v = abs(nums[i])
            if v <= n and nums[v - 1] > 0:
                nums[v - 1] = -nums[v - 1]  # ! 用负号记录「v 出现过」
        for i in range(n):
            if nums[i] > 0:  # ! 还是正的 → i+1 没出现过
                return i + 1
        return n + 1


##################################################################################################
##### ! Solution 3: Hash Set（基线，不满足 O(1) 空间）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：面试第一句先说它建立共识，再说「题目要 O(1) 空间，所以要把数组自己当哈希表用」
##################################################################################################


class Solution_3:
    def firstMissingPositive(self, nums: List[int]) -> int:
        s = set(nums)
        i = 1
        while i in s:
            i += 1
        return i


if __name__ == "__main__":
    import random
    cases = [([1, 2, 0], 3), ([3, 4, -1, 1], 2), ([7, 8, 9, 11, 12], 1),
             ([1], 2), ([2, 2, 2], 1), ([1, 1], 2), ([], 1)]
    sols = [Solution_1(), Solution_2(), Solution_3()]
    for sol in sols:
        for nums, want in cases:
            got = sol.firstMissingPositive(nums[:])
            assert got == want, f"{type(sol).__name__} {nums}: got {got}, want {want}"
    rng = random.Random(41)
    for _ in range(3000):  # ! 随机对拍，重点覆盖重复值和越界值
        nums = [rng.randint(-3, 8) for _ in range(rng.randint(0, 8))]
        want = Solution_3().firstMissingPositive(nums[:])
        for sol in sols:
            assert sol.firstMissingPositive(nums[:]) == want, (type(sol).__name__, nums)
    print("3 个解法全过（含 3000 组随机对拍）")
