from typing import List


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort()

        res = []
        start, end = intervals[0]

        for nextStart, nextEnd in intervals[1:]:
            # Overlap → extend current interval
            if nextStart <= end:
                end = max(end, nextEnd)

            # No overlap → current interval is finished
            else:
                res.append([start, end])

                start, end = nextStart, nextEnd

        # Don't forget the last interval
        res.append([start, end])

        return res


s = Solution()
input_ = [[2, 3], [4, 5], [6, 7], [8, 9], [1, 10]]
result = s.merge(input_)
print(result)
