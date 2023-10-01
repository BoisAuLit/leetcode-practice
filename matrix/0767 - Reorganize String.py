from collections import Counter
import itertools

"""
Time complexity: O(N)
Space complexity: O(1)
"""


class Solution:
    def reorganizeString(self, s: str) -> str:
        counter = Counter(s).most_common()
        if counter[0][1] > (len(s) + 1) // 2:
            return ""
        ans = [""] * len(s)
        indices = itertools.chain(range(0, len(s), 2), range(1, len(s), 2))
        for letter, count in counter:
            for _ in range(count):
                ans[next(indices)] = letter
        return "".join(ans)


s = Solution()

# Expecting "ababadacbc"
input_ = "aabbcaabcd"
result = s.reorganizeString(input_)
print(result)

"""

"""
