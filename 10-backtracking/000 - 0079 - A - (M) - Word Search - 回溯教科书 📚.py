from typing import List


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        m = len(board)
        n = len(board[0])
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        def backtrack(x, y, suffix):
            if not suffix: # Base case 1: end of DFS
                return True

            # Base case 2: end of DFS
            if (not 0 <= x < m) or (not 0 <= y < n) or board[x][y] != suffix[0]:
                return False

            # Backtracking starts
            res = False
            board[x][y] = "#" # Avoid infinite loop
            for xi, yi in dirs:
                res = backtrack(x + xi, y + yi, suffix[1:])
                if res:
                    break

            # Backtracking ends
            board[x][y] = suffix[0]

            return res

        return any(backtrack(x, y, word) for x in range(m) for y in range(n))
