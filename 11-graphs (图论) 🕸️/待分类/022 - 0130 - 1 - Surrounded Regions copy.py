from typing import List, Set, Tuple

"""
Time complexity: O()
Space complexity: O()
"""


def printBoard(board: List[List[str]]) -> None:
    for m in range(len(board)):
        for n in range(len(board[0])):
            print(board[m][n], end="")
        print()


class Solution:
    def flip(
        self, regionO: Set[Tuple[int, int]], board: List[List[str]]
    ) -> None:
        for x, y in regionO:
            board[x][y] = "X"

    def containsBorderO(
        self,
        x: int,
        y: int,
        board: List[List[str]],
        visited: Set[Tuple[int, int]],
        regionO: Set[Tuple[int, int]],
    ) -> bool:
        if (
            (not 0 <= x < len(board))
            or (not 0 <= y < len(board[0]))
            or board[x][y] == "X"
            or (x, y) in visited
        ):
            return False
        visited.add((x, y))
        regionO.add((x, y))
        result = False
        if x == 0 or x == len(board) - 1 or y == 0 or y == len(board[0]) - 1:
            result = True
        # result = False
        for a, b in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            result |= self.containsBorderO(
                x + a, y + b, board, visited, regionO
            )
        return result

    def solve(self, board: List[List[str]]) -> None:
        visited = set()
        for x in range(len(board)):
            for y in range(len(board[0])):
                if board[x][y] == "O":
                    regionO = set()
                    if not self.containsBorderO(x, y, board, visited, regionO):
                        self.flip(regionO, board)


s = Solution()

"""
Expected result:
[
    ["X", "O", "O", "X", "X", "X", "O", "X", "O", "O"],
    ["X", "O", "X", "X", "X", "X", "X", "X", "X", "X"],
    ["X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
    ["X", "X", "X", "X", "X", "X", "X", "X", "X", "O"],
    ["O", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
    ["X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
    ["O", "X", "X", "X", "X", "X", "X", "X", "X", "O"],
    ["O", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
    ["X", "X", "X", "X", "X", "X", "X", "X", "O", "O"],
    ["X", "X", "X", "O", "O", "X", "O", "X", "X", "O"],
]
"""

expected = [
    ["X", "O", "O", "X", "X", "X", "O", "X", "O", "O"],
    ["X", "O", "X", "X", "X", "X", "X", "X", "X", "X"],
    ["X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
    ["X", "X", "X", "X", "X", "X", "X", "X", "X", "O"],
    ["O", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
    ["X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
    ["O", "X", "X", "X", "X", "X", "X", "X", "X", "O"],
    ["O", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
    ["X", "X", "X", "X", "X", "X", "X", "X", "O", "O"],
    ["X", "X", "X", "O", "O", "X", "O", "X", "X", "O"],
]

board = [
    ["X", "O", "O", "X", "X", "X", "O", "X", "O", "O"],
    ["X", "O", "X", "X", "X", "X", "X", "X", "X", "X"],
    ["X", "X", "X", "X", "O", "X", "X", "X", "X", "X"],
    ["X", "O", "X", "X", "X", "O", "X", "X", "X", "O"],
    ["O", "X", "X", "X", "O", "X", "O", "X", "O", "X"],
    ["X", "X", "O", "X", "X", "O", "O", "X", "X", "X"],
    ["O", "X", "X", "O", "O", "X", "O", "X", "X", "O"],
    ["O", "X", "X", "X", "X", "X", "O", "X", "X", "X"],
    ["X", "O", "O", "X", "X", "O", "X", "X", "O", "O"],
    ["X", "X", "X", "O", "O", "X", "O", "X", "X", "O"],
]
print("\t\tBefore")
printBoard(board)
print("*****************************************")

result = s.solve(board)

print("\t\tAfter")
printBoard(board)
print("*****************************************")

print("\t\tExpected")
printBoard(expected)
print("*****************************************")
"""

"""
