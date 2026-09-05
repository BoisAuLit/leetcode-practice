from typing import List

"""
Time complexity: O(n)
Space complexity: O(n)
"""


class Solution:
    def summaryRanges(self, nums: List[int]) -> List[str]:
        streak = []
        result = []
        def push_streak_to_result():
            if len(streak) == 1:
                result.append(str(streak[0]))
            elif len(streak) > 1:
                result.append(f"{streak[0]}->{streak[-1]}")    
        for num in nums:
            if len(streak) == 0:
                streak.append(num)
                continue
            if num - streak[-1] == 1:
                streak.append(num)
            else:
                push_streak_to_result()
                streak = [num]
        push_streak_to_result()
        

        return result


s = Solution()

# Expecting ["0->2","4->5","7"]
# nums = [0, 1, 2, 4, 5, 7]

# Expecting []
nums = []

result = s.summaryRanges(nums)
print(result)

"""
Runtime
- 36ms
- Beats 92.87%

Memory
16.24mb
- Beats 73.35%
"""
