"""LC-0287 - Find the Duplicate Number

Level 1 · 04 Array Index Mapping 与 In-place Marking —— 本层唯一**不能改数组**的一题
题目在问：n+1 个数、取值都在 1..n，必有一个重复，找出它。
      要求 **O(1) 额外空间**，而且**不能修改数组**。

两个约束缺一不可地决定了解法：
  - 「值域是 1..n」⇒ 可以把数组看成一个函数 `f(i) = nums[i]`，于是 `0 → nums[0] → nums[nums[0]] → …`
    是一条在**函数图（functional graph）**上的路径。
  - 「有重复值」⇒ 至少两个下标指向同一个值 ⇒ 这条路径**必然成环**，
    而**环的入口就是那个重复的数**。
  - 「不许改数组」⇒ 同层 0041 / 0442 / 0448 的负号标记和原地归位**全部失效**，
    只能用 Floyd 判圈。

为什么从 0 出发安全：`nums[i] ∈ [1, n]`，所以下标 0 永远不会被任何元素指向 ⇒ 0 不在环里，
      它一定是「环外那一段」的起点。这正是 Floyd 找环入口需要的前提。

坑：
  - 快指针是 `nums[nums[fast]]`（走两步），不是 `nums[fast] + 1`
  - 第一次相遇点**不是**答案，必须让一个指针回到起点再同速走一遍
  - Solution_2 的负号标记虽然能过测试，但它**修改了输入**，严格说违反题意 ——
    面试时要先问一句「可以改数组吗」，不能改就只能上 Floyd
"""

from typing import List


##################################################################################################
##### ! Solution 1: Floyd 判圈（把数组当函数图）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)，且**不修改输入**
##### ! 适用：满足题目全部约束的唯一解法；和 LC-0141/0142 是同一套，只是「next 指针」换成了 nums[i]
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def findDuplicate(self, nums: List[int]) -> int:
        slow, fast = 0, 0
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break

        slow2 = 0
        while True:
            slow = nums[slow]
            slow2 = nums[slow2]
            if slow == slow2:
                return slow


##################################################################################################
##### ! Solution 2: 负号标记（原地修改，**不满足本题的「不许改数组」约束**）
##### ! 时间复杂度: O(n)   空间复杂度: O(1) 额外
##### ! 适用：同层 0442 / 0448 的标准手法；放在这里是为了对照「什么时候能用、什么时候不能」
##################################################################################################


class Solution_2:
    def findDuplicate(self, nums: List[int]) -> int:
        for num in nums:
            if nums[abs(num) - 1] < 0:
                return abs(num)
            nums[abs(num) - 1] *= -1


##################################################################################################
##### ! Solution 3: 对答案二分（值域二分 + 计数）
##### ! 时间复杂度: O(n log n)   空间复杂度: O(1)，同样不修改输入
##### ! 适用：想不起 Floyd 时的退路；按「<= mid 的个数是否超过 mid」二分答案
##################################################################################################


class Solution_3:
    def findDuplicate(self, nums: List[int]) -> int:
        lo, hi = 1, len(nums) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            # ! 鸽巢原理：若 <= mid 的数超过 mid 个，重复值必在 [lo, mid]
            if sum(1 for x in nums if x <= mid) > mid:
                hi = mid
            else:
                lo = mid + 1
        return lo


s = Solution_1()

# Expectin 2
input_ = [1, 3, 4, 2, 2]

result = s.findDuplicate(input_)
print(result)

if __name__ == "__main__":
    import random
    cases = [([1, 3, 4, 2, 2], 2), ([3, 1, 3, 4, 2], 3), ([1, 1], 1), ([2, 2, 2, 2, 2], 2)]
    for sol in (Solution_1(), Solution_2(), Solution_3()):
        for nums, want in cases:
            got = sol.findDuplicate(nums[:])      # ! Solution_2 会改数组，所以每次都传副本
            assert got == want, f"{type(sol).__name__} {nums}: got {got}, want {want}"
    rng = random.Random(287)
    for _ in range(3000):
        n = rng.randint(1, 9)
        dup = rng.randint(1, n)
        nums = list(range(1, n + 1)) + [dup]
        rng.shuffle(nums)
        for sol in (Solution_1(), Solution_2(), Solution_3()):
            assert sol.findDuplicate(nums[:]) == dup, (type(sol).__name__, nums, dup)
    print("3 个解法全过（含 3000 组随机对拍）")
