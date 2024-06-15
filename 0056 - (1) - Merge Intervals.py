from typing import List

"""
Time complexity: O(NlogN)
Space complexity: O(logN) or O(N)

- If we can sort intervals in place,
we do not need more than constant additional space,
although the sorting itself takes O(logn) space.

- Otherwise, we must allocate linear space to store
a copy of intervals and sort that.
"""


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        result = []
        intervals.sort(key=lambda x: x[0])
        curr = intervals[0]
        for i in range(1, len(intervals)):
            if curr[1] >= intervals[i][0]:
                curr[1] = max(curr[1], intervals[i][1])
            else:
                result.append(curr)
                curr = intervals[i]
        result.append(curr)
        return result


s = Solution()

# Expecting [[1,6],[8,10],[15,18]]
input_ = [[1, 3], [2, 6], [8, 10], [15, 18]]

# Expecting [[1,5]]
input_ = [[1, 4], [4, 5]]

# Expecting [[1,5]]
input_ = [[1, 5]]

# Expecting [[0,4]]
input_ = [[1, 4], [0, 4]]

# Expecting [[1,4]]
input_ = [[1, 4], [2, 3]]


result = s.merge(input_)
print(result)

"""

"""
