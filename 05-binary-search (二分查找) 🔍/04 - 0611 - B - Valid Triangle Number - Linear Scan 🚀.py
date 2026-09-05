from typing import List

class Solution:
    def triangleNumber(self, nums: List[int]) -> int:
        nums.sort()
        n = len(nums)
        count = 0

        for i in range(n - 2):
            if nums[i] == 0:
                continue   # 0 不能作为三角形最小边

            k = i + 2
            for j in range(i + 1, n - 1):
                # 线性推进 k，不回退
                while k < n and nums[i] + nums[j] > nums[k]:
                    k += 1

                # [j+1, k-1] 都可以作为第三条边
                count += k - j - 1

        return count
