from typing import List
import bisect

"""
Time complexity: O(N)
Space complexity: O(1)
"""


class Solution:
    def insert(
        self, intervals: List[List[int]], newInterval: List[int]
    ) -> List[List[int]]:
        n = len(intervals)
        i = 0
        res = []

        # Case 1: No overlapping before merging intervals
        while i < n and intervals[i][1] < newInterval[0]:
            res.append(intervals[i])
            i += 1

        # Case 2: Overlapping and merging intervals
        while i < n and newInterval[1] >= intervals[i][0]:
            newInterval[0] = min(newInterval[0], intervals[i][0])
            newInterval[1] = max(newInterval[1], intervals[i][1])
            i += 1
        res.append(newInterval)

        # Case 3: No overlapping after merging newInterval
        while i < n:
            res.append(intervals[i])
            i += 1

        return res


s = Solution()
# Test case 1: Expecting [[1, 2], [3, 5], [6, 7], [8, 10], [11, 17], [78, 99]]
input_1 = [[1, 2], [3, 5], [6, 7], [8, 10], [78, 99]]
input_2 = [11, 17]
result = s.insert(input_1, input_2)
print(result)

# Test case 2 [[1, 5], [6, 9]]
# input_1 = [[1, 3], [6, 9]]
# input_2 = [2, 5]

# result = s.insert(input_1, input_2)
# print(result)
