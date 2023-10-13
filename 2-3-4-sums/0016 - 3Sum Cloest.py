from typing import List

"""
Time complexity: O(N²)
Space complexity: O(NlogN) to O(N)
"""

class Solution:

    def threeSumClosest(self, nums: List[int], target: int) -> int:
        diff = float('inf')
        nums.sort()
        for i in range(len(nums)):
            lo, hi = i + 1, len(nums) - 1
            while (lo < hi):
                sum_ = nums[i] + nums[lo] + nums[hi]
                if abs(target - sum_) < abs(diff):
                    diff = target - sum_
                if sum_ < target:
                    lo += 1
                else:
                    hi -= 1
            if diff == 0:
                break
        return target - diff

s = Solution()

# Expecting 2
# nums = [-1, 2, 1, -4]
# target = 1

# Expecting 15
# nums = [2, 3, 8, 9, 10]
# target = 16

# Expecting -2960
nums = [833,736,953,-584,-448,207,128,-445,126,248,871,860,333,-899,463,488,-50,-331,903,575,265,162,-733,648,678,549,579,-172,-897,562,-503,-508,858,259,-347,-162,-505,-694,300,-40,-147,383,-221,-28,-699,36,-229,960,317,-585,879,406,2,409,-393,-934,67,71,-312,787,161,514,865,60,555,843,-725,-966,-352,862,821,803,-835,-635,476,-704,-78,393,212,767,-833,543,923,-993,274,-839,389,447,741,999,-87,599,-349,-515,-553,-14,-421,-294,-204,-713,497,168,337,-345,-948,145,625,901,34,-306,-546,-536,332,-467,-729,229,-170,-915,407,450,159,-385,163,-420,58,869,308,-494,367,-33,205,-823,-869,478,-238,-375,352,113,-741,-970,-990,802,-173,-977,464,-801,-408,-77,694,-58,-796,-599,-918,643,-651,-555,864,-274,534,211,-910,815,-102,24,-461,-146]
target = -7111

result = s.threeSumClosest(nums, target)
print(result)

"""

"""
