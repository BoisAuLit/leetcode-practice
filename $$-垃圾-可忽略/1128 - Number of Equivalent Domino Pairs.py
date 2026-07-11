from typing import List
from collections import defaultdict


class Solution:
    def numEquivDominoPairs(self, dominoes: List[List[int]]) -> int:
        counter = defaultdict(lambda: 0)
        for pair in dominoes:
            if pair[0] > pair[1]:
                pair[0], pair[1] = pair[1], pair[0]
            counter[(pair[0], pair[1])] += 1
        return sum(x * (x - 1) // 2 for x in counter.values())


s = Solution()
input_ = [[1, 2], [1, 2], [1, 1], [1, 2], [2, 2]]
result = s.numEquivDominoPairs(input_)
print(result)

"""

"""
