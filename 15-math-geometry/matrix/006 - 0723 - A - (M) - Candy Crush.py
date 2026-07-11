from typing import List
from pprint import pprint

"""
m -> Number of rows
n -> Number of columns
"""


def print_2d_array(matrix):
    print("\n".join(["\t".join([str(cell) for cell in row]) for row in matrix]))


class Solution:
    def candyCrush(self, board: List[List[int]]) -> List[List[int]]:
        m, n = len(board), len(board[0])

        while True:
            # Find all points to crush
            to_crush = set()

            # Check horizontally and vertically in one pass
            for i in range(m):
                for j in range(n):
                    # ! We don't care about zeros
                    if board[i][j] == 0:
                        continue

                    # ! Check horizontal streak
                    if j <= n - 3:
                        if board[i][j] == board[i][j + 1] == board[i][j + 2]:
                            to_crush.update((i, j + k) for k in range(3))

                    # ! Check vertical streak
                    if i <= m - 3:
                        if board[i][j] == board[i + 1][j] == board[i + 2][j]:
                            to_crush.update((i + k, j) for k in range(3))

            # If nothing to crush, we're done
            if not to_crush:
                break

            # Crush the candies
            for i, j in to_crush:
                board[i][j] = 0

            # Drop candies down
            for j in range(n):
                # Collect non-zero values from bottom to top
                values = []
                for i in range(m - 1, -1, -1):
                    if board[i][j] != 0:
                        values.append(board[i][j])
                        board[i][j] = 0

                # Place values back from bottom
                for idx, val in enumerate(values):
                    board[m - 1 - idx][j] = val

        return board


s = Solution()
board = [
    [110, 5, 112, 113, 114],
    [210, 211, 5, 213, 214],
    [310, 311, 3, 313, 314],
    [410, 411, 412, 5, 414],
    [5, 1, 512, 3, 3],
    [610, 4, 1, 613, 614],
    [710, 1, 2, 713, 714],
    [810, 1, 2, 1, 1],
    [1, 1, 2, 2, 2],
    [4, 1, 4, 4, 1014],
]
result = s.candyCrush(board)

print("\n\n------ The final result")
print_2d_array(result)

# ! ###########################################
# ! ###########################################
# ! ###########################################
# ! ###########################################
# ! ###########################################
# s = Solution()
# board = [
#     [110, 0, 0, 0, 0],  #
#     [210, 0, 0, 113, 114],  #
#     [310, 0, 0, 213, 214],  #
#     [410, 0, 112, 313, 314],  #
#     [0, 0, 0, 0, 414],  #
#     [610, 211, 0, 0, 0],  #
#     [710, 311, 412, 613, 614],  #
#     [810, 411, 512, 713, 714],  #
#     [0, 0, 0, 0, 0],  #
#     [0, 0, 0, 0, 1014],  #
# ]
# pprint(board)
# print("------------------------")
# s.remove_spaces(board, 10, 5)
# pprint(board)


# ! ###########################################
# ! ###########################################
# ! ###########################################
# ! ###########################################
# ! ###########################################
# s = Solution()
# board = [
#     [110, 0, 0, 0, 0],  #
#     [210, 0, 0, 113, 114],  #
#     [310, 0, 0, 213, 214],  #
#     [410, 0, 112, 313, 314],  #
#     [5, 5, 5, 5, 414],  #
#     [610, 211, 3, 3, 3],  #
#     [710, 311, 412, 613, 614],  #
#     [810, 411, 512, 713, 714],  #
#     [1, 1, 1, 1, 1],  #
#     [4, 4, 4, 4, 1014],  #
# ]
# print_2d_array(board)
# print("-------------------------------------")
# result = s.crush(board, 10, 5)
# print_2d_array(board)
# print("-------------------------------------")
# s.remove_spaces(board, 10, 5)
# print_2d_array(board)
# print("-------------------------------------")
