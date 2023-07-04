from typing import List


"""
Time complexity: O(n)
Space complexity: O(1)
"""


class Solution:
    def average(self, salary: List[int]) -> float:
        min_ = max_ = salary[0]
        sum_ = 0
        for s in salary:
            sum_ += s
            min_ = min(s, min_)
            max_ = max(s, max_)
        return (sum_ - max_ - min_) / (len(salary) - 2)


s = Solution()
input_ = [4000, 3000, 1000, 2000]  # Expecting 2500.00000
result = s.average(input_)
print(result)

"""
Runtime
- 51 ms
- Beats 33.30%

Memory
- 16.3 MB
- Beats 16.5%
"""
