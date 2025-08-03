from typing import List
import math


class Solution:
    def minimumAbsDifference(self, arr: List[int]) -> List[List[int]]:
        arr.sort()
        min_diff = math.inf
        result = []
        for i in range(len(arr) - 1):
            diff = arr[i+1] - arr[i]
            if diff < min_diff:
                result = [[arr[i], arr[i+1]]]
                min_diff = diff
            elif diff == min_diff:
                result.append([arr[i], arr[i+1]])
        return result

s = Solution()
input_ = [3,8,-10,23,19,-4,-14,27]
result = s.minimumAbsDifference(input_)
print(result)
