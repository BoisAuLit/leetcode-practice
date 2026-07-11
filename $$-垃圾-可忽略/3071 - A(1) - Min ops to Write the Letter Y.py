from typing import Dict, List


class Solution:
    def minimumOperationsToWriteY(self, grid: List[List[int]]) -> int:
        onY = {x: 0 for x in range(3)}
        notOnY = {x: 0 for x in range(3)}
        n = len(grid)
        half = n // 2
        y_points = set([(half, half)])
        # Add points to Y
        for i in range(half):
            y_points.update([(i, i), (i, n - i - 1), (half + i + 1, half)])

        for i in range(n):
            for j in range(n):
                if (i, j) in y_points:
                    onY[grid[i][j]] += 1
                else:
                    notOnY[grid[i][j]] += 1

        def get_effort(counter: Dict[int, int], target: int) -> int:
            return sum(
                count for number, count in counter.items() if number != target
            )

        min_ops = float("inf")
        for i in range(3):
            for j in range(3):
                if i != j:
                    effort = get_effort(onY, i) + get_effort(notOnY, j)
                    min_ops = min(min_ops, effort)
        return min_ops


s = Solution()
grid = [
    [0, 1, 0, 1, 0],
    [2, 1, 0, 1, 2],
    [2, 2, 2, 0, 1],
    [2, 2, 2, 2, 2],
    [2, 1, 2, 2, 2],
]
result = s.minimumOperationsToWriteY(grid)
print(result)
