from typing import List
from collections import deque


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        answer = [0] * n
        stack = deque()

        for index, temp in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < temp:
                prev_index = stack.pop()
                answer[prev_index] = index - prev_index
            stack.append(index)

        return answer


s = Solution()

# Test case 1: Expecting [1,1,4,2,1,1,0,0]
temperatures = [73, 74, 75, 71, 69, 72, 76, 73]

# Test case 2: Expecting [1,1,1,0]
# temperatures = [30, 40, 50, 60]

# Test case 3: Expectint [1,1,0]
# temperatures = [30, 60, 90]


result = s.dailyTemperatures(temperatures)
print(result)
