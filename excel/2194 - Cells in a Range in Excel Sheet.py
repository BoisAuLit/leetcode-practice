from typing import List


class Solution:
    def cellsInRange(self, s: str) -> List[str]:
        [c1, r1], [c2, r2] = s.split(":")
        return [
            chr(i) + str(j)
            for i in range(ord(c1), ord(c2) + 1)
            for j in range(int(r1), int(r2) + 1)
        ]


s = Solution()
input_ = "M3:O6"
result = s.cellsInRange(input_)
print(result)

"""

"""
