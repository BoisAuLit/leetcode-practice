from typing import List


"""
Time complexity: O(n+m)
Space complexity: O(m)
"""

# First attempt
# class Solution:
#     def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
#         nums1_copy = nums1.copy()
#         p = p1 = p2 = 0
#         while p <= len(nums1) - 1:
#             if p1 == m:
#                 while p != m + n:
#                     nums1[p] = nums2[p2]
#                     p += 1
#                     p2 += 1
#                 return
#             if p2 == n:
#                 while p != m + n:
#                     nums1[p] = nums1_copy[p1]
#                     p += 1
#                     p1 += 1
#                 return

#             if nums1_copy[p1] < nums2[p2]:
#                 nums1[p] = nums1_copy[p1]
#                 p1 += 1
#             else:
#                 nums1[p] = nums2[p2]
#                 p2 += 1
#             p += 1


# Official solution from Leetcode
class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        # Make a copy of the first m elements of nums1.
        nums1_copy = nums1[:m]

        # Read pointers for nums1Copy and nums2 respectively.
        p1 = 0
        p2 = 0

        # Compare elements from nums1Copy and nums2 and write the smallest to nums1.
        for p in range(n + m):
            # We also need to ensure that p1 and p2 aren't over the boundaries
            # of their respective arrays.
            if p2 >= n or (p1 < m and nums1_copy[p1] <= nums2[p2]):
                nums1[p] = nums1_copy[p1]
                p1 += 1
            else:
                nums1[p] = nums2[p2]
                p2 += 1


s = Solution()
nums1 = [1, 2, 3, 0, 0, 0]
m = 3
nums2 = [2, 5, 6]
n = 3
s.merge(nums1, m, nums2, n)
print(nums1)

"""
Runtime
- 59 ms
- Beats 19.77%

Memory
- 16.4 MB
- Beats 46.16%
"""
