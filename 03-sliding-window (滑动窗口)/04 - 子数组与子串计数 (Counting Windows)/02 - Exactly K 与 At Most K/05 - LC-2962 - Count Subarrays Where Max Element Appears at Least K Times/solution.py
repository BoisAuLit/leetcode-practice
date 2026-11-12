"""LC-2962 - Count Subarrays Where Max Element Appears at Least K Times

Level 1 · 04 子数组与子串计数 → Level 2 · 02 Exactly K 与 At Most K

题目在问：数一数有多少子数组里，**整个数组的最大值** `M` 出现 **≥ k** 次。

### 先把题读对：是全局最大值，不是子数组的最大值

`M = max(nums)` 只算一次。于是每个元素只分两类：是 M / 不是 M ⟹ 题目变成 0/1 数组里「1 的个数 ≥ k 的子数组数」。
这是 LC-2537 的「至少 k」模板最简单的实例，也和 LC-1248（恰好 k 个奇数）同源。

### 三种等价计数

| 写法 | 思路 |
|---|---|
| **至少模板** | `while count >= k: res += n − r; 移出左端` |
| 补集 | `total − atMost(k−1)` |
| 记录 M 的位置 | 第 j 个 M 在下标 p；以每个 r 为右端点，若窗口内 M 的个数 c ≥ k，左端点可以是 `0..pos[c−k]`，贡献 `pos[c−k] + 1` |

第三种最直观地说出了「贡献」的来源：**左端点只要不越过「倒数第 k 个 M」就合法**。
"""
from typing import List


##################################################################################################
##### ! Solution 1: 「至少 k」滑动窗口
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：面试标准答案；和 LC-2537 同一模板，只是把「数对数」换成「M 的个数」
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def countSubarrays(self, nums: List[int], k: int) -> int:
        M, n = max(nums), len(nums)
        l = cnt = res = 0
        for r, x in enumerate(nums):
            cnt += x == M
            while cnt >= k:                             # ! [l, r] 已合法 → 右端延长到 n−1 都合法
                res += n - r
                cnt -= nums[l] == M; l += 1
        return res


##################################################################################################
##### ! Solution 2: 记录 M 的位置，每个右端点的贡献 = pos[c − k] + 1
##### ! 时间复杂度: O(n)   空间复杂度: O(M 的出现次数)
##### ! 适用：最直观：以 r 为右端，窗口内有 c 个 M；c >= k 时，左端 l 只需 l <= 倒数第 k 个 M 的位置
##################################################################################################


class Solution_2:
    def countSubarrays(self, nums: List[int], k: int) -> int:
        M = max(nums)
        pos, res = [], 0
        for r, x in enumerate(nums):
            if x == M:
                pos.append(r)
            if len(pos) >= k:
                res += pos[len(pos) - k] + 1            # ! 左端点 0..pos[c−k] 都合法
        return res


##################################################################################################
##### ! Solution 3: total − atMost(k−1)（补集）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：展示两类模板的互补；atMost 用「不合法就收缩、res += r − l + 1」
##################################################################################################


class Solution_3:
    def countSubarrays(self, nums: List[int], k: int) -> int:
        M, n = max(nums), len(nums)
        l = cnt = at_most = 0
        for r, x in enumerate(nums):
            cnt += x == M
            while cnt > k - 1:
                cnt -= nums[l] == M; l += 1
            at_most += r - l + 1
        return n * (n + 1) // 2 - at_most


def _brute(nums, k):
    M, n = max(nums), len(nums)
    return sum(1 for i in range(n) for j in range(i, n) if nums[i:j + 1].count(M) >= k)


if __name__ == "__main__":
    import random
    cases = [([1, 3, 2, 3, 3], 2, 6), ([1, 4, 2, 1], 3, 0), ([5], 1, 1)]
    for nums, k, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().countSubarrays(nums, k)
            assert got == want, (cls.__name__, nums, k, got, want)
    rng = random.Random(2962)
    for _ in range(4000):
        nums = [rng.randint(1, 4) for _ in range(rng.randint(1, 12))]
        k = rng.randint(1, 5)
        want = _brute(nums, k)
        for cls in (Solution_1, Solution_2, Solution_3):
            assert cls().countSubarrays(nums, k) == want, (cls.__name__, nums, k)
    print("所有测试通过 ✓")
