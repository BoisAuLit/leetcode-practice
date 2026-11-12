"""LC-0673 - Number of Longest Increasing Subsequence

Level 1 · 04 子序列 DP —— **在 LIS 的基础上同时维护「方案数」**
题目在问：最长递增子序列有多少个（不是长度，是**个数**）。

决定性观察（关键在「怎么更新计数」）：
  1. 在 LC-0300 的 O(n²) DP 基础上，**再开一个数组 `cnt`**：
     ```
     dp[i]  = 以 nums[i] 结尾的 LIS 长度
     cnt[i] = 以 nums[i] 结尾、长度为 dp[i] 的 LIS 有几个
     ```
  2. 对每个 `j < i` 且 `nums[j] < nums[i]`：
     ```
     if dp[j] + 1 >  dp[i]:  dp[i] = dp[j] + 1;  cnt[i] = cnt[j]     # 发现更长的 → 计数「重置」
     elif dp[j] + 1 == dp[i]: cnt[i] += cnt[j]                        # 一样长 → 计数「累加」
     ```
     **「重置」和「累加」这两种情况必须分开写** —— 这是本题唯一的难点，
     写成一个 `+=` 就全错了。
  3. 答案 = `sum(cnt[i] for i where dp[i] == max(dp))`。

**初始化**：`dp[i] = 1, cnt[i] = 1`（每个元素自己就是一个长度 1 的 LIS）。

### 和 LC-0300 的关系（同一个 Level 2）

| | LC-0300 | LC-0673 本题 |
|---|---|---|
| 要什么 | LIS 的**长度** | LIS 的**个数** |
| O(n²) DP | 只要 `dp[]` | `dp[]` + `cnt[]` |
| 能否 O(n log n) | **能**（贪心 + 二分，见 LC-0300） | 能，但要**树状数组 / 线段树**维护「长度为 L 的方案数」，复杂度 O(n log n)，实现重得多 |

**面试里 O(n²) 就够**（题目 n ≤ 2000）。知道 O(n log n) 需要什么工具即可，不必背。

### 一个常见错误
用「`dp` 最大值出现了几次」当答案 —— **错**。
`[1,2,4,3,5,4,7,2]` 这种输入里，同一个结尾位置可能对应多条路径，
必须用 `cnt` 累加，而不是数 `dp` 里最大值的个数。

复杂度：**O(n²)** 时间，O(n) 空间。

边界：
  - 全部相同 `[2,2,2]` → 3（每个单独的 2 都是一个长度 1 的 LIS）
  - 严格递增 → 1
  - 严格递减 → n
  - `[1,3,5,4,7]` → 2
  - 单元素 → 1
"""

from typing import List


##################################################################################################
##### ! Solution 1: O(n^2) DP 同时维护 dp[] 和 cnt[]（重置 / 累加分开写）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n)
##### ! 适用：所有「最优值 + 最优方案数」的 DP；关键是分清「更优 ⟹ 重置」和「同优 ⟹ 累加」
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def findNumberOfLIS(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        dp = [1] * n        # ! 以 i 结尾的 LIS 长度
        cnt = [1] * n       # ! 以 i 结尾、长度为 dp[i] 的 LIS 个数
        for i in range(n):
            for j in range(i):
                if nums[j] < nums[i]:
                    if dp[j] + 1 > dp[i]:
                        dp[i] = dp[j] + 1
                        cnt[i] = cnt[j]        # ! 发现更长的 ⟹ 计数**重置**
                    elif dp[j] + 1 == dp[i]:
                        cnt[i] += cnt[j]       # ! 一样长 ⟹ 计数**累加**
        best = max(dp)
        return sum(c for d, c in zip(dp, cnt) if d == best)


##################################################################################################
##### ! Solution 2: 暴力枚举所有递增子序列并统计最长的个数（基准答案，用来对拍）
##### ! 时间复杂度: O(2^n · n)   空间复杂度: O(1)
##### ! 适用：正确性参照 —— 直接按定义数，验证「重置/累加」写对了
##################################################################################################


class Solution_2:
    def findNumberOfLIS(self, nums: List[int]) -> int:
        n = len(nums)
        best, cnt = 0, 0
        for mask in range(1, 1 << n):
            sub = [nums[i] for i in range(n) if mask >> i & 1]
            if all(sub[i] < sub[i + 1] for i in range(len(sub) - 1)):
                if len(sub) > best:
                    best, cnt = len(sub), 1
                elif len(sub) == best:
                    cnt += 1
        return cnt


if __name__ == "__main__":
    import random

    cases = [([1, 3, 5, 4, 7], 2), ([2, 2, 2, 2, 2], 5), ([1, 2, 3], 1),
             ([3, 2, 1], 3), ([1], 1), ([1, 2, 4, 3, 5, 4, 7, 2], 3)]
    for nums, want in cases:
        a = Solution_1().findNumberOfLIS(nums)
        b = Solution_2().findNumberOfLIS(nums)
        assert a == b == want, (nums, a, b, want)
        print(f"{nums} -> {a}")

    for _ in range(1000):                # ! 小值域随机对拍，专压「同样长度的多条路径」
        nums = [random.randint(0, 4) for _ in range(random.randint(1, 10))]
        a = Solution_1().findNumberOfLIS(nums)
        b = Solution_2().findNumberOfLIS(nums)
        assert a == b, (nums, a, b)
    print("随机对拍 1000 组通过 ✓（dp+cnt == 枚举所有递增子序列）")
