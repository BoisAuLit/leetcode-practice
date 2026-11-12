"""LC-0045 - Jump Game II

Level 1 · 01 跳跃、可达性与区间覆盖 —— **把跳跃看成「一层一层的区间覆盖」**
题目在问：每个位置能往前跳 `nums[i]` 步以内，求跳到最后一个下标的最少跳数（保证可达）。

决定性观察（这题的灵魂）：
  1. **这其实是一次 BFS 的分层**，只是不用队列：
     「跳 1 次能到的区间」→「跳 2 次能到的区间」→ …
     每一层是一段**连续的下标区间**，因为能跳 k 步就能跳 1..k 步。
  2. 扫描时维护两个边界：
        `curr_end` = 当前这一层（跳 jumps 次）能覆盖到的最右下标
        `curr_far` = 如果再跳一次，目前发现最远能到哪里
     `curr_far = max(curr_far, i + nums[i])`。
  3. **走到 `i == curr_end` 时，就必须再跳一次**（这一层走完了）
     ⟹ `jumps += 1; curr_end = curr_far`。
  4. **循环只到 `n - 2`**：站在最后一个下标上不需要再跳了。
     这是本题最容易多算一次的地方。

```python
jumps = curr_end = curr_far = 0
for i in range(len(nums) - 1):          # ★ 到 n-2 为止
    curr_far = max(curr_far, i + nums[i])
    if i == curr_end:
        jumps += 1
        curr_end = curr_far
return jumps
```

和 LC-0055 Jump Game 的关系：
      0055 只问「能不能到」⟹ 只需要维护一个 `max_reach`，一旦 `i > max_reach` 就 False。
      0045 问「最少几跳」⟹ 需要**分层**，多维护一个 `curr_end`。
      **两题是同一个「最远可达」思想的两个问题。**

复杂度：**O(n) 时间、O(1) 空间**。
      DP / 记忆化版本是 O(n²)（见 Solution_3 / Solution_4），n = 10⁴ 时也能过，
      但面试应该给出 O(n) 的贪心。

### 本文件修掉的两个 bug（都是原有代码里的）

**① 原 `Solution_0` 的 `farthest` 算错，会死循环**：
```python
farthest = max(farthest, nums[i])        # ✗ 少加了 i
farthest = max(farthest, i + nums[i])    # ✓
```
`nums[i]` 是「能跳多远」，`i + nums[i]` 才是「能跳到哪个下标」。
写错之后 `r` 不保证前进，`[2,3,0,1,4]` 就会无限循环（实测卡死）。

**② Cluster 版 `Solution_1` 的初始化写错**：
```python
curr_end, curr_far = 0        # ✗ ValueError: cannot unpack non-sequence int
curr_end = curr_far = 0       # ✓
```

边界：
  - 单元素 `[0]` → 0（已经在终点）
  - `[2,3,1,1,4]` → 2
  - `[2,3,0,1,4]` → 2
  - 全是 1 → n-1
  - 第一步就能直达 → 1
"""

from functools import lru_cache
from typing import List


##################################################################################################
##### ! Solution 1: 区间分层贪心（Cluster 版的实现，已修掉初始化 bug）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：最少跳数 / 最少区间覆盖；把「能跳多远」看成一层一层的区间
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def jump(self, nums: List[int]) -> int:
        jumps = 0                 # 已经跳了几次
        curr_end = curr_far = 0   # ! 修正：原来写的是 `curr_end, curr_far = 0`（解包报错）
        # curr_end: 当前 jumps 次能够覆盖到的最右边界
        # curr_far: 如果再跳一次，目前发现最远能够到哪里
        for i in range(len(nums) - 1):      # ! 只到 n-2：站在终点就不用再跳了
            curr_far = max(curr_far, i + nums[i])
            if i == curr_end:               # ! 这一层走完了，必须再跳一次
                jumps += 1
                curr_end = curr_far
        return jumps


##################################################################################################
##### ! Solution 2: 显式双指针写法（原文件的实现，已修掉 farthest 的死循环 bug）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：和 Solution_1 等价，只是把「层」显式写成 [l, r] 两个指针，更直观
##################################################################################################


class Solution_2:
    def jump(self, nums: List[int]) -> int:
        res = 0
        l = r = 0
        while r < len(nums) - 1:
            farthest = 0
            for i in range(l, r + 1):
                # ! 修正：原来写的是 max(farthest, nums[i])，少加了 i ⟹ r 不保证前进 ⟹ 死循环
                farthest = max(farthest, i + nums[i])
            l = r + 1
            r = farthest
            res += 1
        return res


##################################################################################################
##### ! Solution 3: 记忆化搜索（Cluster 版的实现，原样保留）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n)
##### ! 适用：先想到这版再优化成贪心很自然；n = 10^4 时也能过
##################################################################################################


class Solution_3:
    def jump(self, nums: List[int]) -> int:
        n = len(nums)

        @lru_cache(maxsize=None)
        def dfs(i):
            if i >= n - 1:
                return 0
            if nums[i] == 0:
                return float("inf")
            return 1 + min(dfs(i + j) for j in range(1, nums[i] + 1) if i + j <= n - 1)

        r = dfs(0)
        dfs.cache_clear()
        return int(r)


##################################################################################################
##### ! Solution 4: 自底向上 DP（Cluster 版的实现，原样保留）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n)
##### ! 适用：和 Solution_3 等价的迭代版，不用担心递归深度
##################################################################################################


class Solution_4:
    def jump(self, nums: List[int]) -> int:
        n = len(nums)
        dp = [float("inf")] * n
        dp[-1] = 0
        for i in range(n - 2, -1, -1):
            if nums[i] == 0:
                continue
            dp[i] = 1 + min(dp[i + j] for j in range(1, nums[i] + 1) if i + j <= n - 1)
        return int(dp[0])


if __name__ == "__main__":
    import random

    cases = [([2, 3, 1, 1, 4], 2), ([2, 3, 0, 1, 4], 2), ([0], 0), ([1, 1, 1, 1], 3),
             ([10, 1, 1], 1), ([1, 2, 3], 2)]
    sols = [Solution_1(), Solution_2(), Solution_3(), Solution_4()]
    for nums, want in cases:
        outs = [s.jump(nums[:]) for s in sols]
        assert all(o == want for o in outs), (nums, outs, want)
        print(f"{nums} -> {outs[0]}")

    for _ in range(600):                 # ! 随机对拍（保证可达：每个位置至少能跳 1 步）
        n = random.randint(1, 10)
        nums = [random.randint(1, 4) for _ in range(n)]
        outs = [s.jump(nums[:]) for s in sols]
        assert len(set(outs)) == 1, (nums, outs)
    print("随机对拍 600 组通过 ✓（区间分层 == 双指针 == 记忆化 == DP）")
