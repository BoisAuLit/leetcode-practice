from typing import List

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def transpose(self, matrix: List[List[int]]) -> List[List[int]]:
        m = len(matrix)
        n = len(matrix[0])
        result = [[0] * m for _ in range(n)]
        for i in range(n):
            for j in range(m):
                result[i][j] = matrix[j][i]
        return result


s = Solution()

# Expecting [[1,4,7],[2,5,8],[3,6,9]]
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
result = s.transpose(matrix)

print(result)

"""
Runtime
- 85ms
- Beats 53.17%

Memory
17.21mb
- Beats 38.83%
"""
