from typing import List

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        pointer = 0
        for n in nums:
            if n != val:
                nums[pointer] = n
                pointer += 1
        return pointer


s = Solution()
input_ = [0, 1, 2, 2, 3, 0, 4, 2]
result = s.removeElement(input_, 2)
print(result)
print(input_)

"""
Runtime
- 51 ms
- Beats 39.66%

Memory
- 16.3 MB
- Beats 60.51%
"""
