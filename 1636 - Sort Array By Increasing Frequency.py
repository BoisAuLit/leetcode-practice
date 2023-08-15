from typing import List
from collections import Counter
import bisect

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def frequencySort(self, nums: List[int]) -> List[int]:
        frequency_mapping = Counter(nums)
        mapping = {}
        frequencies = []
        result = []
        for number, count in frequency_mapping.items():
            if count not in mapping:
                mapping[count] = [number]
                frequencies.append(count)
            else:
                bisect.insort(mapping[count], number)
        frequencies.sort()
        for count in frequencies:
            sorted_list = mapping[count]
            for i in range(len(sorted_list) - 1, -1, -1):
                result.extend([sorted_list[i]] * count)
        return result


s = Solution()

# Expecting [1,3,3,2,2]
# input_ = [2, 3, 1, 3, 2]

# Expecting [5,-1,4,4,-6,-6,1,1,1]
input_ = [-1, 1, -6, 4, 5, -6, 1, 4, 1]
result = s.frequencySort(input_)
print(result)

"""
Runtime
- 53ms
- Beats 87.98%

Memory
16.44mb
- Beats 30.81%
"""
