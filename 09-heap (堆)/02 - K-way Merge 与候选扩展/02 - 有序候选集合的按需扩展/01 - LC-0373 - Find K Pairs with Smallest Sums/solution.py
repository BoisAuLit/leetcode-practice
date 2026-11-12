"""LC-0373 - Find K Pairs with Smallest Sums

Level 1 · 02 K-way Merge 与候选扩展 —— **按需扩展候选**（不要把所有候选都塞进堆）
题目在问：两个**升序**数组 nums1、nums2，从中各取一个组成数对，
         返回和最小的 k 个数对。

决定性观察（本题的全部难点在「堆里该放什么」）：
  1. **不能把所有 m×n 个数对都入堆** —— m、n 可达 10⁵，那是 10¹⁰ 个数对，直接爆。
  2. 正确做法：把它看成 **m 条有序链的 k-way merge**。
     第 i 条链是：`(nums1[i], nums2[0]), (nums1[i], nums2[1]), ...`
     因为 nums2 升序，**每条链本身就是和递增的**。
  3. 初始只把**每条链的第一个**入堆：`(nums1[i] + nums2[0], i, 0)`。
     每次弹出堆顶（全局最小的数对），再把**它所在链的下一个**推进去 —— 这就是「按需扩展」。
  4. **初始只需要 min(k, len(nums1)) 条链**：
     答案最多 k 个数对，第 k+1 条链的第一个数对已经不可能进入前 k
     （它比前 k 条链的第一个都大）。这个剪枝让堆大小从 m 降到 min(k, m)。

为什么「弹出的一定是全局第 t 小」：
      堆里始终包含「所有已被弹出数对的**后继**」。任何还没入堆的数对，
      它在自己链上的前驱要么在堆里、要么已被弹出且其后继已入堆 ——
      所以全局最小的未弹出数对一定在堆里。（这就是 k-way merge 的标准论证。）

复杂度：**O(min(k, m) + k log(min(k, m)))** 时间，O(min(k, m)) 空间。
      对比「全部入堆」的 O(mn log(mn))，差距是数量级的。

和 LC-0378 的关系：两题都是 k-way merge。
      378 的「链」是矩阵的每一行，本题的「链」是 `nums1[i]` 配上整个 nums2。
      **骨架完全相同：初始化每条链的头 → 弹出 → 推进同一条链的下一个。**

边界：
  - k 大于 m×n → 返回全部数对
  - 某个数组为空 → 返回 []
  - 含重复值 / 负数
  - k == 1
"""

import heapq
from typing import List


##################################################################################################
##### ! Solution 1: k-way merge —— 每条链只放一个候选，弹一个补一个
##### ! 时间复杂度: O(min(k,m) + k log(min(k,m)))   空间复杂度: O(min(k,m))
##### ! 适用：所有「从有序结构的笛卡尔积里取最小 k 个」的题；和 LC-0378 同骨架
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        if not nums1 or not nums2 or k <= 0:
            return []
        # ! 只初始化前 min(k, m) 条链：再多的链，它的第一个数对也进不了前 k
        heap = [(nums1[i] + nums2[0], i, 0) for i in range(min(k, len(nums1)))]
        heapq.heapify(heap)
        res = []
        while heap and len(res) < k:
            _, i, j = heapq.heappop(heap)
            res.append([nums1[i], nums2[j]])
            if j + 1 < len(nums2):               # ! 只推进「同一条链」的下一个
                heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))
        return res


##################################################################################################
##### ! Solution 2: 全部数对入堆后取前 k 个（基准答案，用来对拍；m×n 大时会爆）
##### ! 时间复杂度: O(mn log(mn))   空间复杂度: O(mn)
##### ! 适用：正确性参照 —— 正好说明 Solution_1 省掉的是什么
##################################################################################################


class Solution_2:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        pairs = [[a, b] for a in nums1 for b in nums2]
        pairs.sort(key=lambda p: p[0] + p[1])
        return pairs[:k]


if __name__ == "__main__":
    import random

    cases = [([1, 7, 11], [2, 4, 6], 3), ([1, 1, 2], [1, 2, 3], 2),
             ([1, 2], [3], 3), ([], [1, 2], 2), ([1], [1], 1),
             ([1, 2, 4, 5, 6], [3, 5, 7, 9], 20)]
    for a1, a2, k in cases:
        x = Solution_1().kSmallestPairs(a1, a2, k)
        y = Solution_2().kSmallestPairs(a1, a2, k)
        # ! 和相同的数对顺序可能不同，所以比较「和的多重集」和长度
        assert len(x) == len(y), (a1, a2, k, x, y)
        assert sorted(p[0] + p[1] for p in x) == sorted(p[0] + p[1] for p in y), (a1, a2, k, x, y)
        print(f"nums1={a1}, nums2={a2}, k={k} -> {x}")

    for _ in range(1000):                # ! 随机升序数组（含重复、负数）对拍
        a1 = sorted(random.randint(-5, 9) for _ in range(random.randint(0, 7)))
        a2 = sorted(random.randint(-5, 9) for _ in range(random.randint(0, 7)))
        k = random.randint(1, 15)
        x = Solution_1().kSmallestPairs(a1, a2, k)
        y = Solution_2().kSmallestPairs(a1, a2, k)
        assert len(x) == len(y), (a1, a2, k)
        assert sorted(p[0] + p[1] for p in x) == sorted(p[0] + p[1] for p in y), (a1, a2, k, x, y)
    print("随机对拍 1000 组通过 ✓（按需扩展 == 全量排序，和的多重集一致）")
