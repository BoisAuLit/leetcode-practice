# https://leetcode.com/problems/insert-interval/
# https://neetcode.io/problems/insert-new-interval/question?list=neetcode150

from typing import List
from bisect import bisect_left, bisect_right

class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        left, right = newInterval
        p1 = bisect_left(intervals, left, key=lambda x: x[1])
        p2 = bisect_right(intervals, right, key=lambda x: x[0])
        if p1 == p2:
            return intervals[:p1] + [newInterval] + intervals[p2:]
        newInterval = [min(left, intervals[p1][0]), max(right, intervals[p2 - 1][1])]
        return intervals[:p1] + [newInterval] + intervals[p2:]


s = Solution()
intervals = [[0, 1], [3, 4], [5, 7], [111, 113]]
newInterval = [2, 16]

result = s.insert(intervals, newInterval)
print(result)
