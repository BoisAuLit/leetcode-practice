from typing import List


class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        mapping = {}
        for index, num in enumerate(nums):
            if num not in mapping:
                mapping[num] = index
            else:
                if index - mapping[num] <= k:
                    return True
                else:
                    mapping[num] = index

        return False


"""
Runtime
- 519ms
- Beats 90.72%

Memory
29.69mb
- Beats 49.06%
"""
