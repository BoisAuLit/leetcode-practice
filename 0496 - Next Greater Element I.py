from typing import List

"""
Time complexity: O(n)
Space complexity: O(n)
"""

class Solution:
    def nextGreaterElement(
        self, nums1: List[int], nums2: List[int]
    ) -> List[int]:
        stack = []
        mapping = {}
        for num in nums2:
            while stack and num > stack[-1]:
                mapping[stack.pop()] = num
            stack.append(num)
        while stack:
            mapping[stack.pop()] = -1
        result = []
        for num in nums1:
            result.append(mapping[num])
        return result
                

s = Solution()
# Expecting [-1,3,-1]
nums1 = [4, 1, 2]
nums2 = [1, 3, 4, 2]
result = s.nextGreaterElement(nums1, nums2)

print(result)

"""
Runtime
- 59ms
- Beats 73.91%

Memory
16.68mb
- Beats 37.72%
"""
