from typing import List

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def isReflected(self, points: List[List[int]]) -> bool:
        points = {(x, y) for x, y in points}
        avg = sum(x for x, _ in points) / len(points)
        return all((2 * avg - x, y) in points for x, y in points)


s = Solution()
input_ = [[1, 1], [-1, 1]]  # True
# input_ = [[1, 1], [-1, -1]]  # False
# input_ = [[0, 0], [1, 0], [3, 0]]  # False
result = s.isReflected(input_)
print(result)
