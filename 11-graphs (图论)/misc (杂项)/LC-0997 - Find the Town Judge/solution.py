from typing import List

"""
Time complexity: O(n)
Space complexity: O(n)
"""


class Solution:
    def findJudge(self, n: int, trust: List[List[int]]) -> int:
        trust_mapping = [
            {"people_trusting_him": [], "people_he_trusts": []}
            for _ in range(n)
        ]
        for pair in trust:
            trust_mapping[pair[0] - 1]["people_he_trusts"].append(pair[1])
            trust_mapping[pair[1] - 1]["people_trusting_him"].append(pair[0])
        for index, t in enumerate(trust_mapping):
            if (
                len(t["people_he_trusts"]) == 0
                and len(t["people_trusting_him"]) == n - 1
            ):
                return index + 1
        return -1


s = Solution()

# Expecting 2
# n = 2
# trust = [[1, 2]]

# Expecting 3
# n = 3
# trust = [[1,3],[2,3]]

# Expecting -1
n = 3
trust = [[1,3],[2,3],[3,1]]


result = s.findJudge(n, trust)
print(result)

"""
Runtime
- 770 ms
- Beats 45.96%

Memory
- 22.3 MB
- Beats 13.28%
"""
