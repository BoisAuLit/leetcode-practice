from typing import List


class Solution:
    def sortColors(self, nums: List[int]) -> None:
        low = mid = 0

        high = len(nums) - 1

        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
            elif nums[mid] == 2:
                # We don't increment mid by 1 because the element
                # that was swapped from high position to current position
                # has not been checked yet
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1
            else:
                mid += 1
