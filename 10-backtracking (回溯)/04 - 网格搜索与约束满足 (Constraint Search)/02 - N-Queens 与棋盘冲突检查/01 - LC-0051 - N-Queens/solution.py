from typing import List


class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        col, posDiag, negDiag = set(), set(), set()  # 三个「被占用」集合
        res = []
        board = [["."] * n for _ in range(n)]

        def backtrack(r):
            if r == n:  # 放满 n 行 → 收获一个解
                res.append(["".join(row) for row in board])
                return
            for c in range(n):  # 在第 r 行，试每一列
                if c in col or (r + c) in posDiag or (r - c) in negDiag:
                    continue  # 被攻击 → 跳过
                col.add(c)
                posDiag.add(r + c)
                negDiag.add(r - c)  # 放皇后
                board[r][c] = "Q"
                backtrack(r + 1)  # 去下一行
                col.remove(c)
                posDiag.remove(r + c)
                negDiag.remove(r - c)  # 撤销
                board[r][c] = "."

        backtrack(0)
        return res
