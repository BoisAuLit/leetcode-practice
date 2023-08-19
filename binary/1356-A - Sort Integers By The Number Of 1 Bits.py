from typing import List

"""
Time complexity: O(nlogn)
Space complexity: O(n)
"""


class Solution:
    def sortByBits(self, arr: List[int]) -> List[int]:
        arr_sorted = sorted(arr)
        count_mapping = [[bin(num).count("1"), num] for num in arr_sorted]
        count_mapping.sort(key=lambda x: x[0])
        return [x[1] for x in count_mapping]

s = Solution()
input_ = [1, 2, 3, 6, 7, 9, 11, 15, 1024]
result = s.sortByBits(input_)
print(result)

"""
Runtime
- 78 ms
- Beats 76.76%

Memory
- 16.5 MB
- Beats 31.38%
"""
