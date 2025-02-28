from typing import List
import heapq
# from collections import Counter


class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        if len(intervals) == 0:
            return 0

        intervals.sort()
        rooms = [intervals[0][1]]
        for start, end in intervals[1:]:
            if rooms[0] <= start:
                heapq.heappop(rooms)
            heapq.heappush(rooms, end)
        return len(rooms)


# # ! Naive approach
# class Solution:
#     def minMeetingRooms(self, intervals: List[List[int]]) -> int:
#         births = [x[0] for x in intervals]
#         deaths = [x[1] for x in intervals]

#         b_count = Counter(births)
#         d_count = Counter(deaths)

#         alive = 0
#         max_alive = -1
#         for i in range(min(births), max(deaths)+1):
#             if i in b_count:
#                 alive += b_count[i]
#             if i in d_count:
#                 alive -= d_count[i]
#             max_alive = max(max_alive, alive)
#         return max_alive

s = Solution()


# Test case 1: Expecting 2
# intervals = [[0,30],[5,10],[15,20]]

# Tes case 2: Expecting 1
intervals = [[7, 10], [2, 4]]

result = s.minMeetingRooms(intervals)
print(result)
