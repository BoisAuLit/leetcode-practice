from typing import List

"""
Time complexity: O(S)
Space complexity: O(1)
"""


class Solution:
    def longestCommonPrefix(self, v: List[str]) -> str:
        ans = ""
        v = sorted(v)
        first = v[0]
        last = v[-1]
        for i in range(min(len(first), len(last))):
            if first[i] != last[i]:
                return ans
            ans += first[i]
        return ans


s = Solution()
# input_ = ["flower", "flow", "flight"]
input_ = [""]
result = s.longestCommonPrefix(input_)
print(result)
