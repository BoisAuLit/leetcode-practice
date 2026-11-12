"""LC-1248 - Count Number of Nice Subarrays

Level 1 · 04 子数组与子串计数 → Level 2 · 02 Exactly K 与 At Most K

题目在问：数一数有多少个子数组**恰好**含 k 个奇数。
它和 LC-0992（恰好 K 个不同整数）、LC-0930（和恰好为 goal 的 0/1 数组）是同一道题：**exactly(k) = atMost(k) − atMost(k−1)**。

### 第一步永远是「把元素映射成 0/1」

    nums[i] 奇数 → 1，偶数 → 0        ⟹  「恰好 k 个奇数」=「0/1 数组里和恰好为 k」= LC-0930

映射完之后本题就是 0930，三种标准解法全部可用：

| 解法 | 思路 | 复杂度 |
|---|---|---|
| **atMost 差分** | `atMost(k)`：右指针扩张、左指针在和 > k 时收缩，每个右端点贡献 `r − l + 1` | O(n) 两遍 |
| 前缀和 + 哈希 | `count[prefix − k]` 累加（LC-0560 的骨架） | O(n) 一遍，O(n) 空间 |
| 三指针（一遍） | 对每个右端点，维护 `[l_min, l_max]` 使窗口恰好 k 个奇数 | O(n) 一遍，O(1) 空间 |

面试里：先写 atMost 差分（最通用，能推广到任何「恰好」计数），再提前缀和版本作为对照。

### 为什么 atMost 里每个右端点贡献 r − l + 1

窗口 `[l, r]` 是满足「和 ≤ k」的最长窗口（l 是最小合法左端）；以 r 为右端点、左端点在 `l..r` 的每个子数组都合法，共 `r − l + 1` 个。
"""
from collections import defaultdict
from typing import List


##################################################################################################
##### ! Solution 1: exactly(k) = atMost(k) − atMost(k − 1)，atMost 用滑动窗口
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：面试标准答案，也是「恰好 K」类计数的通用模板（LC-0992 / LC-0930 同款）
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def numberOfSubarrays(self, nums: List[int], k: int) -> int:
        def at_most(k: int) -> int:
            if k < 0:
                return 0
            l = odd = res = 0
            for r, x in enumerate(nums):
                odd += x & 1
                while odd > k:                         # ! 奇数超了：左指针右移直到合法
                    odd -= nums[l] & 1; l += 1
                res += r - l + 1                       # ! 以 r 结尾、左端在 [l, r] 的全部合法
            return res
        return at_most(k) - at_most(k - 1)


##################################################################################################
##### ! Solution 2: 前缀「奇数个数」+ 哈希计数（LC-0560 骨架）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：一遍扫完；prefix[j] − prefix[i] == k ⟺ 以 j 结尾、从 i+1 开始的子数组恰好 k 个奇数；
#####         count[0] = 1 是空前缀哨兵
##################################################################################################


class Solution_2:
    def numberOfSubarrays(self, nums: List[int], k: int) -> int:
        count = defaultdict(int)
        count[0] = 1                                   # ! 空前缀
        odd = res = 0
        for x in nums:
            odd += x & 1
            res += count[odd - k]                      # ! 前面有多少个前缀使差恰好 k
            count[odd] += 1
        return res


##################################################################################################
##### ! Solution 3: 「数两边的偶数」—— 对每一段恰好 k 个奇数的区间，左右可延伸的偶数个数相乘
##### ! 时间复杂度: O(n)   空间复杂度: O(n)（奇数下标列表）
##### ! 适用：直接按定义数：第 i 到第 i+k-1 个奇数（下标 a..b），左边能延伸 (a − 上一个奇数位置) 个起点，
#####         右边能延伸 (下一个奇数位置 − b) 个终点，乘起来。最直观，也是最好的真值基线
##################################################################################################


class Solution_3:
    def numberOfSubarrays(self, nums: List[int], k: int) -> int:
        odds = [-1] + [i for i, x in enumerate(nums) if x & 1] + [len(nums)]   # ! 两端哨兵
        res = 0
        for i in range(1, len(odds) - k):
            left = odds[i] - odds[i - 1]               # ! 起点可选个数
            right = odds[i + k] - odds[i + k - 1]      # ! 终点可选个数
            res += left * right
        return res


def _brute(nums, k):
    n = len(nums)
    return sum(1 for i in range(n) for j in range(i, n) if sum(x & 1 for x in nums[i:j + 1]) == k)


if __name__ == "__main__":
    import random
    cases = [([1, 1, 2, 1, 1], 3, 2), ([2, 4, 6], 1, 0), ([2, 2, 2, 1, 2, 2, 1, 2, 2, 2], 2, 16), ([1], 1, 1)]
    for nums, k, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().numberOfSubarrays(nums, k)
            assert got == want, (cls.__name__, nums, k, got, want)
    rng = random.Random(1248)
    for _ in range(3000):
        nums = [rng.randint(1, 9) for _ in range(rng.randint(1, 12))]
        k = rng.randint(1, 5)
        want = _brute(nums, k)
        for cls in (Solution_1, Solution_2, Solution_3):
            assert cls().numberOfSubarrays(nums, k) == want, (cls.__name__, nums, k)
    print("所有测试通过 ✓（样例 + 3000 随机对拍）")
