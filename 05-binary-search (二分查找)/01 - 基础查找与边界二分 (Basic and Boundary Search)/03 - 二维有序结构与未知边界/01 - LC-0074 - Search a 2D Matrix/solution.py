"""LC-0074 - Search a 2D Matrix

Level 1 · 01 基础查找与边界二分 —— 把二维矩阵在**逻辑上**展开成一维有序数组
题目在问：m×n 矩阵，每行递增、且**每行第一个数大于上一行最后一个数**，判断 target 是否存在。

决定性观察：
  1. 题目给的条件（行内递增 + 跨行递增）等价于说：
     **把矩阵按行拼起来就是一个完全有序的一维数组**。
     于是整道题退化成 LC-0704，只是下标要换算。
  2. 换算公式：一维下标 `mid` ↔ `row = mid // cols`, `col = mid % cols`。
  3. 搜索空间是 `[0, m*n)`，所以复杂度是 **O(log(m·n))**，不是 O(log m + log n)
     （虽然两者数值相等：log(mn) = log m + log n，但推导路径不同，说清楚哪一种都行）。

这个展开**依赖题目给的跨行条件**：
      如果只保证「每行递增、每列递增」（那是 LC-0240 Search a 2D Matrix II），
      拼起来**不是**有序数组，这个模板就彻底失效，那题要用「从右上角阶梯走」的 O(m+n) 解法。
      这一点必须分清，是本题最常见的误用。

Loop Invariant（左闭右开 `[lo, hi)`）：
      target 如果存在，它的一维下标一定落在 `[lo, hi)` 里。

复杂度：O(log(m·n)) 时间，O(1) 空间。

边界：
  - 空矩阵 / 空行 → False
  - target 比所有元素都小或都大 → False
  - 1×1 矩阵
  - target 恰好是某行的第一个或最后一个
"""

from typing import List


##################################################################################################
##### ! Solution 1: 把矩阵当成一维有序数组，直接套标准二分
##### ! 时间复杂度: O(log(m·n))   空间复杂度: O(1)
##### ! 适用：行内有序 **且** 跨行有序（上一行末 < 下一行首）的矩阵
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        if not matrix or not matrix[0]:
            return False
        rows, cols = len(matrix), len(matrix[0])
        lo, hi = 0, rows * cols                   # ! 左闭右开 [lo, hi)
        while lo < hi:
            mid = (lo + hi) // 2
            v = matrix[mid // cols][mid % cols]   # ! 一维下标 → 二维坐标
            if v == target:
                return True
            if v < target:
                lo = mid + 1
            else:
                hi = mid
        return False


##################################################################################################
##### ! Solution 2: 两次二分 —— 先定位行（最后一个首元素 <= target），再在行内二分
##### ! 时间复杂度: O(log m + log n)   空间复杂度: O(1)
##### ! 适用：想把「选行」和「选列」两步分开看时；和 Solution_1 等价，可读性各有取舍
##################################################################################################


class Solution_2:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        if not matrix or not matrix[0]:
            return False
        # ! 第一步：找最后一个「首元素 <= target」的行 —— 这是 Last True 模板
        lo, hi = 0, len(matrix) - 1
        row = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if matrix[mid][0] <= target:
                row = mid                          # ! 记录候选，继续往右找更大的
                lo = mid + 1
            else:
                hi = mid - 1
        if row == -1:                              # ! target 比第一个元素还小
            return False
        # ! 第二步：行内标准二分
        lo, hi = 0, len(matrix[row]) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if matrix[row][mid] == target:
                return True
            if matrix[row][mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return False


##################################################################################################
##### ! Solution 3: 线性扫描（基准答案，用来对拍）
##### ! 时间复杂度: O(m·n)   空间复杂度: O(1)
##### ! 适用：正确性参照
##################################################################################################


class Solution_3:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        return any(target in row for row in matrix)


if __name__ == "__main__":
    import random

    m1 = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    for t in (3, 13, 1, 60, 0, 61):
        a = Solution_1().searchMatrix(m1, t)
        assert a == Solution_2().searchMatrix(m1, t) == Solution_3().searchMatrix(m1, t), t
        print(f"target={t} -> {a}")
    assert Solution_1().searchMatrix([], 1) is False
    assert Solution_1().searchMatrix([[]], 1) is False

    for _ in range(500):                 # ! 随机构造满足「整体有序」的矩阵对拍
        rows, cols = random.randint(1, 4), random.randint(1, 4)
        flat = sorted(random.sample(range(0, 60), rows * cols))
        mat = [flat[r * cols:(r + 1) * cols] for r in range(rows)]
        t = random.randint(-1, 61)
        assert (Solution_1().searchMatrix(mat, t)
                == Solution_2().searchMatrix(mat, t)
                == Solution_3().searchMatrix(mat, t)), (mat, t)
    print("随机对拍 500 组通过 ✓")
