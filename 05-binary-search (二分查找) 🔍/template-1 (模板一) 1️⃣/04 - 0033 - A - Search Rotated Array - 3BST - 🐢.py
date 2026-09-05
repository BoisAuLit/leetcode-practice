from typing import List

"""
For this question, we do
- At least 2 binary searches
- At most 3 binary searches

Which is quite slow.
"""


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        n = len(nums)
        left, right = 0, n - 1

        """
        Find the index of the pivot element (the smallest element)

        In the end, left will be the pivot.
        For example if the input array is [11, 12, 13, 1, 2, 3]
        Then left will equal to 3 (index of element 1)
        """
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] > nums[-1]:
                left = mid + 1
            else:
                right = mid - 1

        # Binary search over an inclusive range [p1 ~ p2]
        def binarySearch(p1: int, p2: int, target: int) -> int:
            while p1 <= p2:
                mid = (p1 + p2) // 2
                if nums[mid] == target:
                    return mid
                elif nums[mid] > target:
                    p2 = mid - 1
                else:
                    p1 = mid + 1
            return -1

        # Binary search over elements on the pivot element's left
        answer = binarySearch(0, left - 1, target)
        if answer != -1:
            return answer

        # Binary search over elements on the pivot element's right
        return binarySearch(left, n - 1, target)


nums = [4, 5, 6, 7, 0, 1, 2]
target = 0
s = Solution()
result = s.search(nums, target)
print(result)

# nums = [7, 8, 1, 2, 3, 4, 5, 6]
# target = 2
# s = Solution()
# result = s.search(nums, target)
# print(result)
