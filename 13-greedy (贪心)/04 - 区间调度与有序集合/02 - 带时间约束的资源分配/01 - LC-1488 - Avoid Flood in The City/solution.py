from typing import List
from collections import defaultdict, deque
import heapq


class Solution:
    def avoidFlood(self, rains: List[int]) -> List[int]:
        right = defaultdict(deque)
        for index, rain in enumerate(rains):
            if rain > 0:
                right[rain].append(index)

        res = []
        min_heap = []
        full_lakes = set()
        for index, rain in enumerate(rains):
            if rain > 0:
                # It rained today, we need to decide wether to continue or return empty array
                if rain in full_lakes:
                    return []

                res.append(-1)
                right[rain].popleft()

                # We only add lake to full_lakes if they re-occurr later.
                # We don't care about lakes that don't re-occurr later
                if right[rain]:
                    full_lakes.add(rain)
                    heapq.heappush(min_heap, (right[rain][0], rain))
            else:
                # It didn't rain today, we need to optimally empty a good lake to avoid flood in the future
                if min_heap:
                    _, lake = heapq.heappop(min_heap)
                    res.append(lake)
                    full_lakes.remove(lake)
                else:
                    res.append(1)
        return res


# # Test case 1: Expecting [-1,-1,2,1,-1,-1]
# s = Solution()
# rains = [1, 2, 0, 0, 2, 1]
# result = s.avoidFlood(rains)
# print(result)

# # Test case 2: Expecting [-1,69,1,1,-1]
# s = Solution()
# rains = [69, 0, 0, 0, 69]
# result = s.avoidFlood(rains)
# print(result)

# # Test case 3: Expecting []
# s = Solution()
# rains = [0, 1, 1]
# result = s.avoidFlood(rains)
# print(result)

# Test case 4: Expecting []
s = Solution()
rains = [1, 1, 0, 0]
result = s.avoidFlood(rains)
print(result)
