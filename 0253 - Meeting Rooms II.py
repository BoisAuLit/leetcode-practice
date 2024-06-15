import heapq
from typing import List

"""
Time complexity: O(NlogN)
Space complexity: O(N)
"""

class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:

        used_rooms = 0

        start_timings = sorted([i[0] for i in intervals])
        end_timings = sorted(i[1] for i in intervals)
        L = len(intervals)

        end_pointer = 0
        start_pointer = 0

        while start_pointer < L:
            if start_timings[start_pointer] >= end_timings[end_pointer]:
                used_rooms -= 1
                end_pointer += 1
            used_rooms += 1    
            start_pointer += 1   

        return used_rooms


class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        # The heap initialization
        free_rooms = []

        intervals.sort(key=lambda x: x[0])

        heapq.heappush(free_rooms, intervals[0][1])

        for i in intervals[1:]:
            if free_rooms[0] <= i[0]:
                heapq.heappop(free_rooms)

            heapq.heappush(free_rooms, i[1])

        return len(free_rooms)


s = Solution()
intervals = [[0, 30], [5, 10], [15, 20]]
result = s.minMeetingRooms(intervals)
print(result)
