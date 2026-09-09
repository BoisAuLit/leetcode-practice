from typing import List


class Solution:
    def findIndex(self, nums: List[int]) -> int:
        """
        Find pivot index:
            It's the index of the smallest element
            index is also the times it's rotated to the right
        """

        # ! If the array is already sorted, then we short-circuit
        if nums[0] <= nums[-1]:
            return 0
        l = 0
        r = len(nums) - 1
        while l <= r:
            m = (l + r) // 2
            # ! 这一步非常关键，一旦当前元素大于下一个，我们就返回下一个 index
            if nums[m] > nums[m + 1]:
                return m + 1
            if nums[m] > nums[l]:
                l = m
            else:
                r = m
        return -1

    def search(self, nums: List[int], target: int) -> int:
        i = self.findIndex(nums)
        # ! Short-circuit（一旦不在数组里，我们就快速返回）
        if target < nums[i] or target > nums[i - 1]:
            return -1
        l = i
        r = i + len(nums) - 1
        while l <= r:
            # ! 由于我们是直接在 sorted array 里搜寻，所以要加上这个 % len(nums)
            m = ((l + r) // 2) % len(nums)
            if nums[m] < target:
                l += 1
            elif nums[m] > target:
                r -= 1
            else:
                # ! 由于我们是直接在 sorted array 里搜寻，所以要加上这个 % len(nums)
                return m % len(nums)
        return -1


s = Solution()
input_ = [1, 3]
target = 0
result = s.search(input_, target)
print(result)
