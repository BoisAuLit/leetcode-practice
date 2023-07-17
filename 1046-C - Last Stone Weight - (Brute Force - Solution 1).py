from typing import List

"""
Time complexity: O(n2)
Space complexity:
- O(1) if we can modify input list in place
- O(n) if we cannot modify input list in place

- Find and remove the maximum stone in O(N) time
- Add the new stone in O(1) time
"""


class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        def remove_largest():
            index_of_largest = stones.index(max(stones))
            stones[index_of_largest], stones[-1] = stones[-1], stones[index_of_largest]
            return stones.pop()

        while len(stones) > 1:
            stone_1 = remove_largest()
            stone_2 = remove_largest()
            if stone_1 != stone_2:
                stones.append(stone_1 - stone_2)

        return stones[0] if stones else 0


s = Solution()
input_ = [2, 7, 4, 1, 8, 1]  # Expecting 1
# input_ = [1] # Expecting 1
# input_ = [3, 7, 8]  # Expecting 2
# input_ = [4, 3, 4, 3, 2]  # Expecting 2
result = s.lastStoneWeight(input_)
print(result)

"""
Runtime
- 35 ms
- Beats 98.60%

Memory
- 16.2 MB
- Beats 95.83%
"""
