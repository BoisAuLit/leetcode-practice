"""LC-0033 - Search in Rotated Sorted Array

合并自 4 个解法文件:
  1. 08 - 0033 - (1) - Search in Rotated Sorted Array.py
  2. 04 - 0033 - A - Search Rotated Array - 3BST - 🐢.py
  3. 04 - 0033 - B - Search Rotated Array - 2BST - 🚀.py
  4. 04 - 0033 - C - Search Rotated Array - 1BST - 🚀🚀🚀.py
"""

from typing import List


# ============================================================================
# Solution 1: Search_in_Rotated_Sorted_Array    (原文件: 08 - 0033 - (1) - Search in Rotated Sorted Array.py)
# ============================================================================

class Solution_1_Search_in_Rotated_Sorted_Array:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid

            # Check if left half is sorted
            if nums[left] <= nums[mid]:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            # Otherwise, right half is sorted
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return -1

# ============================================================================
# Solution 2: A    (原文件: 04 - 0033 - A - Search Rotated Array - 3BST - 🐢.py)
# ============================================================================

# For this question, we do
# - At least 2 binary searches
# - At most 3 binary searches
#
# Which is quite slow.

nums_2 = [4, 5, 6, 7, 0, 1, 2]

target_2 = 0

class Solution_2_A:
    def search(self, nums_2: List[int], target_2: int) -> int:
        n = len(nums_2)
        left, right = 0, n - 1

        """
        Find the index of the pivot element (the smallest element)

        In the end, left will be the pivot.
        For example if the input array is [11, 12, 13, 1, 2, 3]
        Then left will equal to 3 (index of element 1)
        """
        while left <= right:
            mid = (left + right) // 2
            if nums_2[mid] > nums_2[-1]:
                left = mid + 1
            else:
                right = mid - 1

        # Binary search over an inclusive range [p1 ~ p2]
        def binarySearch(p1: int, p2: int, target_2: int) -> int:
            while p1 <= p2:
                mid = (p1 + p2) // 2
                if nums_2[mid] == target_2:
                    return mid
                elif nums_2[mid] > target_2:
                    p2 = mid - 1
                else:
                    p1 = mid + 1
            return -1

        # Binary search over elements on the pivot element's left
        answer = binarySearch(0, left - 1, target_2)
        if answer != -1:
            return answer

        # Binary search over elements on the pivot element's right
        return binarySearch(left, n - 1, target_2)

# ============================================================================
# Solution 3: B    (原文件: 04 - 0033 - B - Search Rotated Array - 2BST - 🚀.py)
# ============================================================================

# For this question, we do
# - 2 binary searches
#
# Which is quicker than approach A.

nums_3 = [4, 5, 6, 7, 0, 1, 2]

target_3 = 0

class Solution_3_B:
    def search(self, nums_3: List[int], target_3: int) -> int:
        n = len(nums_3)
        left, right = 0, n - 1

        """
        Find the index of the pivot element (the smallest element)

        In the end, left will be the pivot.
        For example if the input array is [11, 12, 13, 1, 2, 3]
        Then left will equal to 3 (index of element 1)
        """
        while left <= right:
            mid = (left + right) // 2
            if nums_3[mid] > nums_3[-1]:
                left = mid + 1
            else:
                right = mid - 1

        def shiftedBinarySearch(pivot: int, target_3: int) -> int:
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
                if nums_3[(m - shift) % n] == target_3:
                    return (m - shift) % n
                elif nums_3[(m - shift) % n] > target_3:
                    p2 = m - 1
                else:
                    p1 = m + 1
            return -1

        return shiftedBinarySearch(left, target_3)

# ============================================================================
# Solution 4: C    (原文件: 04 - 0033 - C - Search Rotated Array - 1BST - 🚀🚀🚀.py)
# ============================================================================

# For this question, we do
# - 1 single binary search.
#
# Which is significantly faster and easier than approaches 1 and 2.

nums_4 = [4, 5, 6, 7, 0, 1, 2]

target_4 = 0

class Solution_4_C:
    def search(self, nums_4: List[int], target_4: int) -> int:
        n = len(nums_4)
        left, right = 0, n - 1
        while left <= right:
            mid = left + (right - left) // 2

            # Case 1: find target_4
            if nums_4[mid] == target_4:
                return mid

            # Case 2: subarray on mid's left is sorted
            elif nums_4[mid] >= nums_4[left]:
                if target_4 >= nums_4[left] and target_4 < nums_4[mid]:
                    right = mid - 1
                else:
                    left = mid + 1

            # Case 3: subarray on mid's right is sorted.
            else:
                if target_4 <= nums_4[right] and target_4 > nums_4[mid]:
                    left = mid + 1
                else:
                    right = mid - 1
        return -1


if __name__ == "__main__":

    # --- Solution 2: A ---
    s = Solution_2_A()
    result = s.search(nums_2, target_2)
    print(result)

    # --- Solution 3: B ---
    s = Solution_3_B()
    result = s.search(nums_3, target_3)
    print(result)

    # --- Solution 4: C ---
    s = Solution_4_C()
    result = s.search(nums_4, target_4)
    print(result)
