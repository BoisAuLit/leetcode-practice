# https://leetcode.com/problems/least-number-of-unique-integers-after-k-removals/

# https://leetcode.com/problems/least-number-of-unique-integers-after-k-removals/

from typing import List
from collections import Counter


class Solution:
    def findLeastNumOfUniqueInts(self, arr: List[int], k: int) -> int:
        counter = Counter(arr)
        most_common = counter.most_common()
        acc = 0
        for i in range(len(most_common)-1, -1, -1):
            acc += most_common[i][1]
            if acc == k:
                return i
            elif acc > k:
                return i+1

# Test case 1: Expecting 2
s = Solution()
arr = [4, 3, 1, 1, 3, 3, 2]
k = 3
result = s.findLeastNumOfUniqueInts(arr, k)
print(result)

# Test case 2: Expecting 4
arr = [5, 5, 4]
k = 1
result = s.findLeastNumOfUniqueInts(arr, k)
print(result)
