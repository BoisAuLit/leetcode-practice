"""LC-0378 - Kth Smallest Element in a Sorted Matrix（第二轮自主新增）

Level 1 · 03 二分答案与可行性判断 —— 在**值域**上二分，可行性是一个**计数**
题目在问：n×n 矩阵，每行递增、每列递增，求全局第 k 小的元素。

为什么新增它（它补的是哪个缺口）：
  前面的二分答案题（875 / 1011 / 1482 / 1283 / 410 / 1552），
  feasible 都是一个**贪心模拟**。这道题的 feasible 是一个**计数函数**
  `count(x) = 矩阵中 <= x 的元素个数`，这是一个独立且极其常用的变体
  （「第 k 小」「第 k 大」「中位数」类问题几乎都走这条路）。
  而且它展示了一个重要细节：**二分的候选值不必是数组里的元素，答案却一定是**（见下）。

  注意：本题**不能**套 LC-0074 的「展开成一维」—— 那需要「上一行末 < 下一行首」，
  本题只保证行内、列内递增，拼起来不是有序数组。这个对比本身就有教学价值。

决定性观察：
  1. 在**值域** `[matrix[0][0], matrix[n-1][n-1]]` 上二分一个数 x。
  2. `count(x) = 矩阵里 <= x 的元素个数`，显然随 x **单调不减**。
  3. 找**最小的** x 使 `count(x) >= k` ⟹ First True。
  4. **为什么这个 x 一定是矩阵里真实存在的元素？**
     设答案为 x₀ = 最小的满足 count(x₀) >= k 的值。
     若 x₀ 不在矩阵中，则 `count(x₀ - 1) == count(x₀) >= k`，
     与 x₀ 的最小性矛盾。所以 x₀ 必然是矩阵中的某个元素。∎
     这条论证是所有「值域二分求第 k 小」的通用保证，必须记住。

count(x) 怎么 O(n) 算（阶梯法）：
      从**左下角**出发（row = n-1, col = 0）：
        - `matrix[row][col] <= x` ⟹ 这一列从上到下到 row 全都 <= x，
          累加 `row + 1`，然后 `col += 1` 往右走。
        - 否则 `row -= 1` 往上走。
      每一步要么右移要么上移，总共最多 2n 步 ⟹ O(n)。

复杂度：**O(n · log(max - min))** 时间，O(1) 空间。
      对比堆解法 O(k log n)：当 k 接近 n² 时二分明显更优，且空间 O(1)。

边界：
  - matrix=[[1,5,9],[10,11,13],[12,13,15]], k=8 → 13
  - k=1 → 左上角；k=n² → 右下角
  - 全部元素相同 → 那个值
  - 1×1 矩阵
"""

import heapq
from typing import List


##################################################################################################
##### ! Solution 0: 遍历全部元素 + 大小为 k 的最大堆（用户原有实现，方法体未改动）
##### ! 时间复杂度: O(n^2 log k)   空间复杂度: O(k)
##### ! 适用：最直观的 Top-K 写法；没有利用矩阵「行列有序」的性质，所以不是本题最优
##################################################################################################


class Solution_0:
    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
        n = len(matrix)
        max_heap = []
        for i in range(n):
            for j in range(n):
                if len(max_heap) <= k - 1:
                    heapq.heappush(max_heap, -matrix[i][j])
                else:
                    heapq.heappushpop(max_heap, -matrix[i][j])
        return -max_heap[0]


##################################################################################################
##### ! Solution 1: 值域二分 + 阶梯法 O(n) 计数（First True）
##### ! 时间复杂度: O(n · log(max - min))   空间复杂度: O(1)
##### ! 适用：所有「第 k 小 / 第 k 大 / 中位数」且能 O(n) 数出「<= x 的个数」的题
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
        n = len(matrix)

        def count_le(x: int) -> int:
            """矩阵里 <= x 的元素个数，从左下角走阶梯，O(n)。"""
            cnt, row, col = 0, n - 1, 0
            while row >= 0 and col < n:
                if matrix[row][col] <= x:
                    cnt += row + 1       # ! 这一列 0..row 全都 <= x（列递增）
                    col += 1
                else:
                    row -= 1
            return cnt

        lo, hi = matrix[0][0], matrix[n - 1][n - 1]
        while lo < hi:
            mid = (lo + hi) // 2
            if count_le(mid) >= k:       # ! 够多了 → 答案在左边（含 mid）
                hi = mid
            else:
                lo = mid + 1
        return lo                        # ! 由上面的论证，lo 一定是矩阵中真实存在的元素


##################################################################################################
##### ! Solution 2: 最小堆多路归并（n 路有序链表取第 k 个）
##### ! 时间复杂度: O(k log n)   空间复杂度: O(n)
##### ! 适用：k 很小时更快；也是「k 路归并」这个独立模板的练习
##################################################################################################


class Solution_2:
    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
        n = len(matrix)
        heap = [(matrix[r][0], r, 0) for r in range(min(n, k))]   # ! 每行的第一个入堆
        heapq.heapify(heap)
        val = matrix[0][0]
        for _ in range(k):
            val, r, c = heapq.heappop(heap)
            if c + 1 < n:
                heapq.heappush(heap, (matrix[r][c + 1], r, c + 1))
        return val


##################################################################################################
##### ! Solution 3: 全部拍平排序取第 k 个（基准答案，用来对拍）
##### ! 时间复杂度: O(n^2 log n)   空间复杂度: O(n^2)
##### ! 适用：正确性参照
##################################################################################################


class Solution_3:
    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
        return sorted(v for row in matrix for v in row)[k - 1]


if __name__ == "__main__":
    import random

    m1 = [[1, 5, 9], [10, 11, 13], [12, 13, 15]]
    for k in (1, 8, 9):
        a = Solution_1().kthSmallest(m1, k)
        assert a == Solution_2().kthSmallest(m1, k) == Solution_3().kthSmallest(m1, k), k
        print(f"k={k} -> {a}")
    assert Solution_1().kthSmallest([[-5]], 1) == -5

    for _ in range(400):                 # ! 随机构造行列都递增的矩阵对拍
        n = random.randint(1, 5)
        base = [[random.randint(0, 6) for _ in range(n)] for _ in range(n)]
        for r in range(n):               # ! 先行内排序
            base[r].sort()
        for c in range(n):               # ! 再列内排序 —— 结果仍保持行内有序
            col = sorted(base[r][c] for r in range(n))
            for r in range(n):
                base[r][c] = col[r]
        k = random.randint(1, n * n)
        a, b, c3 = (Solution_1().kthSmallest(base, k), Solution_2().kthSmallest(base, k),
                    Solution_3().kthSmallest(base, k))
        assert a == b == c3, (base, k, a, b, c3)
    print("随机对拍 400 组通过 ✓")
