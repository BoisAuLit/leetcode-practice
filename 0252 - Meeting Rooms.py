from typing import List


class Solution:
    def overlap(self, i1: List[int], i2: List[int]) -> bool:
        return i2[0] < i1[1]

    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:
        intervals = sorted(intervals, key=lambda x: x[0])
        if len(intervals) < 1:
            return True
        for i in range(0, len(intervals) - 1):
            if self.overlap(intervals[i], intervals[i + 1]):
                return False
        return True


s = Solution()
# Expecting False
# intervals = [[0, 30], [5, 10], [15, 20]]

# Expecting True
# intervals = [[7,10],[2,4]]

# Expecting True
intervals = [[13, 15], [1, 13]]

result = s.canAttendMeetings(intervals)
print(result)

"""

"""
