from typing import List

"""
Time complexity: O(n²)
Space complexity: O(1)

While O(n²) space is used to store the output,
the input and output generally do not count towards the space complexity.
"""


class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        triangle = []
        for i in range(1, numRows + 1):
            row = [None] * i
            row[0] = row[-1] = 1
            for j in range(1, i - 1):
                row[j] = triangle[-1][j - 1] + triangle[-1][j]
            triangle.append(row)
        return triangle


s = Solution()
input_ = 10
result = s.generate(input_)
print(result)

"""
Runtime
- 32 ms
- Beats 99.58%

Memory
- 16.2 MB
- Beats 98.7%
"""
