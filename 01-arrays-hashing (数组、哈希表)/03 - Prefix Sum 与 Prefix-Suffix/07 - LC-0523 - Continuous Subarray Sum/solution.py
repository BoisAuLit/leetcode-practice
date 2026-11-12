"""LC-0523 - Continuous Subarray Sum

Level 1 · 03 Prefix Sum 与 Prefix-Suffix

题目在问：是否存在**长度 ≥ 2** 的子数组，其和是 k 的倍数。
它是 LC-0560（和等于 k）和 LC-0974（和被 k 整除、数个数）之间的一环，三题共用「前缀和 + 哈希」。

### 决定性观察：和是 k 的倍数 ⟺ 两个前缀和模 k 同余

    sum(i+1..j) = P[j] − P[i]  是 k 的倍数   ⟺   P[j] ≡ P[i]  (mod k)

所以只需要记住**每个余数第一次出现的位置**；再遇到同余的 j 时检查 `j − i ≥ 2`。
为什么记「第一次」？因为同一个余数下，最早的 i 给出最长的子数组，长度 ≥ 2 的条件最容易满足；后面再出现不必更新。

### 哨兵：`{0: -1}`

前缀和 P[-1] = 0（空前缀），余数 0 出现在位置 −1。这样「从头开始的子数组」也被统一处理：
`nums = [6, 1], k = 6`：P[0] = 6 ≡ 0，位置 0 − (−1) = 1 < 2 不算；`nums = [6, 6]`：P[1] = 12 ≡ 0，1 − (−1) = 2 ✓。

### 边角

- Python 的 `%` 对负数返回非负余数，所以本题（nums 非负）和 LC-0974（有负数）都不用额外处理；Java/C++ 要 `((x % k) + k) % k`。
- 题目保证 k ≥ 1（旧版允许 k = 0，那时「和为 0 的长度 ≥ 2 子数组」要单独处理 —— `Solution_3` 保留了这个兼容分支作为知识点）。
"""
from typing import List


##################################################################################################
##### ! Solution 1: 前缀和模 k + 哈希表记「余数首次出现位置」
##### ! 时间复杂度: O(n)   空间复杂度: O(min(n, k))
##### ! 适用：面试标准答案；哨兵 {0: -1}，只记首次位置，长度检查 j - i >= 2
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def checkSubarraySum(self, nums: List[int], k: int) -> bool:
        first = {0: -1}                                # ! 余数 → 首次出现的下标；空前缀余数 0 在 -1
        r = 0
        for j, x in enumerate(nums):
            r = (r + x) % k
            if r in first:
                if j - first[r] >= 2:                  # ! 长度 ≥ 2
                    return True
            else:
                first[r] = j                           # ! 只记第一次：越早越好
        return False


##################################################################################################
##### ! Solution 2: 「上一步的余数集合」技巧 —— 不存位置，错开一位保证长度 ≥ 2
##### ! 时间复杂度: O(n)   空间复杂度: O(min(n, k))
##### ! 适用：另一种保证长度 ≥ 2 的方法：维护一个集合 seen，里面只放「至少两步之前」的余数
#####         （用变量 prev 延迟一拍再放进去），于是任何命中天然长度 ≥ 2。少一个比较，但更难讲清楚
##################################################################################################


class Solution_2:
    def checkSubarraySum(self, nums: List[int], k: int) -> bool:
        seen = set()
        r = prev = 0                                   # ! prev = 上一个前缀和的余数（延迟一拍）
        for x in nums:
            r = (r + x) % k
            if r in seen:
                return True
            seen.add(prev)                             # ! 把「两步前」的余数放进去
            prev = r
        return False


##################################################################################################
##### ! Solution 3: 暴力 O(n²) 枚举（真值基线，兼容 k == 0 的旧题面）
##### ! 时间复杂度: O(n²)   空间复杂度: O(1)
##### ! 适用：只用来对拍。k == 0 时「倍数」定义为和 == 0
##################################################################################################


class Solution_3:
    def checkSubarraySum(self, nums: List[int], k: int) -> bool:
        n = len(nums)
        for i in range(n):
            s = nums[i]
            for j in range(i + 1, n):
                s += nums[j]
                if (k == 0 and s == 0) or (k and s % k == 0):
                    return True
        return False


if __name__ == "__main__":
    import random
    cases = [([23, 2, 4, 6, 7], 6, True), ([23, 2, 6, 4, 7], 6, True), ([23, 2, 6, 4, 7], 13, False),
             ([6, 1], 6, False), ([6, 6], 6, True), ([0, 0], 1, True), ([5], 5, False), ([1, 2, 3], 6, True), ([1, 0], 2, False)]
    for nums, k, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().checkSubarraySum(nums, k)
            assert got == want, (cls.__name__, nums, k, got, want)
    rng = random.Random(523)
    for _ in range(5000):
        nums = [rng.randint(0, 12) for _ in range(rng.randint(1, 10))]
        k = rng.randint(1, 10)
        outs = [cls().checkSubarraySum(nums, k) for cls in (Solution_1, Solution_2, Solution_3)]
        assert outs[0] == outs[1] == outs[2], (nums, k, outs)
    print("所有测试通过 ✓（样例 + 5000 随机对拍）")
