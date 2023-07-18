from typing import List
"""
Time complexity: O(n)
Space complexity: O(1)
"""


class Solution:
    def checkStraightLine(self, coordinates: List[List[int]]) -> bool:
        x1, y1 = coordinates[0]
        x2, y2 = coordinates[1]
        if x1 == x2:
            return all(x == x1 for x in (pair[0] for pair in coordinates))
        slope = (y1 - y2) / (x1 - x2)
        intercept = y1 - slope * x1
        return all((y == slope * x + intercept) for (x, y) in coordinates)

"""
Runtime
- 82ms
- Beats 33.54%

Memory
- 16.81mb
- Beats 58.57%
"""
