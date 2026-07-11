from typing import List

"""
For this question, we do
- 2 binary searches

Which is quicker than approach A.
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

        def shiftedBinarySearch(pivot: int, target: int) -> int:
            """
            Shift elements in circular manner, with the pivot element at index 0.
            Then perform a regular binary search

            p1 is left pointer
            p2 is right pointer
            m is middle pointer
            """
            shift = n - pivot
            p1, p2 = (pivot + shift) % n, (pivot - 1 + shift) % n

            while p1 <= p2:
                m = (p1 + p2) // 2
                if nums[(m - shift) % n] == target:
                    return (m - shift) % n
                elif nums[(m - shift) % n] > target:
                    p2 = m - 1
                else:
                    p1 = m + 1
            return -1

        return shiftedBinarySearch(left, target)


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
