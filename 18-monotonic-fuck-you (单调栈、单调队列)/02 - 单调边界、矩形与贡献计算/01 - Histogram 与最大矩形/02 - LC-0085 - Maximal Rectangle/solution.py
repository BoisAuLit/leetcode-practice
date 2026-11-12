"""LC-0085 - Maximal Rectangle

Level 1 · 02 单调边界、矩形与贡献计算 —— Matrix → Histogram → Monotonic Stack
题目在问：0/1 矩阵里全为 '1' 的最大矩形面积。

决定性观察（这题的全部价值就在这一步转化）：
  1. 任何一个全 1 矩形，一定有一条**底边**落在某一行上。
     所以只要「枚举底边在第 r 行」，再求出该情形下的最大矩形，取所有行的最大值即可，不会漏。
  2. 固定底边在第 r 行时，第 c 列能往上伸多高？就是「从第 r 行向上连续 1 的个数」。
     把这一行的 heights[] 看成柱状图，问题**原样变成 LC-0084**。
  3. heights 可以逐行 O(cols) 增量维护：
         matrix[r][c] == '1' → heights[c] += 1
         matrix[r][c] == '0' → heights[c] = 0      （柱子被切断，必须清零而不是减一）

为什么遇到 '0' 要清零：高度的定义是「向上**连续**的 1」，一旦断了，连续段就从头开始。

复杂度：rows 行，每行跑一次 O(cols) 的单调栈 → **O(rows * cols)** 时间，O(cols) 空间。
      不能因为内层有 while 就说成 O(rows * cols^2)：每行里每根柱子最多入栈出栈各一次。

和 LC-0084 的关系：本题不需要记一套新的矩形算法，
      只需要记住「二维 → 每行一个柱状图」这一个转化，核心仍是 84 的边界结算。
      因此标记 **P2**：先把 84 吃透，85 是顺带的。

边界：
  - 全 0 矩阵 → 0
  - 单行 ["1","0","1","1"] → 2
  - 单列 → 连续 1 的个数
  - 全 1 的 r×c 矩阵 → r*c
"""

from typing import List


def _largest_rectangle(heights: List[int]) -> int:
    """LC-0084 的核心：单调递增索引栈 + 左右边界结算。不修改调用者传进来的 heights。"""
    stack: List[int] = []            # ! 存下标，对应高度单调不减
    best = 0
    n = len(heights)
    for i in range(n + 1):           # ! i == n 时当作一根高度 0 的哨兵（Sentinel），把栈清空
        cur = 0 if i == n else heights[i]
        while stack and heights[stack[-1]] > cur:
            h = heights[stack.pop()]             # ! 它的右边界就是 i（第一个比它矮的）
            left = stack[-1] if stack else -1    # ! 弹完之后的新栈顶就是左边界
            best = max(best, h * (i - left - 1)) # ! 宽度要减 1：两个边界都是开区间
        stack.append(i)
    return best


##################################################################################################
##### ! Solution 1: 逐行维护 heights，每行调用一次 LC-0084 的单调栈
##### ! 时间复杂度: O(rows * cols)   空间复杂度: O(cols)
##### ! 适用：所有「二维 0/1 矩阵求最大全 1 子矩形」；记住 Matrix → Histogram 这一步就够
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        if not matrix or not matrix[0]:
            return 0
        cols = len(matrix[0])
        heights = [0] * cols
        best = 0
        for row in matrix:
            for c in range(cols):
                heights[c] = heights[c] + 1 if row[c] == "1" else 0   # ! 遇 0 清零，不是减一
            best = max(best, _largest_rectangle(heights))
        return best


##################################################################################################
##### ! Solution 2: 逐行维护 left / right / height 三个数组（不显式用栈的经典 DP 写法）
##### ! 时间复杂度: O(rows * cols)   空间复杂度: O(cols)
##### ! 适用：想避开单调栈时的替代写法；也能帮助看清「左右边界」到底是什么
##################################################################################################


class Solution_2:
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        if not matrix or not matrix[0]:
            return 0
        cols = len(matrix[0])
        height = [0] * cols
        left = [0] * cols            # ! 当前高度下，向左能延伸到的最小列下标
        right = [cols] * cols        # ! 向右能延伸到的列下标（开区间）
        best = 0
        for row in matrix:
            cur_left, cur_right = 0, cols
            for c in range(cols):                     # ! 高度
                height[c] = height[c] + 1 if row[c] == "1" else 0
            for c in range(cols):                     # ! 左边界：从左往右
                if row[c] == "1":
                    left[c] = max(left[c], cur_left)
                else:
                    left[c], cur_left = 0, c + 1
            for c in range(cols - 1, -1, -1):         # ! 右边界：从右往左
                if row[c] == "1":
                    right[c] = min(right[c], cur_right)
                else:
                    right[c], cur_right = cols, c
            for c in range(cols):
                best = max(best, (right[c] - left[c]) * height[c])
        return best


##################################################################################################
##### ! Solution 3: 暴力枚举左上 / 右下角（基准答案，用来对拍）
##### ! 时间复杂度: O(rows^2 * cols^2)   空间复杂度: O(rows * cols)
##### ! 适用：正确性参照
##################################################################################################


class Solution_3:
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        if not matrix or not matrix[0]:
            return 0
        rows, cols = len(matrix), len(matrix[0])
        pre = [[0] * (cols + 1) for _ in range(rows + 1)]      # ! 二维前缀和，数 1 的个数
        for r in range(rows):
            for c in range(cols):
                pre[r + 1][c + 1] = (int(matrix[r][c] == "1") + pre[r][c + 1]
                                     + pre[r + 1][c] - pre[r][c])
        best = 0
        for r1 in range(rows):
            for r2 in range(r1, rows):
                for c1 in range(cols):
                    for c2 in range(c1, cols):
                        area = (r2 - r1 + 1) * (c2 - c1 + 1)
                        ones = (pre[r2 + 1][c2 + 1] - pre[r1][c2 + 1]
                                - pre[r2 + 1][c1] + pre[r1][c1])
                        if ones == area:
                            best = max(best, area)
        return best


if __name__ == "__main__":
    import random

    cases = [
        [["1", "0", "1", "0", "0"], ["1", "0", "1", "1", "1"],
         ["1", "1", "1", "1", "1"], ["1", "0", "0", "1", "0"]],      # 官方样例 → 6
        [["0"]], [["1"]], [], [["1", "0", "1", "1"]],
        [["1", "1"], ["1", "1"]],
    ]
    for m in cases:
        a = Solution_1().maximalRectangle([r[:] for r in m])
        assert a == Solution_2().maximalRectangle([r[:] for r in m]) == Solution_3().maximalRectangle([r[:] for r in m])
        print(f"{m} -> {a}")

    for _ in range(200):                 # ! 随机小矩阵对拍
        R, C = random.randint(1, 4), random.randint(1, 4)
        m = [[random.choice("01") for _ in range(C)] for _ in range(R)]
        assert (Solution_1().maximalRectangle([r[:] for r in m])
                == Solution_2().maximalRectangle([r[:] for r in m])
                == Solution_3().maximalRectangle([r[:] for r in m])), m
    print("随机对拍 200 组通过 ✓")
