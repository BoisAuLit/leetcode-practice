"""LC-0304 - Range Sum Query 2D - Immutable

Level 1 · 03 Prefix Sum 与 Prefix-Suffix —— 二维前缀和（2D Prefix Sum）
题目在问：给一个不变的矩阵，多次查询某个子矩形的元素和，每次查询要 O(1)

核心观察：一维前缀和 `sum(i..j) = pre[j+1] - pre[i]`，推到二维就是**容斥**：
      定义 `pre[r][c]` = 左上角 (0,0) 到 (r-1, c-1) 这个矩形的和，则

          sum(r1..r2, c1..c2) = pre[r2+1][c2+1] - pre[r1][c2+1] - pre[r2+1][c1] + pre[r1][c1]
                                   大矩形       -   减去上面     -   减去左边   + 补回多减的左上角

      递推式同样是容斥：`pre[r+1][c+1] = m[r][c] + pre[r][c+1] + pre[r+1][c] - pre[r][c]`。

不变量：`pre` 多开一圈 0（大小 (m+1) x (n+1)），这样所有边界情况都不用特判 ——
      这是二维前缀和唯一需要的「技巧」，padding 比写 4 个 if 可靠得多。

和同层其他题的区别：238 是前缀**积**、560/974 是前缀和配哈希表，
      本题不需要哈希表，它练的是**预处理换查询速度**这件事本身（构造 O(mn)，查询 O(1)）。

坑：
  - 容斥四项的符号：减两次、加一次，少加那一项是最常见的错
  - padding 之后下标整体 +1，`row1` 对应 `pre[row1]` 而不是 `pre[row1+1]`
  - 「Immutable」= 矩阵不会变，所以可以预处理；要支持修改得上树状数组 / 线段树（LC-308）
"""

from typing import List


##################################################################################################
##### ! Solution 1: 二维前缀和 + 容斥，构造 O(mn)、查询 O(1)
##### ! 时间复杂度: 构造 O(mn)，每次查询 O(1)   空间复杂度: O(mn)
##### ! 适用：矩阵不变 + 多次区域求和的标准答案；1314、1738 都是它的变形
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class NumMatrix:
    def __init__(self, matrix: List[List[int]]):
        m, n = len(matrix), len(matrix[0]) if matrix else 0
        # ! 多开一圈 0，省掉所有边界特判
        self.pre = [[0] * (n + 1) for _ in range(m + 1)]
        for r in range(m):
            for c in range(n):
                self.pre[r + 1][c + 1] = (matrix[r][c] + self.pre[r][c + 1]
                                          + self.pre[r + 1][c] - self.pre[r][c])

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        p = self.pre
        # ! 容斥：大矩形 - 上面 - 左边 + 左上角（被减了两次，补回来）
        return (p[row2 + 1][col2 + 1] - p[row1][col2 + 1]
                - p[row2 + 1][col1] + p[row1][col1])


Solution_1 = NumMatrix  # LeetCode 上类名必须叫 NumMatrix


##################################################################################################
##### ! Solution 2: 每行各做一维前缀和，查询时逐行相加
##### ! 时间复杂度: 构造 O(mn)，每次查询 O(m)   空间复杂度: O(mn)
##### ! 适用：行数很少、或者只有少量查询时够用；也是通往解法 1 的中间台阶
##################################################################################################


class NumMatrixRowwise:
    def __init__(self, matrix: List[List[int]]):
        self.rows = []
        for row in matrix:
            acc = [0]
            for v in row:
                acc.append(acc[-1] + v)
            self.rows.append(acc)

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return sum(self.rows[r][col2 + 1] - self.rows[r][col1] for r in range(row1, row2 + 1))


Solution_2 = NumMatrixRowwise


##################################################################################################
##### ! Solution 3: 不预处理，每次查询现场累加（基线）
##### ! 时间复杂度: 每次查询 O(mn)   空间复杂度: O(1) 额外
##### ! 适用：对拍参照；查询次数到 1e4 时必然超时，正好说明预处理的价值
##################################################################################################


class NumMatrixNaive:
    def __init__(self, matrix: List[List[int]]):
        self.m = matrix

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return sum(self.m[r][c] for r in range(row1, row2 + 1) for c in range(col1, col2 + 1))


Solution_3 = NumMatrixNaive


if __name__ == "__main__":
    import random
    mat = [[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]
    for cls in (NumMatrix, NumMatrixRowwise, NumMatrixNaive):
        o = cls([row[:] for row in mat])
        assert o.sumRegion(2, 1, 4, 3) == 8
        assert o.sumRegion(1, 1, 2, 2) == 11
        assert o.sumRegion(1, 2, 2, 4) == 12
    rng = random.Random(304)
    for _ in range(300):
        m, n = rng.randint(1, 6), rng.randint(1, 6)
        g = [[rng.randint(-9, 9) for _ in range(n)] for _ in range(m)]
        objs = [cls([row[:] for row in g]) for cls in (NumMatrix, NumMatrixRowwise, NumMatrixNaive)]
        for _ in range(20):
            r1, r2 = sorted((rng.randrange(m), rng.randrange(m)))
            c1, c2 = sorted((rng.randrange(n), rng.randrange(n)))
            vals = {o.sumRegion(r1, c1, r2, c2) for o in objs}
            assert len(vals) == 1, (g, r1, c1, r2, c2, vals)
    print("3 个解法全过（含 300 个随机矩阵 × 20 次查询对拍）")
