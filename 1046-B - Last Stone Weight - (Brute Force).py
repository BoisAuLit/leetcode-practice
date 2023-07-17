from typing import List

"""
Time complexity: O(n2)
Space complexity:
- O(1) if we can modify input list in place
- O(n) if we cannot modify input list in place
"""


class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        stones = stones.copy()
        while len(stones) > 2:
            m = 0 if stones[0] <= stones[1] else 1
            n = 1 - m 
            for i in range(2, len(stones)):
                if stones[i] > stones[n]:
                    m = n
                    n = i
                elif stones[i] <= stones[n] and stones[i] >= stones[m]:
                    m = i
            diff = abs(stones.pop(max(m, n)) - stones.pop(min(m, n)))
            if diff != 0:
                stones.append(diff)
        if len(stones) == 0:
            return 0
        if len(stones) == 1:
            return stones[0]
        return abs(stones[0] - stones[1])


s = Solution()
input_ = [2, 7, 4, 1, 8, 1]  # Expecting 1
# input_ = [1] # Expecting 1
# input_ = [3, 7, 8]  # Expecting 2
# input_ = [4, 3, 4, 3, 2]  # Expecting 2
result = s.lastStoneWeight(input_)
print(result)

"""
Runtime
- 49 ms
- Beats 50.40%

Memory
- 16.3 MB
- Beats 33.76%
"""
