from typing import Set

"""
Time complexity: O(N!)
Space complexity: O(N)
"""


class Solution:
    def totalNQueens(self, n):
        def backtrack(
            row: int,
            columns: Set[int],
            diagonals: Set[int],
            antiDiagonals: Set[int],
        ) -> bool:
            if row == n:
                return 1
            currentSum = 0
            for col in range(n):
                if (
                    col in columns
                    or (row - col) in diagonals
                    or (row + col) in antiDiagonals
                ):
                    continue
                diagonals.add(row - col)
                antiDiagonals.add(row + col)
                columns.add(col)
                currentSum += backtrack(
                    row + 1, columns, diagonals, antiDiagonals
                )
                diagonals.remove(row - col)
                antiDiagonals.remove(row + col)
                columns.remove(col)
            return currentSum

        return backtrack(0, set(), set(), set())


s = Solution()
input_ = 4
result = s.totalNQueens(input_)
print(result)

"""

"""
