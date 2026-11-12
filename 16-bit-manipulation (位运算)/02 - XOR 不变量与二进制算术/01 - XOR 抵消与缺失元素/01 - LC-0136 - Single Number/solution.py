from typing import List


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        res = 0
        for num in nums:
            res ^= num

        return res


"""
旧解法（2023-07-22，Counter，O(n) 额外空间）：

    from collections import Counter

    class Solution:
        def singleNumber(self, nums: List[int]) -> int:
            return Counter(nums).most_common()[-1][0]

Runtime 144ms  Beats 64.00%
Memory 19.24mb Beats 20.73%
"""
