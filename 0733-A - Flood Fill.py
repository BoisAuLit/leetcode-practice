from typing import List

"""
Time complexity: O(N)
Space complexity: O(N)
"""


class Solution:
    def __init__(self):
        self.filled = set()

    def floodFill(
        self, image: List[List[int]], sr: int, sc: int, color: int
    ) -> List[List[int]]:
        valid_points = []
        for x, y in [(sr - 1, sc), (sr + 1, sc), (sr, sc + 1), (sr, sc - 1)]:
            if (
                0 <= x < len(image)
                and 0 <= y < len(image[0])
                and (x, y) not in self.filled
                and image[x][y] == image[sr][sc]
            ):
                valid_points.append((x, y))
        self.filled.add((sr, sc))
        self.filled.update(valid_points)
        image[sr][sc] = color
        for x, y in valid_points:
            self.floodFill(image, x, y, color)
        return image


s = Solution()

# Expecting [[2, 2, 2], [2, 2, 0], [2, 0, 1]]
image = [[1, 1, 1], [1, 1, 0], [1, 0, 1]]
sr = 1
sc = 1
color = 2

result = s.floodFill(image, sr, sc, color)

print(result)

"""
Runtime
- 89ms
- Beats 67.09%

Memory
16.54mb
- Beats 47.51%
"""
