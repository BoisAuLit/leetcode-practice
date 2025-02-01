from typing import List
import bisect

"""
File path: "./assets/0057_Insert_Interval.png"

Difficulty: Medium
"""


class Solution:
    def insert(
        self, intervals: List[List[int]], newInterval: List[int]
    ) -> List[List[int]]:
        start, end = newInterval

        left_index = bisect.bisect(
            intervals, newInterval[0], key=lambda x: x[0]
        )
        right_index = bisect.bisect(
            intervals, newInterval[1], key=lambda x: x[0]
        )

        # if left_index == right_index:
        #     right_index += 1

        print("left index:", left_index)
        print("right index:", right_index)

        left_start, left_end = intervals[left_index]
        right_start, right_end = intervals[right_index + 1]

        print("left_start", left_start)
        print("left_end", left_end)
        print("right_start", right_start)
        print("right_end", right_end)

        middle = []

        if left_end < start:
            if end < right_start:
                print("Here arrived 111")
                middle = [
                    intervals[left_index],
                    newInterval,
                    intervals[right_index],
                ]
            else:
                print("Here arrived 222")
                middle = [intervals[left_index], [start, right_end]]
        else:
            if end < right_start:
                print("Here arrived 333")
                middle = [[left_start, end], intervals[right_index]]
            else:
                middle = [[left_end, right_end]]
                print("Here arrived 444")

        return intervals[:left_index] + middle + intervals[right_index + 1 :]


s = Solution()

# Test case 1: Expecting [[1,2],[3,10],[12,16]]
input_1 = [[1, 2], [3, 5], [6, 7], [8, 10], [78, 99]]
input_2 = [11, 17]


result = s.insert(input_1, input_2)
print(result)
