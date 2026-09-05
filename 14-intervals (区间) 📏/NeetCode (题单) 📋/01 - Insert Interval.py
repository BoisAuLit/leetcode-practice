from bisect import bisect_left, bisect_right
from typing import List


class Solution:
    def insert(
        self,
        intervals: List[List[int]],
        newInterval: List[int]
    ) -> List[List[int]]:

        start, end = newInterval

        # First interval whose END >= new start
        left = bisect_left(
            intervals,
            start,
            key=lambda interval: interval[1]
        )

        # First interval whose START > new end
        right = bisect_right(
            intervals,
            end,
            key=lambda interval: interval[0]
        )

        # No overlap
        if left == right:
            return (
                intervals[:left]
                + [newInterval]
                + intervals[left:]
            )

        # Merge every interval in intervals[left:right]
        merged = [
            min(start, intervals[left][0]),
            max(end, intervals[right - 1][1])
        ]

        return (
            intervals[:left]
            + [merged]
            + intervals[right:]
        )
s = Solution()
intervals = [[0, 1], [3, 4], [5, 7], [111, 113]]
newInterval = [2, 16]

result = s.insert(intervals, newInterval)
print(result)
