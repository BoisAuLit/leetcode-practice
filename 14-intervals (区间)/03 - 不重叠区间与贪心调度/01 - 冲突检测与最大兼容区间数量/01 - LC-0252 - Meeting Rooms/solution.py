class Solution:
    def canAttendMeetings(self, intervals: list[list[int]]) -> bool:
        n = len(intervals)

        if n <= 1:
            return True
        intervals.sort()
        for i in range(1, n):
            if intervals[i-1][1] > intervals[i][0]:
                return False
        return True

