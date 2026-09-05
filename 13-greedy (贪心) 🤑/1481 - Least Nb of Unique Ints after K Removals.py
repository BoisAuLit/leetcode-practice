from typing import List
from collections import Counter


from typing import List

"""
Time complexity: O()
Space complexity: O()
"""
class Solution:
    def findLeastNumOfUniqueInts(self, arr: List[int], k: int) -> int:
        counter = Counter(arr)
        toRemove = 0
        for _, count in counter.most_common()[::-1]:
            k -= count
            toRemove += 1
            if k == 0:
                break
            if k < 0:
                toRemove -= 1
                break
        return len(counter) - toRemove


s = Solution()

# Expecting 2
arr = [4, 3, 1, 1, 3, 3, 2]
k = 3

result = s.findLeastNumOfUniqueInts(arr, k)
print(result)

"""

"""
