from typing import List

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # Check all the rows
        for i in range(9):
            # check ith row
            digits = set()
            for j in range(9):
                digit = board[i][j]
                if digit in digits:
                    return False
                if digit.isdigit():
                    digits.add(digit)

            # check ith column
            digits = set()
            for j in range(9):
                digit = board[j][i]
                if digit in digits:
                    return False
                if digit.isdigit():
                    digits.add(digit)

            # check the 3x3 grids
            row, column = divmod(i, 3)
            digits = set()
            rowStart = row * 3
            columnStart = column * 3
            for x in range(rowStart, rowStart + 3):
                for y in range(columnStart, columnStart + 3):
                    digit = board[x][y]
                    if digit in digits:
                        return False
                    if digit.isdigit():
                        digits.add(digit)
        return True


s = Solution()

# Expecting True
board = [
    ["5", "3", ".", ".", "7", ".", ".", ".", "."],
    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    [".", "6", ".", ".", ".", ".", "2", "8", "."],
    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    [".", ".", ".", ".", "8", ".", ".", "7", "9"],
]

# Expecting False
# board = [
#     ["8", "3", ".", ".", "7", ".", ".", ".", "."],
#     ["6", ".", ".", "1", "9", "5", ".", ".", "."],
#     [".", "9", "8", ".", ".", ".", ".", "6", "."],
#     ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
#     ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
#     ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
#     [".", "6", ".", ".", ".", ".", "2", "8", "."],
#     [".", ".", ".", "4", "1", "9", ".", ".", "5"],
#     [".", ".", ".", ".", "8", ".", ".", "7", "9"],
# ]
result = s.isValidSudoku(board)
print(result)
