from typing import List

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def minDeletionSize(self, strs: List[str]) -> int:
        count = 0
        for i in range(len(strs[0])):
            for j in range(len(strs) - 1):
                if ord(strs[j][i]) > ord(strs[j + 1][i]):
                    count += 1
                    break
        return count


s = Solution()
# input_ = ["zyx", "wvu", "tsr"]  # Expecting 3
input_ = ["cba", "daf", "ghi"]  # Expecting 1
result = s.minDeletionSize(input_)
print(result)

"""
Runtime
- 221 ms
Beats 16.43%

Memory
- 17.2 MB
- Beats 26.81%
"""
