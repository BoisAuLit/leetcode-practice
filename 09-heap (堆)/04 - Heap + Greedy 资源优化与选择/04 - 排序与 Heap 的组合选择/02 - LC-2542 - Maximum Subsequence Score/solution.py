"""LC-2542 - Maximum Subsequence Score

Level 1 · 04 Heap + Greedy —— **枚举最小值 + 堆维护 Top K 和**
题目在问：从两个长度为 n 的数组里选 k 个下标，
         score = `(选中的 nums1 之和) × (选中的 nums2 的最小值)`，求最大 score。

这题是「两个维度相互牵制」的典型：
  nums1 要**和尽量大**，nums2 要**最小值尽量大**，而选的是同一批下标。

决定性观察：
  1. **固定一个维度**：枚举「nums2 的最小值是谁」。
     把下标按 **nums2 降序**排序，当遍历到第 i 个时，
     前 i 个（含自己）的 nums2 都 **>= nums2[i]** ——
     所以**如果最小值取 nums2[i]**，候选池就是前 i+1 个下标。
  2. **优化另一个维度**：在这个候选池里要选 k 个使 nums1 之和最大
     ⟹ 维护一个**大小为 k 的最小堆**装 nums1，和一个 running sum。
     每加入一个新元素，若堆超过 k 就弹掉**最小的那个**（它对和的贡献最差）。
  3. 当堆里恰好有 k 个时，`score = cur_sum × nums2[i]`，取最大值。

**为什么降序排而不是升序**：降序保证「遍历到 i 时，前面的 nums2 都不小于 nums2[i]」，
      于是 `nums2[i]` 天然就是当前候选池的最小值。升序排的话最小值在最前面，
      候选池反而随遍历缩小，没法用「加入 + 弹最小」的增量维护。

**为什么弹掉 nums1 最小的是安全的**：候选池里选 k 个使和最大 ⟹ 就是取 Top-K 大。
      最小堆的堆顶正是当前 k+1 个里最该被淘汰的那个。

复杂度：**O(n log n + n log k)** —— 排序 + 每个元素一次堆操作。空间 O(k)。

和 LC-0502 的对照（同一个 Level 2 的原因）：

| | LC-0502 IPO | LC-2542 |
|---|---|---|
| 排序哪个维度 | capital 升序（用来**解锁**） | nums2 降序（用来**枚举最小值**） |
| 堆里放什么 | profit（**最大**堆，取最优） | nums1（**最小**堆，踢最差） |
| 堆的作用 | 从可选集合里挑最好的 | 维护 Top-K 的和 |

边界：
  - k == n → 只有一种选法
  - k == 1 → 答案是 `max(nums1[i] * nums2[i])`
  - 含 0
  - 所有 nums2 相同
"""

import heapq
from typing import List


##################################################################################################
##### ! Solution 1: 按 nums2 降序排序 + 大小为 k 的最小堆维护 nums1 的 Top-K 和
##### ! 时间复杂度: O(n log n + n log k)   空间复杂度: O(k)
##### ! 适用：「两个维度相互牵制」—— 排序固定一个（通常是取 min/max 的那个），堆优化另一个
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def maxScore(self, nums1: List[int], nums2: List[int], k: int) -> int:
        pairs = sorted(zip(nums2, nums1), reverse=True)   # ! 按 nums2 降序
        heap: List[int] = []
        cur_sum = 0
        best = 0
        for v2, v1 in pairs:
            heapq.heappush(heap, v1)
            cur_sum += v1
            if len(heap) > k:
                cur_sum -= heapq.heappop(heap)            # ! 弹掉 nums1 最小的（对和贡献最差）
            if len(heap) == k:
                # ! 此刻 v2 就是候选池里 nums2 的最小值（因为是降序遍历过来的）
                best = max(best, cur_sum * v2)
        return best


##################################################################################################
##### ! Solution 2: 暴力枚举所有大小为 k 的下标组合（基准答案，用来对拍）
##### ! 时间复杂度: O(C(n,k) · k)   空间复杂度: O(k)
##### ! 适用：正确性参照；只适合很小的 n
##################################################################################################


class Solution_2:
    def maxScore(self, nums1: List[int], nums2: List[int], k: int) -> int:
        from itertools import combinations
        n = len(nums1)
        best = 0
        for comb in combinations(range(n), k):
            s = sum(nums1[i] for i in comb)
            m = min(nums2[i] for i in comb)
            best = max(best, s * m)
        return best


if __name__ == "__main__":
    import random

    cases = [([1, 3, 3, 2], [2, 1, 3, 4], 3), ([4, 2, 3, 1, 1], [7, 5, 10, 9, 6], 1),
             ([1], [1], 1), ([2, 1, 14, 12], [11, 7, 13, 6], 3)]
    for a1, a2, k in cases:
        x = Solution_1().maxScore(a1, a2, k)
        y = Solution_2().maxScore(a1, a2, k)
        assert x == y, (a1, a2, k, x, y)
        print(f"nums1={a1}, nums2={a2}, k={k} -> {x}")

    for _ in range(800):
        n = random.randint(1, 7)
        a1 = [random.randint(0, 9) for _ in range(n)]
        a2 = [random.randint(0, 9) for _ in range(n)]
        k = random.randint(1, n)
        assert Solution_1().maxScore(a1, a2, k) == Solution_2().maxScore(a1, a2, k), (a1, a2, k)
    print("随机对拍 800 组通过 ✓（排序+堆 == 枚举所有组合）")
