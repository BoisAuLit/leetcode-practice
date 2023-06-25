from typing import List

"""
Time complexity: O(n)
Space complexity: O(n)
"""


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        set_ = set()
        for num in nums:
            if num in set_:
                return True
            set_.add(num)
        return False


s = Solution()
# input_ = [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]  # Expecting True
input_ = [1, 2, 3, 4]  # Expecting False
result = s.containsDuplicate(input_)
print(result)


"""
Runtime
- 539 ms
- Beats 82.48%

Memory
- 30.9 MB
- Beats 68.27%
"""
