from typing import List

"""
Time complexity: O(N)
Space complexity: O(N)
"""


class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)
        for x in range(0, (n // 2) + n % 2):
            for y in range(0, n // 2):
                x1, y1 = x, y
                x2, y2 = y1, n - 1 - x1
                x3, y3 = n - 1 - x1, n - 1 - y1
                x4, y4 = n - 1 - y1, x1

                (
                    matrix[x2][y2],
                    matrix[x3][y3],
                    matrix[x4][y4],
                    matrix[x1][y1],
                ) = (
                    matrix[x1][y1],
                    matrix[x2][y2],
                    matrix[x3][y3],
                    matrix[x4][y4],
                )


s = Solution()

# Expecting [[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]
matrix = [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]
result = s.rotate(matrix)
print(matrix)

"""

"""
