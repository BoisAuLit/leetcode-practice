from typing import List


class Solution:
    def tictactoe(self, moves: List[List[int]]) -> str:
        rows, cols = [0] * 3, [0] * 3
        diag = anti_diag = 0
        player = 1
        for row, col in moves:
            rows[row] += player
            cols[col] += player
            if row == col:
                diag += player
            if row + col == 2:
                anti_diag += player
            if any(
                abs(line) == 3
                for line in (rows[row], cols[col], diag, anti_diag)
            ):
                return "A" if player == 1 else "B"
            player *= -1
        return "Draw" if len(moves) == 9 else "Pending"


s = Solution()

"""
Test case 1: Expecting "A"
+---+---+---+
| X |   |   |
+---+---+---+
|   | X |   |
+---+---+---+
| O | O | X |
+---+---+---+
"""
moves = [[0, 0], [2, 0], [1, 1], [2, 1], [2, 2]]

"""
Test case 2: Expecting "B"
+---+---+---+
| X | X | O |
+---+---+---+
| X | O |   |
+---+---+---+
| O |   |   |
+---+---+---+
"""
# moves = [[0, 0], [1, 1], [0, 1], [0, 2], [1, 0], [2, 0]]

"""
Test case 3: Expecting "Draw"
+---+---+---+
| X | X | O |
+---+---+---+
| O | O | X |
+---+---+---+
| X | O | X |
+---+---+---+
"""
# moves = [[0, 0], [1, 1], [2, 0], [1, 0], [1, 2], [2, 1], [0, 1], [0, 2], [2, 2]]

result = s.tictactoe(moves)


print(result)

"""

"""
