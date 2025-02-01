from typing import List


class Solution:
    def overlap(self, i1: List[int], i2: List[int]):
        return i2[0] <= i1[1]

    def merge_2_intervals(self, i1: List[int], i2: List[int]):
        return [i1[0], max(i1[1], i2[1])]

    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort()
        result = []
        for interval in intervals:
            if len(result) == 0:
                result.append(interval)
                continue
            if self.overlap(result[-1], interval):
                result[-1] = self.merge_2_intervals(result[-1], interval)
            else:
                result.append(interval)
        return result


s = Solution()

# Test case 1: Expecting [[1,6],[8,10],[15,18]]
ntervals = [[1, 3], [2, 6], [8, 10], [15, 18]]

# Test case 2: Expecting [[1,4]]
ntervals = [[1,4],[2,3]]

result = s.merge(ntervals)


print(result)
