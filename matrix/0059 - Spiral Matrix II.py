from typing import List

"""
Time complexity: O(N²)
Space complexity: O(1)
"""

class Solution:
    def generateMatrix(self, n: int) -> List[List[int]]:
        matrix = [[[] for _ in range(n)] for _ in range(n)]
        number = 1
        direction = 1  # Start off going right
        i, j = 0, -1
        while n > 0:
            for _ in range(n):  # move horizontally
                j += direction
                matrix[i][j] = number
                number += 1
            for _ in range(n-1):  # move vertically
                i += direction
                matrix[i][j] = number
                number += 1
            n -= 1
            direction *= -1  # flip direction
        return matrix

s = Solution()
n = 3
result = s.generateMatrix(n)
print(result)

"""

"""
