from typing import List, Tuple, Set

"""
Time complexity: O()
Space complexity: O()
"""


def prettyPrint2DArray(array: List[List[str]]) -> None:
    print("-" * 25)
    for idx, row in enumerate(board):
        rowStr = " | ".join([" ".join(map(str, row[i : i + 3])) for i in range(0, len(row), 3)])
        print(f"| {rowStr} |")
        if (idx + 1) % 3 == 0:
            print("-" * 25)


class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        digits = set(str(x) for x in range(1, 10))

        def getAvailableChoices(row: int, col: int) -> Set[str]:
            numbersAlreadyExist = set((x for x in board[row] if x.isdigit()))
            numbersAlreadyExist.update(x for x in [arr[col] for arr in board] if x.isdigit())
            rowStart = (row // 3) * 3
            colStart = (col // 3) * 3
            numbersAlreadyExist.update(
                board[x][y]
                for x in range(rowStart, rowStart + 3)
                for y in range(colStart, colStart + 3)
                if board[x][y].isdigit()
            )
            return digits.difference(numbersAlreadyExist)

        def getNextRowCol(row: int, col: int) -> Tuple[int, int]:
            return (row, col + 1) if col <= 7 else (row + 1, 0)

        def backtrack(row: int, col: int):
            if row == 9 and col == 0:
                return True
            if board[row][col].isdigit():
                return backtrack(*getNextRowCol(row, col))
            for choice in getAvailableChoices(row, col):
                board[row][col] = choice
                if backtrack(*getNextRowCol(row, col)):
                    return True
                board[row][col] = "."

        backtrack(0, 0)


s = Solution()
board = [
    [".", ".", "9", "7", "4", "8", ".", ".", "."],
    ["7", ".", ".", ".", ".", ".", ".", ".", "."],
    [".", "2", ".", "1", ".", "9", ".", ".", "."],
    [".", ".", "7", ".", ".", ".", "2", "4", "."],
    [".", "6", "4", ".", "1", ".", "5", "9", "."],
    [".", "9", "8", ".", ".", ".", "3", ".", "."],
    [".", ".", ".", "8", ".", "3", ".", "2", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", "6"],
    [".", ".", ".", "2", "7", "5", "9", ".", "."],
]
s.solveSudoku(board)
prettyPrint2DArray(board)
