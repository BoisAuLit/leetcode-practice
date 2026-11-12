"""LC-0632 - Smallest Range Covering Elements from K Lists（第二轮自主新增）

Level 1 · 02 K-way Merge 与候选扩展 —— **k 路指针 + 堆维护「当前最小」，同时跟踪最大**
题目在问：k 个**升序**列表，找一个最小区间 `[a, b]`，使**每个列表至少有一个数**落在里面。
         区间更小的优先；长度相同时取 a 更小的。

为什么新增它（它补的是哪个缺口）：
  LC-0378 / LC-0373 的 k-way merge 都是「**弹出第 t 小**」，一次只关心堆顶。
  本题要同时盯住 **当前 k 个候选里的最小值（堆顶）和最大值（单独维护）**，
  并把 `[min, max]` 当作一个候选答案。
  **「堆给最小值，变量给最大值」** 这个组合在很多「覆盖 / 配平」题里都会出现，
  本专题原本没有练到。

决定性观察：
  1. **任何合法区间，都可以缩小到「每个列表恰好取一个数」的情形**。
     所以只需要考虑「从每个列表各取一个数」构成的 k 元组，
     区间就是 `[min(元组), max(元组)]`。
  2. 用 k 个指针，初始都指向各列表的第 0 个。
     堆里放 `(值, 列表编号, 列表内下标)`，另用一个变量 `cur_max` 记录当前 k 个数的最大值。
  3. 每一轮：
     - 当前候选区间就是 `[heap[0].val, cur_max]`，更新答案。
     - **弹出最小的那个**，把它所在列表的**下一个**推进来（同时更新 `cur_max`）。
       为什么动最小的？因为要缩小区间，只能抬高下界 —— 动最大的只会让区间更大。
     - 某个列表走到头 ⟹ **立刻结束**（它再也无法贡献元素，不可能有更优区间）。
  4. 一共最多推进 Σ len(list) 次。

**为什么「弹最小」是对的**：当前区间的下界由最小值决定。
      要么抬高下界（弹最小、补它后面的），要么就只能扩大上界 —— 后者不会更优。
      所以每一步唯一可能改进的动作就是推进最小值所在的列表。∎

比较规则：`b - a < best_b - best_a` 才更新（题目说长度相同取 a 小的，
      而我们是按 a 递增的顺序产生候选的，所以用**严格小于**就自动满足了）。

复杂度：**O(N log k)**，N 是所有元素总数，k 是列表数。空间 O(k)。

和同 Level 1 其他两题的对照：

| | 堆里放什么 | 每轮做什么 |
|---|---|---|
| LC-0378 | 每行的当前元素 | 弹第 t 小，补同行下一个 |
| LC-0373 | 每条链的当前数对 | 弹最小和，补同链下一个 |
| **LC-0632** | 每个列表的当前元素 **+ 外部 cur_max** | 记录 `[堆顶, cur_max]`，弹最小补同列表下一个 |

边界：
  - 只有一个列表 → 区间是 `[x, x]`（任意单个元素）
  - 所有列表都只有一个元素 → `[min, max]`
  - 含负数
  - 列表长度差异很大（短的先走到头，立刻结束）
  - 存在相同的值
"""

import heapq
from typing import List


##################################################################################################
##### ! Solution 1: k 个指针 + 最小堆（取下界）+ cur_max 变量（取上界）
##### ! 时间复杂度: O(N log k)   空间复杂度: O(k)
##### ! 适用：「从每组各取一个，使某个跨组指标最优」；堆管最小、变量管最大
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def smallestRange(self, nums: List[List[int]]) -> List[int]:
        heap = [(row[0], i, 0) for i, row in enumerate(nums)]
        heapq.heapify(heap)
        cur_max = max(row[0] for row in nums)          # ! 上界单独维护，堆只给下界
        best = [heap[0][0], cur_max]
        while True:
            val, i, j = heapq.heappop(heap)
            if cur_max - val < best[1] - best[0]:      # ! 严格小于：a 是递增产生的，自动满足平局规则
                best = [val, cur_max]
            if j + 1 == len(nums[i]):
                return best                            # ! 某个列表走到头，不可能更优了
            nxt = nums[i][j + 1]
            cur_max = max(cur_max, nxt)                # ! 推进最小的那一路，上界可能被抬高
            heapq.heappush(heap, (nxt, i, j + 1))


##################################################################################################
##### ! Solution 2: 暴力 —— 枚举所有「每个列表各取一个」的组合（基准答案，用来对拍）
##### ! 时间复杂度: O(∏ len(list_i))   空间复杂度: O(k)
##### ! 适用：正确性参照；只适合很小的输入
##################################################################################################


class Solution_2:
    def smallestRange(self, nums: List[List[int]]) -> List[int]:
        from itertools import product
        best = None
        for combo in product(*nums):
            lo, hi = min(combo), max(combo)
            if best is None or (hi - lo) < (best[1] - best[0]) or \
               ((hi - lo) == (best[1] - best[0]) and lo < best[0]):
                best = [lo, hi]
        return best


if __name__ == "__main__":
    import random

    cases = [[[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
             [[1]], [[1, 3], [2]], [[-5, -2], [-3, 0], [-1, 4]]]
    for nums in cases:
        a = Solution_1().smallestRange([r[:] for r in nums])
        b = Solution_2().smallestRange([r[:] for r in nums])
        assert a == b, (nums, a, b)
        print(f"{nums} -> {a}")

    for _ in range(800):                 # ! 随机升序列表（含负数、重复、长度不一）对拍
        k = random.randint(1, 4)
        nums = [sorted(random.randint(-6, 9) for _ in range(random.randint(1, 4))) for _ in range(k)]
        a = Solution_1().smallestRange([r[:] for r in nums])
        b = Solution_2().smallestRange([r[:] for r in nums])
        assert a == b, (nums, a, b)
    print("随机对拍 800 组通过 ✓（k 路指针 == 全组合枚举）")
