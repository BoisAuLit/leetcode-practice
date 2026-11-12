"""LC-0494 - Target Sum（第二轮自主新增）

Level 1 · 05 回溯与记忆化的边界 —— **什么时候该停止回溯、改用 DP**
题目在问：给每个数字前面加 `+` 或 `-`，求有多少种加法使结果等于 target。

为什么单独开一个 Level 1 放它（这是本专题最该想清楚的一件事）：
  前四章的题（子集、排列、分割、N 皇后）都**必须**枚举出每一个方案，
  所以回溯是唯一选择 —— 答案本身就有指数级那么多。

  但本题**只要数量，不要方案**。一旦「只要计数」，
  不同的搜索分支就可能**汇合到同一个状态**，于是可以记忆化、可以 DP。
  **这是回溯和 DP 的分水岭**：

> **要列出所有方案 ⟹ 只能回溯（答案规模就是指数级）。
> 只要数量 / 最优值 ⟹ 先找「状态」，能合并就上记忆化或 DP。**

本题的三级演进（solution.py 里三种解法正是这三级）：

### ① 朴素回溯 —— O(2^n)
```python
def dfs(i, cur):
    if i == n: return 1 if cur == target else 0
    return dfs(i+1, cur + nums[i]) + dfs(i+1, cur - nums[i])
```
n = 20 时 2²⁰ ≈ 10⁶ 勉强能过，但这是上限。

### ② 记忆化 —— O(n · S)
**关键观察**：走到第 i 个数字时，**无论前面怎么选**，
只要「当前累计和 cur」相同，后面的结果就完全一样。
⟹ 状态是 `(i, cur)`，可以缓存。
S 是可能的和的个数，`sum(nums) <= 1000` 所以 S 最多 2001 个。

**找到这个状态，是整道题唯一的思考步骤。**

### ③ 转成子集和 DP —— O(n · sum)
设选 `+` 的那些数之和为 P，选 `-` 的为 N：
```
P + N = sum
P - N = target
⟹ P = (sum + target) / 2
```
于是问题变成：**有多少个子集的和等于 `(sum+target)/2`** ⟹ 经典 0-1 背包计数。

**两个无解判定**（必须先做）：
  - `(sum + target)` 是**奇数** ⟹ 无解（P 必须是整数）
  - `abs(target) > sum` ⟹ 无解

```python
P = (sum(nums) + target) // 2
dp = [0] * (P + 1); dp[0] = 1
for x in nums:
    for j in range(P, x - 1, -1):      # 倒序 ⟹ 0-1 背包（每个数只用一次）
        dp[j] += dp[j - x]
return dp[P]
```
**倒序遍历**是 0-1 背包的标志；正序就变成完全背包（每个数可以用多次），答案会错。

**注意 nums 里可能有 0**：`[0,0,0,0,0,0,0,0,1]`, target=1 的答案是 512
（每个 0 都可以 `+` 或 `-`）。上面的 DP 自动处理了这一点 ——
`dp[j] += dp[j-0]` 会让计数翻倍。这是本题最经典的边界用例。

## 复杂度对照

| 解法 | 时间 | 空间 | 什么时候用 |
|---|---|---|---|
| ① 回溯 | O(2^n) | O(n) | n 很小；或者**需要列出所有方案** |
| ② 记忆化 | O(n · S) | O(n · S) | 想从回溯平滑过渡，改动最小 |
| ③ 01 背包 DP | **O(n · sum)** | O(sum) | 最优；但需要先想出那个数学转化 |

边界：
  - `abs(target) > sum(nums)` → 0
  - `(sum + target)` 为奇数 → 0
  - 含 0（`[0,0,0,0,0,0,0,0,1]`, target=1 → 512）
  - 单个元素
  - target 为负
"""

from functools import lru_cache
from typing import List

# ! ============================================================================================
# ! 下面这段是**用户原有的实现**，一字未改。
# ! 后面追加的 Solution_1 / Solution_2 / Solution_3 是本次补充的三级演进
# !（01 背包 → 记忆化 → 朴素回溯）与随机对拍。
# ! ============================================================================================

from typing import List

# Approach:Recursion with memoization
"""
Don't set cache direction under Solution, it won't work for different python interpreters


Time complexity: O(N * S)
S is the total sum(nums)

Space complexity: O(N* S)
"""


class Solution:
    def dfs(self, index: int, nums: List[int], target: int, cache) -> int:
        key = (index, target)
        if key in cache:
            return cache[key]
        if index == len(nums) - 1:
            if abs(nums[-1]) != abs(target):
                return 0
            if nums[-1] == 0:
                return 2
            return 1
        result = self.dfs(
            index + 1, nums, target - nums[index], cache
        ) + self.dfs(index + 1, nums, target + nums[index], cache)
        cache[key] = result
        return result

    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        return self.dfs(0, nums, target, dict())



s = Solution()

# Test case 1: Expecting 5
nums = [1, 1, 1, 1, 1]
target = 3

# Test case 2: Expecting 2
# nums = [1, 1]
# target = 0

# Test case 3: Expecting 256
# nums = [0, 0, 0, 0, 0, 0, 0, 0, 1]
# target = 1


# Test case 4: Expecting 2
# nums = [1, 0]
# target = 1

result = s.findTargetSumWays(nums, target)
print(result)


##################################################################################################
##### ! Solution 1: 转成子集和 01 背包计数（最优）
##### ! 时间复杂度: O(n · sum)   空间复杂度: O(sum)
##### ! 适用：只要「方案数」而不要「方案本身」时的终点形态；倒序遍历 = 0-1 背包
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        total = sum(nums)
        if abs(target) > total or (total + target) % 2 != 0:
            return 0                       # ! 两个无解判定，必须先做
        P = (total + target) // 2          # ! 选 + 的那些数之和
        dp = [0] * (P + 1)
        dp[0] = 1                          # ! 空集的和是 0，算一种方案
        for x in nums:
            for j in range(P, x - 1, -1):  # ! 倒序 ⟹ 每个数最多用一次（0-1 背包）
                dp[j] += dp[j - x]
        return dp[P]


##################################################################################################
##### ! Solution 2: 记忆化搜索 —— 状态 (下标, 当前累计和)
##### ! 时间复杂度: O(n · S)   空间复杂度: O(n · S)
##### ! 适用：从朴素回溯过渡过来，改动最小；也最能看清「为什么能合并分支」
##################################################################################################


class Solution_2:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        n = len(nums)

        @lru_cache(maxsize=None)
        def dfs(i: int, cur: int) -> int:
            # ! 关键：走到第 i 个数时，前面怎么选过无所谓，只有 cur 影响后续结果
            if i == n:
                return 1 if cur == target else 0
            return dfs(i + 1, cur + nums[i]) + dfs(i + 1, cur - nums[i])

        res = dfs(0, 0)
        dfs.cache_clear()
        return res


##################################################################################################
##### ! Solution 3: 朴素回溯（基准答案，用来对拍；也是这三级演进的起点）
##### ! 时间复杂度: O(2^n)   空间复杂度: O(n)
##### ! 适用：正确性参照。如果题目改成「列出所有符号方案」，就只能用它
##################################################################################################


class Solution_3:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        n = len(nums)

        def dfs(i: int, cur: int) -> int:
            if i == n:
                return 1 if cur == target else 0
            return dfs(i + 1, cur + nums[i]) + dfs(i + 1, cur - nums[i])

        return dfs(0, 0)


if __name__ == "__main__":
    import random

    cases = [([1, 1, 1, 1, 1], 3), ([1], 1), ([1], 2),
             ([0, 0, 0, 0, 0, 0, 0, 0, 1], 1), ([1, 2, 3], -2), ([100], -100)]
    for nums, t in cases:
        a = Solution_1().findTargetSumWays(nums, t)
        b = Solution_2().findTargetSumWays(nums, t)
        c = Solution_3().findTargetSumWays(nums, t)
        assert a == b == c, (nums, t, a, b, c)
        print(f"{nums}, target={t} -> {a}")

    for _ in range(1000):                # ! 随机对拍（含 0 和负 target）
        nums = [random.randint(0, 5) for _ in range(random.randint(1, 10))]
        t = random.randint(-10, 10)
        a = Solution_1().findTargetSumWays(nums, t)
        b = Solution_2().findTargetSumWays(nums, t)
        c = Solution_3().findTargetSumWays(nums, t)
        assert a == b == c, (nums, t, a, b, c)
    print("随机对拍 1000 组通过 ✓（01 背包 == 记忆化 == 朴素回溯）")
