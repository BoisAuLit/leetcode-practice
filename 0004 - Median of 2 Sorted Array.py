from typing import List

"""
Time complexity: O(m+n)
Space complexity: O(1)
"""


class Solution:
    def findMedianSortedArrays(self, A: List[int], B: List[int]) -> float:
        m, n = len(A), len(B)
        length = m + n

        def solve(k, a_start, a_end, b_start, b_end):
            # If the segment of on array is empty, it means we have passed all
            # its element, just return the corresponding element in the other array.
            if a_start > a_end:
                return B[k - a_start]
            if b_start > b_end:
                return A[k - b_start]

            # Get the middle indexes and middle values of A and B.
            a_index, b_index = (a_start + a_end) // 2, (b_start + b_end) // 2
            a_value, b_value = A[a_index], B[b_index]

            # If k is in the right half of A + B, remove the smaller left half.
            if a_index + b_index < k:
                if a_value > b_value:
                    return solve(k, a_start, a_end, b_index + 1, b_end)
                else:
                    return solve(k, a_index + 1, a_end, b_start, b_end)
            # Otherwise, remove the larger right half.
            else:
                if a_value > b_value:
                    return solve(k, a_start, a_index - 1, b_start, b_end)
                else:
                    return solve(k, a_start, a_end, b_start, b_index - 1)

        if length % 2:
            return solve(length // 2, 0, m - 1, 0, n - 1)
        else:
            return (
                solve(length // 2 - 1, 0, m - 1, 0, n - 1)
                + solve(length // 2, 0, m - 1, 0, n - 1)
            ) / 2


class Solution_Brute_Force:
    def findMedianSortedArrays(
        self, nums1: List[int], nums2: List[int]
    ) -> float:
        m = len(nums1)
        n = len(nums2)
        p1 = 0
        p2 = 0
        index = 0

        prev = -1
        target_index = (m + n) // 2
        isEven = (m + n) % 2 == 0
        while p1 < m and p2 < n:
            if nums1[p1] <= nums2[p2]:
                curr = nums1[p1]
                p1 += 1
            else:
                curr = nums2[p2]
                p2 += 1
            if index == target_index:
                return (curr + prev) / 2 if isEven else curr
            index += 1
            prev = curr

        if index == target_index:
            curr = nums2[p2] if p1 == m else nums1[p1]
            return (curr + prev) / 2 if isEven else curr
        if p1 == m:
            p2 += target_index - index
            return (nums2[p2 - 1] + nums2[p2]) / 2 if isEven else nums2[p2]
        if p2 == n:
            p1 += target_index - index
            return (nums1[p1 - 1] + nums1[p1]) / 2 if isEven else nums1[p1]


s = Solution()

# Expecting 2
nums1 = [1, 3]
nums2 = [2]

# Expecting 2.5
# nums1 = [1, 2]
# nums2 = [3, 4]
result = s.findMedianSortedArrays(nums1, nums2)
print(result)
