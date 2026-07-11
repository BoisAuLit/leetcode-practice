from typing import List
import heapq


class Solution:

    """
    min_heap stores on the top the earliest end time of previous intervals

    In each loop, we compare current start to the earliest end time,
    while current start >= earliest end time of previous intervals,
    we keep popping out the top element
    """
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        intervals.sort()
        min_heap = []
        rooms = 1
        for start, end in intervals:
            while min_heap and start >= min_heap[0]:
                heapq.heappop(min_heap)
            heapq.heappush(min_heap, end)
            rooms = max(rooms, len(min_heap))
        return rooms


s = Solution()
intervals = [[13, 15], [1, 13]]
result = s.minMeetingRooms(intervals)
print(result)
