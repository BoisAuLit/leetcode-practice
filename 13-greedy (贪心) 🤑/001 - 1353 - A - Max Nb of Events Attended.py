from typing import List
import heapq


class Solution:
    def maxEvents(self, events: List[List[int]]) -> int:
        n = len(events)
        max_day = max(event[1] for event in events)
        events.sort()
        min_heap = []
        ans, j = 0, 0
        for day in range(1, max_day + 1):
            # ! Add all the events whose start date <= today to the min heap
            while j < n and events[j][0] <= day:
                heapq.heappush(min_heap, events[j][1])
                j += 1
            
            # !Remove all the events in the past (e)
            while min_heap and min_heap[0] < day:
                heapq.heappop(min_heap)
            # ! Greedily pick the event whose end date is the earliest
            if min_heap:
                heapq.heappop(min_heap)
                # ! Every time we participate in an event, we
                # ! increase the answer by one
                ans += 1

        return ans
