from typing import List

class Solution:
    def triangleNumber(self, nums: List[int]) -> int:
        n = len(nums)
        def binary_search(l: int, r: int, x: int) -> int:
            # Find the first index >= x in the range [l, r]
            while r >= l and r < n:
                mid = (l + r) // 2
                if nums[mid] >= x:
                    r = mid - 1
                else:
                    l = mid + 1
            return l

        nums.sort()
        res = 0

        for i in range(n - 2):
            k = i + 2
            for j in range(i + 1, n - 1):
                if nums[i] == 0:
                    break
                k = binary_search(k, n - 1, nums[i] + nums[j])
                res += k - j - 1

        return res
