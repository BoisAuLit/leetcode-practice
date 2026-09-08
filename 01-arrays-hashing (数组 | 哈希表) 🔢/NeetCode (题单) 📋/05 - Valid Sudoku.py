"""
📌 信号→模式: 行/列/3×3 宫无重复 → 三组哈希集合一次遍历，宫索引 (r//3, c//3)
📅 首次: 2026-09-04 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 未排期
"""
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
