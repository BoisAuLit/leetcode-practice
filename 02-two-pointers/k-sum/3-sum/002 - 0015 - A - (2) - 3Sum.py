from typing import List

"""
Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]]
such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.
"""

# ===========================================================================
# 笔记：为什么外层循环里有 `if i == 0 or nums[i - 1] != nums[i]:`
# ===========================================================================
# 作用：给"第一个数"去重（跳过重复数字）。
#
# 前提：数组已经排序，所以相同的数字挨在一起，例如：
#     索引:   0    1    2    3    4
#     值:    -2   -2   -1    3    3
#
# 若不去重：i=0 选 -2 找到 [-2,-1,3]；i=1 又是 -2，会再找出一模一样的
# [-2,-1,3] → 结果重复。题目要求三元组不能重复，所以必须跳过。
#
# 条件拆解（用 or 连接，满足其一就处理）：
#     i == 0               → 第一个元素，前面没得比，永远处理
#     nums[i-1] != nums[i] → 和前一个不同，是"新"数字才处理
# 只有 i != 0 且 nums[i-1] == nums[i]（与前一个相同）时才跳过。
#
# 走一遍上面的例子：
#     i=0 (-2): i==0            → 处理 ✅
#     i=1 (-2): 与前一个相同     → 跳过 ⏭️ (-2 已作为第一个数处理过)
#     i=2 (-1): 与前一个不同     → 处理 ✅
#     i=3 ( 3): 与前一个不同     → 处理 ✅
#     i=4 ( 3): 与前一个相同     → 跳过 ⏭️
#
# 关键点：和"前一个"比而不是"后一个"，是为了保留每个值第一次出现的位置、
# 跳过之后的重复。一句话记：排序后，只在数字"第一次出现"时才处理它。
#
# 补充：twoSumII 里 `while lo < hi and nums[lo] == nums[lo - 1]` 是同样的
# 去重思路，只不过针对三元组里的"第二个数"。
# ===========================================================================


class Solution:
    """
    Time complexity: O(N² + NlogN) --> O(N²)
    Space complexity: Between O(logN) & O(N)
    """
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        res = []
        nums.sort()
        for i in range(len(nums)):
            if nums[i] > 0:
                break
            if i == 0 or nums[i - 1] != nums[i]: # 这里是为了去重
                self.twoSumII(nums, i, res)
        return res

    def twoSumII(self, nums: List[int], i: int, res: List[List[int]]):
        lo, hi = i + 1, len(nums) - 1
        while lo < hi:
            sum = nums[i] + nums[lo] + nums[hi]
            if sum < 0:
                lo += 1
            elif sum > 0:
                hi -= 1
            else:
                res.append([nums[i], nums[lo], nums[hi]])
                # 可以是 【2,9】，也可以是【3,8】！
                lo += 1
                hi -= 1
                # 这里也是为了去重
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1


s = Solution()
input_ = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# input_ = [-1, 0, 1, 2, -1, -4]
result = s.threeSum(input_)
print(result)
