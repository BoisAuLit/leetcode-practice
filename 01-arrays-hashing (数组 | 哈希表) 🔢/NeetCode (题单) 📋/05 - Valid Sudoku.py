from typing import List
from collections import defaultdict


class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        rows = defaultdict(set)
        cols = defaultdict(set)
        squares = defaultdict(set)
        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    continue
                ch = board[r][c]
                if (
                    ch in rows[r]
                    or ch in cols[c]
                    or ch in squares[(r // 3, c // 3)]
                ):
                    return False
                rows[r].add(ch)
                cols[c].add(ch)
                squares[(r // 3, c // 3)].add(ch)
        return True
