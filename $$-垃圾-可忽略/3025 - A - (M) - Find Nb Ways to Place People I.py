from typing import List


class Solution:
    def numberOfPairs(self, points: List[List[int]]) -> int:
        # Sort points by x ascending, and for ties by y descending
        points.sort(key=lambda p: (p[0], -p[1]))

        n = len(points)
        ans = 0

        # For each left point
        for i in range(n - 1):
            pi2 = points[i][1]
            min_h = float("-inf")

            # Scan right-side points
            for j in range(i + 1, n):
                if points[j][1] > min_h and points[j][1] <= pi2:
                    ans += 1
                    min_h = points[j][1]

        return ans


# # Test case 1: Expecting 0
# s = Solution()
# points = [[1, 1], [2, 2], [3, 3]]
# result = s.numberOfPairs(points)
# print(result)

# # Test case 2: Expecting 2
# s = Solution()
# points = [[6, 2], [4, 4], [2, 6]]
# result = s.numberOfPairs(points)
# print(result)

# Test case 3: Expecting 2
s = Solution()
points = [[3, 1], [1, 3], [1, 1]]
result = s.numberOfPairs(points)
print(result)
