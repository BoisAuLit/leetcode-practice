"""LC-0162 - Find Peak Element

⚠️ 自动合并失败 (12 - 0162 - Find Peak Element.py: 语法错误 invalid syntax (<unknown>, line 20)); 下面是各解法文件的原样拼接, 需要手工整理
"""

# ============================================================================
# 原文件: 12 - 0162 - Find Peak Element.py
# ============================================================================
from typing import List

"""
Time complexity: O()
Space complexity: O()
"""
class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        left =0
        right = len(nums)-1
        while left < right:
            mid = left + (right - left ) //2
            if nums[mid] > nums[mid+1]: # True Condition # Dec function # go left # Find First True i.e first elem where this condition will be True
                right = mid # include mid # mid is potential solution 
            else:
                left = mid +1
        return left

s = Solution()
input_ = 
result = s.XXXXXXXXXXXXX(input_)
print(result)


# ============================================================================
# 原文件: 03 - 0162 - A - Find Peak Element - A - BST.py
# ============================================================================
"""
This question is using template 2
of the binary search tutorial
"""

class Solution:
    def findPeakElement(self, nums):
        for i in range(len(nums) - 1):
            if nums[i] > nums[i + 1]:
                return i
        return len(nums) - 1


# ============================================================================
# 原文件: 03 - 0162 - B - Find Peak Element - A - Linear Scan.py
# ============================================================================
"""
This question is using template 2
of the binary search tutorial
"""

class Solution:
    def findPeakElement(self, nums):
        for i in range(len(nums) - 1):
            if nums[i] > nums[i + 1]:
                return i
        return len(nums) - 1
