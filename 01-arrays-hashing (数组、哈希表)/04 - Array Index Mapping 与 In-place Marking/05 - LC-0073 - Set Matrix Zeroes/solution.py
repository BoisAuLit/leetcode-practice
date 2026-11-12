from typing import List


class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        m, n = len(matrix), len(matrix[0])

        # ① 先单独记录:第 0 行/第 0 列自己原本有没有 0(它们即将被征用,原始信息要备份)
        first_row_has_zero = any(matrix[0][j] == 0 for j in range(n))
        first_col_has_zero = any(matrix[i][0] == 0 for i in range(m))

        # ② 用第 0 行/列做记事本:内部区域发现 0,就在对应的行头、列头做标记
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0
                    matrix[0][j] = 0

        # ③ 按记事本清零内部区域(从 (1,1) 开始,不碰记事本自己)
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0

        # ④ 最后处理记事本自己(顺序必须最后,否则记事本先被抹掉,内部就没依据了)
        if first_row_has_zero:
            for j in range(n):
                matrix[0][j] = 0
        if first_col_has_zero:
            for i in range(m):
                matrix[i][0] = 0
