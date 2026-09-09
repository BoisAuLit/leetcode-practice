from typing import List
import heapq


class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Solution:
    def minMeetingRooms(self, intervals: List[Interval]) -> int:
        intervals.sort(key=lambda interval: interval.start)

        minHeap = []
        rooms = 0

        for interval in intervals:
            # Remove all meetings that already ended
            while minHeap and minHeap[0] <= interval.start:
                heapq.heappop(minHeap)

            # Current meeting takes one room
            heapq.heappush(minHeap, interval.end)

            rooms = max(rooms, len(minHeap))

        return rooms


s = Solution()
input_ = [Interval(0, 40), Interval(5, 10), Interval(15, 20)]
result = s.minMeetingRooms(input_)
print(result)
