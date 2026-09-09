from typing import List


class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        # Greedy: keep intervals that end earliest
        intervals.sort(key=lambda x: x[1])

        prevEnd = intervals[0][1]
        removed = 0

        for start, end in intervals[1:]:
            if start < prevEnd:
                # Overlap:
                # remove current interval because the previous one
                # ends no later than it
                removed += 1
            else:
                # No overlap: keep it
                prevEnd = end

        return removed
