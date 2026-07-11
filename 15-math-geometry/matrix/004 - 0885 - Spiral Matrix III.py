from typing import List

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def inRange(self, x: int, y: int, m: int, n: int) -> bool:
        return 0 <= x < m and 0 <= y < n

    def spiralMatrixIII(
        self, rows: int, cols: int, rStart: int, cStart: int
    ) -> List[List[int]]:
        number = 1
        steps = 1
        direction = 1  # Start off going right
        x, y = rStart, cStart
        m, n = rows, cols
        result = []
        while number <= rows * cols:
            for _ in range(steps):  # Moving horizontally
                if self.inRange(x, y, m, n):
                    number += 1
                    result.append([x, y])
                
                y += direction
            for _ in range(steps):  # Moving vertically
                if self.inRange(x, y, m, n):
                    number += 1
                    result.append([x, y])
                x += direction
            steps += 1
            direction *= -1
        return result


s = Solution()

rows = 5
cols = 6
rStart = 1
cStart = 4
result = s.spiralMatrixIII(rows, cols, rStart, cStart)
print(result)

"""

"""
