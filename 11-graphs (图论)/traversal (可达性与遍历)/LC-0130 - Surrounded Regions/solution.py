"""LC-0130 - Surrounded Regions

合并自 3 个解法文件:
  1. 022 - 0130 - 1 - Surrounded Regions copy.py
  2. 022 - 0130 - Surrounded Regions.py
  3. 0130 - Surrounded Regions - BFS from border O's.py
"""

from typing import List, Set, Tuple

from collections import deque

from pprint import pprint


# ============================================================================
# Solution 1: Surrounded_Regions_copy    (原文件: 022 - 0130 - 1 - Surrounded Regions copy.py)
# ============================================================================

# Time complexity: O()
# Space complexity: O()

# Expected result:
# [
#     ["X", "O", "O", "X", "X", "X", "O", "X", "O", "O"],
#     ["X", "O", "X", "X", "X", "X", "X", "X", "X", "X"],
#     ["X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
#     ["X", "X", "X", "X", "X", "X", "X", "X", "X", "O"],
#     ["O", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
#     ["X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
#     ["O", "X", "X", "X", "X", "X", "X", "X", "X", "O"],
#     ["O", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
#     ["X", "X", "X", "X", "X", "X", "X", "X", "O", "O"],
#     ["X", "X", "X", "O", "O", "X", "O", "X", "X", "O"],
# ]

expected_1 = [
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

board_1 = [
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


def printBoard_1(board_1: List[List[str]]) -> None:
    for m in range(len(board_1)):
        for n in range(len(board_1[0])):
            print(board_1[m][n], end="")
        print()

class Solution_1_Surrounded_Regions_copy:
    def flip(
        self, regionO: Set[Tuple[int, int]], board_1: List[List[str]]
    ) -> None:
        for x, y in regionO:
            board_1[x][y] = "X"

    def containsBorderO(
        self,
        x: int,
        y: int,
        board_1: List[List[str]],
        visited: Set[Tuple[int, int]],
        regionO: Set[Tuple[int, int]],
    ) -> bool:
        if (
            (not 0 <= x < len(board_1))
            or (not 0 <= y < len(board_1[0]))
            or board_1[x][y] == "X"
            or (x, y) in visited
        ):
            return False
        visited.add((x, y))
        regionO.add((x, y))
        result = False
        if x == 0 or x == len(board_1) - 1 or y == 0 or y == len(board_1[0]) - 1:
            result = True
        # result = False
        for a, b in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            result |= self.containsBorderO(
                x + a, y + b, board_1, visited, regionO
            )
        return result

    def solve(self, board_1: List[List[str]]) -> None:
        visited = set()
        for x in range(len(board_1)):
            for y in range(len(board_1[0])):
                if board_1[x][y] == "O":
                    regionO = set()
                    if not self.containsBorderO(x, y, board_1, visited, regionO):
                        self.flip(regionO, board_1)

# ============================================================================
# Solution 2: Surrounded_Regions    (原文件: 022 - 0130 - Surrounded Regions.py)
# ============================================================================

# Time complexity: O()
# Space complexity: O()

# Expected result:
# [
#     ["X", "O", "O", "X", "X", "X", "O", "X", "O", "O"],
#     ["X", "O", "X", "X", "X", "X", "X", "X", "X", "X"],
#     ["X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
#     ["X", "X", "X", "X", "X", "X", "X", "X", "X", "O"],
#     ["O", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
#     ["X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
#     ["O", "X", "X", "X", "X", "X", "X", "X", "X", "O"],
#     ["O", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
#     ["X", "X", "X", "X", "X", "X", "X", "X", "O", "O"],
#     ["X", "X", "X", "O", "O", "X", "O", "X", "X", "O"],
# ]

expected_2 = [
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

board_2 = [
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


def printBoard_2(board_2: List[List[str]]) -> None:
    for m in range(len(board_2)):
        for n in range(len(board_2[0])):
            print(board_2[m][n], end="")
        print()

class Solution_2_Surrounded_Regions:
    def flip(
        self, regionO: Set[Tuple[int, int]], board_2: List[List[str]]
    ) -> None:
        for x, y in regionO:
            board_2[x][y] = "X"

    def containsBorderO(
        self,
        x: int,
        y: int,
        board_2: List[List[str]],
        visited: Set[Tuple[int, int]],
        regionO: Set[Tuple[int, int]],
    ) -> bool:
        if (
            (not 0 <= x < len(board_2))
            or (not 0 <= y < len(board_2[0]))
            or board_2[x][y] == "X"
            or (x, y) in visited
        ):
            return False
        visited.add((x, y))
        regionO.add((x, y))
        result = False
        if x == 0 or x == len(board_2) - 1 or y == 0 or y == len(board_2[0]) - 1:
            result = True
        # result = False
        for a, b in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            result |= self.containsBorderO(
                x + a, y + b, board_2, visited, regionO
            )
        return result

    def solve(self, board_2: List[List[str]]) -> None:
        visited = set()
        for x in range(len(board_2)):
            for y in range(len(board_2[0])):
                if board_2[x][y] == "O":
                    regionO = set()
                    if not self.containsBorderO(x, y, board_2, visited, regionO):
                        self.flip(regionO, board_2)

# ============================================================================
# Solution 3: BFS_from_border_O_s    (原文件: 0130 - Surrounded Regions - BFS from border O's.py)
# ============================================================================

input_ = [
  ["X","X","X","X"],
  ["X","O","O","X"],
  ["X","X","O","X"],
  ["X","O","X","X"]
]

class Solution_3_BFS_from_border_O_s:
    def solve(self, board: List[List[str]]) -> None:
        m = len(board)
        n = len(board[0])

        regions = set()
        q = deque()
        seen = set()
        for x in range(m):
            for y in range(n):
                if board[x][y] == "O":
                    regions.add((x, y))
                    if x == 0 or x == m - 1 or y == 0 or y == n - 1:
                        q.append((x, y))
                        seen.add((x, y))

        while q:
            x, y = q.popleft()
            regions.remove((x,y))
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and board[nx][ny] == "O" and (nx, ny) not in seen:
                    seen.add((nx, ny))
                    q.append((nx, ny))
        for x, y in regions:
            board[x][y] = "X"


if __name__ == "__main__":

    # --- Solution 1: Surrounded_Regions_copy ---
    s = Solution_1_Surrounded_Regions_copy()
    print("\t\tBefore")
    printBoard_1(board_1)
    print("*****************************************")
    result = s.solve(board_1)
    print("\t\tAfter")
    printBoard_1(board_1)
    print("*****************************************")
    print("\t\tExpected")
    printBoard_1(expected_1)
    print("*****************************************")

    # --- Solution 2: Surrounded_Regions ---
    s = Solution_2_Surrounded_Regions()
    print("\t\tBefore")
    printBoard_2(board_2)
    print("*****************************************")
    result = s.solve(board_2)
    print("\t\tAfter")
    printBoard_2(board_2)
    print("*****************************************")
    print("\t\tExpected")
    printBoard_2(expected_2)
    print("*****************************************")

    # --- Solution 3: BFS_from_border_O_s ---
    s = Solution_3_BFS_from_border_O_s()
    pprint(input_)
    result = s.solve(input_)
    print()
    pprint(input_)
