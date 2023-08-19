from typing import List

"""
Time complexity: O(k²)
Space complexity: O(k)
"""


class Solution:
    def getRow(self, rowIndex: int) -> List[int]:
        lastRow = []
        for i in range(1, rowIndex + 2):
            row = [None] * i
            row[0] = row[-1] = 1
            for j in range(1, i - 1):
                row[j] = lastRow[j] + lastRow[j - 1]
            lastRow = row
        return lastRow


s = Solution()
rowIndex = 3
result = s.getRow(rowIndex)
print(result)
