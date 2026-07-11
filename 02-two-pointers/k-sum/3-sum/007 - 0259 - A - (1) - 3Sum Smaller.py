from typing import List

"""
Time complexity: O(N²)
Space complexity: O(1)
"""


class Solution:
    def threeSumSmaller(self, nums: List[int], target: int) -> int:
        nums.sort()  # 排序是利用双指针的前提
        count = 0

        # 固定第一个数 nums[i]，然后在它右边用双指针 lo、hi 从两端往中间夹。
        for i in range(len(nums) - 2):
            lo = i + 1
            hi = len(nums) - 1
            if nums[i] + nums[lo] + nums[lo + 1]  >= target:
                break
            if nums[i] + nums[hi-1] + nums[hi]  < target:
                # 这个其实就是排列组合 C(n, 2)
                # “// 2” 是因为必须要得到 int 返回值，即使 C(n, 2) 必为偶数
                count += (hi - lo + 1) * (hi - lo) // 2
                continue

            # 以上的两个 if 其实是抄近道，以下的 7 行才是最精华的部分 ⭐️
            # lo 从左端、hi 从右端，向中间夹紧
            while lo < hi:
                # 既然【i，lo，hi】的组合满足条件，
                # 那么 对于所有的 lo <= k <= hi-1 的 k，必然都满足条件
                # 这样的【lo，hi】组合总共有 hi - lo 对，所以 “count += hi - lo” 是合理的
                if nums[i] + nums[lo] + nums[hi] < target:
                    count += hi - lo
                    lo += 1
                else:
                    hi -= 1

        return count


s = Solution()

# Expection 2
nums = [-2, 0, 1, 3]
target = 2

# Expection 3
nums = [-2, 0, 1, 3]
target = 4


result = s.threeSumSmaller(nums, target)
print(result)
