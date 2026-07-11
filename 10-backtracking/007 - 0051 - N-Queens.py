from typing import List, Set

"""
Time complexity: O(N!)
Space complexity: O(N²)
"""


class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        def backtrack(
            row: int,
            columns: Set[int],
            diagonals: Set[int],
            antiDiagonals: Set[int],
            currentSolutions: List[str],
            finalSolutions: List[List[str]],
        ) -> bool:
            if row == n:
                finalSolutions.append(currentSolutions.copy())
            for col in range(n):
                if (
                    col in columns
                    or (row - col) in diagonals
                    or (row + col) in antiDiagonals
                ):
                    continue

                currentSolutions.append("." * col + "Q" + "." * (n - 1 - col))

                diagonals.add(row - col)
                antiDiagonals.add(row + col)
                columns.add(col)
                backtrack(
                    row + 1,
                    columns,
                    diagonals,
                    antiDiagonals,
                    currentSolutions,
                    finalSolutions,
                )
                currentSolutions.pop()
                diagonals.remove(row - col)
                antiDiagonals.remove(row + col)
                columns.remove(col)

        finalSolutions = []
        backtrack(0, set(), set(), set(), [], finalSolutions)

        return finalSolutions


s = Solution()
n = 9
result = s.solveNQueens(n)
print(result)
