from typing import List


"""
Time complexity: O(N)
Space complexity: O(1)

How it works?
Define a standby array which represents possible candidate array
that may be added to the result array.

In every loop we compare the current inner interval with the "standby"
interval
- If there's an overlap, then merge the current interval and the "standby" interval
    - and re-assign the "standby" interval with the newly calculated interval above
- If there's no overlap, then add the "standby" interval to the result list
"""


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        # ! Sort by interval start
        intervals.sort(key=lambda x: x[0])
        standby = intervals[0]
        result = []
        for i in range(1, len(intervals)):
            if intervals[i][0] > standby[1]:
                result.append(standby)
                standby = intervals[i]
            else:
                standby = [
                    min(standby[0], intervals[i][0]),
                    max(standby[1], intervals[i][1]),
                ]
        result.append(standby)
        return result


s = Solution()

# Test case 1: Expecting [[1,6],[8,10],[15,18]]
intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
result = s.merge(intervals)
print(result)

# Test case 2: Expecting [[1,5]]
intervals = [[1, 4], [4, 5]]
result = s.merge(intervals)
print(result)
