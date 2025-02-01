from typing import List


class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        return sorted(
            points, key=lambda point: point[0] * point[0] + point[1] * point[1]
        )[:k]


s = Solution()

# Test case 1: Expecting [[3,3],[-2,4]]
points = [[3, 3], [5, -1], [-2, 4]]
k = 2

result = s.kClosest(points, 2)
print(result)
