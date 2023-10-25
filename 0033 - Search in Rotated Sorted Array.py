from typing import List


class Solution_Best_of_Best:
    """
    Time complexity: O(logN)
    Space complexity: O(1)
    """

    def search(self, nums: List[int], target: int) -> int:
        n = len(nums)
        left, right = 0, n - 1
        while left <= right:
            mid = left + (right - left) // 2

            # Case 1: find target
            if nums[mid] == target:
                return mid

            # Case 2: subarray on mid's left is sorted
            elif nums[mid] >= nums[left]:
                if target >= nums[left] and target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1

            # Case 3: subarray on mid's right is sorted.
            else:
                if target <= nums[right] and target > nums[mid]:
                    left = mid + 1
                else:
                    right = mid - 1
        return -1


class Solution:
    """
    Time complexity: O(logN)
    Space complexity: O(1)

    First use binary search to find the pivot index (index of the smallest element)
    Then use binary search on entire array. (use different notations for indices)
    """

    def search(self, nums: List[int], target: int) -> int:
        n = len(nums)
        left, right = 0, n - 1

        # Find the index of the pivot element (the smallest element)
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] > nums[-1]:
                left = mid + 1
            else:
                right = mid - 1

        # Shift elements in circular manner, with the pivot element at index 0.
        # Then perform a regular binary search
        def shiftedBinarySearch(pivot_index, target):
            shift = n - pivot_index
            left, right = 0, n - 1

            while left <= right:
                mid = (left + right) // 2
                if nums[(mid - shift) % n] == target:
                    return (mid - shift) % n
                elif nums[(mid - shift) % n] > target:
                    right = mid - 1
                else:
                    left = mid + 1
            return -1

        return shiftedBinarySearch(left, target)


class Solution:
    """
    Time complexity: O(logN)
    Space complexity: O(1)

    First use binary search to find the pivot index (index of the smallest element)
    Then use binary search on left and right side of the pivot
    """

    def search(self, nums: List[int], target: int) -> int:
        n = len(nums)
        left, right = 0, n - 1

        # Find the index of the pivot element (the smallest element)
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] > nums[-1]:
                left = mid + 1
            else:
                right = mid - 1

        # Binary search over an inclusive range [left_boundary ~ right_boundary]
        def binarySearch(left_boundary, right_boundary, target):
            left, right = left_boundary, right_boundary
            while left <= right:
                mid = (left + right) // 2
                if nums[mid] == target:
                    return mid
                elif nums[mid] > target:
                    right = mid - 1
                else:
                    left = mid + 1
            return -1

        # Binary search over elements on the pivot element's left
        if (answer := binarySearch(0, left - 1, target)) != -1:
            return answer

        # Binary search over elements on the pivot element's right
        return binarySearch(left, n - 1, target)


s = Solution()

# ini_list = [[99, 100, 101], list(range(1, 99))]
# nums = list(chain.from_iterable(ini_list))
# target = 33

# nums = [4, 5, 6, 7, 8, 11, 0, 1, 2]
# for x in [4, 5, 6, 7, 8, 11, 0, 1, 2, 3, 10, 12]:
#     result = s.search(nums, x)
#     print(result)


nums = [3, 1]
target = 1
result = s.search(nums, target)
print(result)
