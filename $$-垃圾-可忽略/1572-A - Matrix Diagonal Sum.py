from typing import List

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def diagonalSum(self, mat: List[List[int]]) -> int:
        len_ = len(mat)
        sum_ = 0 if len_ % 2 == 0 else -mat[len_ // 2][len_ // 2]
        return sum_ + sum(mat[i][i] + mat[i][len_ - 1 - i] for i in range(len(mat)))


# class Solution:
#     def diagonalSum(self, mat: List[List[int]]) -> int:
#         length = len(mat)
#         sum_ = 0 if length % 2 == 0 else -mat[length // 2][length // 2]
#         for i in range(len(mat)):
#             sum_ += mat[i][i] + mat[i][length - 1 - i]
#         return sum_


s = Solution()

# Expecting 25
mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Expecting 8
# mat = [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]

result = s.diagonalSum(mat)
print(result)

"""
Runtime
- 118ms
- Beats 76.85%

Memory
- 16.53mb
- Beats 82.21%
"""
