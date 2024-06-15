from typing import List
from collections import deque

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        answer = [0] * n
        stack = []
        for curr_day, curr_temp in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < curr_temp:
                prev_day = stack.pop()
                answer[prev_day] = curr_day - prev_day
            stack.append(curr_day)
        
        return answer


s = Solution()
temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
# temperatures = [30,40,50,60]
result = s.dailyTemperatures(temperatures)
print(result)
