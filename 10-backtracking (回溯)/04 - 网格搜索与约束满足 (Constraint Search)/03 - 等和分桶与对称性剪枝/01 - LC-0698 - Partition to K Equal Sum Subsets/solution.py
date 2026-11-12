"""LC-0698 - Partition to K Equal Sum Subsets

Level 1 · 04 网格搜索与约束满足 —— **分桶回溯 + 四条关键剪枝**
题目在问：能否把数组分成 k 个**和相等**的子集。

这是一道「不剪枝必 TLE、剪枝后很快」的典型题。**全部价值都在剪枝。**

决定性观察：
  1. **先做可行性检查**（O(n)，能挡掉大部分无解情况）：
     - `sum(nums) % k != 0` ⟹ 无解
     - `max(nums) > target` ⟹ 那个数放不进任何桶 ⟹ 无解
     （`target = sum // k`）
  2. **视角选择**：「为每个数字选一个桶」比「为每个桶挑数字」更好写。
     枚举 `nums[i]` 放进哪个桶，桶用一个 `buckets[j]` 数组记当前和。

四条剪枝（缺一个都可能 TLE）：

**① 降序排序**（最重要）
   `nums.sort(reverse=True)` —— 先放大的数。
   大数的选择最少、最容易失败，**让失败尽早发生**，从而尽早回溯。
   这是「失败优先（fail-fast）」的经典体现。

**② 跳过相同容量的桶**
   ```python
   if buckets[j] == buckets[j-1]: continue
   ```
   两个桶当前和相同时，把数字放进 j 和放进 j-1 的**后续搜索完全同构** ——
   第一个失败了，第二个也必然失败。这条剪枝消除了桶之间的**对称性**，
   是复杂度从爆炸降到可行的关键。

**③ 放不下就跳过**
   `if buckets[j] + nums[i] > target: continue`

**④ 第一个数字只放第一个桶**（可选，但有效）
   由对称性，第一个（最大的）数字放哪个桶都等价，固定放 0 号桶。
   也可以写成「如果 `buckets[j] == 0` 且这次失败了，就 break」——
   因为后面所有空桶都等价。

```python
def dfs(i):
    if i == n: return True              # 所有数字都放完了（和一定都等于 target）
    for j in range(k):
        if buckets[j] + nums[i] > target: continue      # ③
        if j > 0 and buckets[j] == buckets[j-1]: continue  # ②
        buckets[j] += nums[i]
        if dfs(i + 1): return True
        buckets[j] -= nums[i]           # 回溯
        if buckets[j] == 0: break       # ④ 空桶等价，后面的空桶不用再试
    return False
```

**为什么 `i == n` 就一定成功**：总和是 `k * target`，每个桶都 ≤ target，
所有数字都放完 ⟹ 每个桶**恰好**等于 target。不需要额外验证。

复杂度：最坏 **O(k^n)**，但有了四条剪枝后实际远低于此。
      **不要声称它是多项式时间** —— 这个问题本身是 NP-complete（等和划分的推广）。
      空间 O(n + k)（递归栈 + 桶数组）。

边界：
  - k == 1 → 恒为 True
  - k == n → 所有元素必须相等
  - k > n → False
  - 含 0（题目保证正整数，但防御性处理不亏）
  - 总和不能被 k 整除

和 LC-0473 Matchsticks to Square 的关系：**473 就是 k = 4 的本题**，
      所以本专题没有单独收录 473。
"""

from typing import List


##################################################################################################
##### ! Solution 1: 分桶回溯 + 四条剪枝（降序 / 跳过同容量桶 / 放不下 / 空桶等价）
##### ! 时间复杂度: 最坏 O(k^n)，剪枝后实际快得多   空间复杂度: O(n + k)
##### ! 适用：所有「把元素分成若干组、组内满足某约束」的搜索；剪枝决定能否通过
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def canPartitionKSubsets(self, nums: List[int], k: int) -> bool:
        total = sum(nums)
        if k <= 0 or total % k != 0:
            return False
        target = total // k
        nums = sorted(nums, reverse=True)        # ! 剪枝①：大的先放，失败尽早发生
        if nums and nums[0] > target:
            return False
        n = len(nums)
        buckets = [0] * k

        def dfs(i: int) -> bool:
            if i == n:
                return True                       # ! 所有数放完 ⟹ 每桶必然恰好 target
            for j in range(k):
                if buckets[j] + nums[i] > target:
                    continue                      # ! 剪枝③：放不下
                if j > 0 and buckets[j] == buckets[j - 1]:
                    continue                      # ! 剪枝②：同容量的桶是对称的，试一个就够
                buckets[j] += nums[i]
                if dfs(i + 1):
                    return True
                buckets[j] -= nums[i]             # ! 回溯
                if buckets[j] == 0:
                    break                         # ! 剪枝④：空桶都等价，后面的不用试
            return False

        return dfs(0)


##################################################################################################
##### ! Solution 2: 状态压缩 DP（位掩码），不依赖剪枝技巧
##### ! 时间复杂度: O(n · 2^n)   空间复杂度: O(2^n)
##### ! 适用：n <= 16 时的稳定解法；复杂度有明确上界，不像回溯那样依赖数据
##################################################################################################


class Solution_2:
    def canPartitionKSubsets(self, nums: List[int], k: int) -> bool:
        total = sum(nums)
        if k <= 0 or total % k != 0:
            return False
        target = total // k
        n = len(nums)
        if n < k or (nums and max(nums) > target):
            return False
        # ! dp[mask] = 用 mask 这些数字时，「当前正在装的那个桶」里已有多少（-1 表示不可达）
        dp = [-1] * (1 << n)
        dp[0] = 0
        for mask in range(1 << n):
            if dp[mask] < 0:
                continue
            for i in range(n):
                if mask >> i & 1:
                    continue
                if dp[mask] + nums[i] > target:
                    continue
                nxt = mask | (1 << i)
                # ! 装满就归零，开下一个桶
                dp[nxt] = max(dp[nxt], (dp[mask] + nums[i]) % target)
        return dp[(1 << n) - 1] == 0


##################################################################################################
##### ! Solution 3: 朴素回溯（无剪枝，基准答案，用来对拍；大输入会很慢）
##### ! 时间复杂度: O(k^n)   空间复杂度: O(n + k)
##### ! 适用：正确性参照 —— 也正好说明四条剪枝带来的差距
##################################################################################################


class Solution_3:
    def canPartitionKSubsets(self, nums: List[int], k: int) -> bool:
        total = sum(nums)
        if k <= 0 or total % k != 0:
            return False
        target = total // k
        n = len(nums)
        buckets = [0] * k

        def dfs(i):
            if i == n:
                return all(b == target for b in buckets)
            for j in range(k):
                if buckets[j] + nums[i] <= target:
                    buckets[j] += nums[i]
                    if dfs(i + 1):
                        return True
                    buckets[j] -= nums[i]
            return False

        return dfs(0)


if __name__ == "__main__":
    import random

    cases = [([4, 3, 2, 3, 5, 2, 1], 4), ([1, 2, 3, 4], 3), ([1, 1, 1, 1], 4),
             ([1, 1, 1, 1], 5), ([2, 2, 2, 2, 3, 4, 5], 4), ([5], 1), ([1, 2], 1)]
    for nums, k in cases:
        a = Solution_1().canPartitionKSubsets(nums[:], k)
        b = Solution_2().canPartitionKSubsets(nums[:], k)
        c = Solution_3().canPartitionKSubsets(nums[:], k)
        assert a == b == c, (nums, k, a, b, c)
        print(f"{nums}, k={k} -> {a}")

    for _ in range(600):                 # ! 随机小输入三方对拍
        n = random.randint(1, 8)
        nums = [random.randint(1, 6) for _ in range(n)]
        k = random.randint(1, 4)
        a = Solution_1().canPartitionKSubsets(nums[:], k)
        b = Solution_2().canPartitionKSubsets(nums[:], k)
        c = Solution_3().canPartitionKSubsets(nums[:], k)
        assert a == b == c, (nums, k, a, b, c)
    print("随机对拍 600 组通过 ✓（剪枝回溯 == 状压 DP == 朴素回溯）")
