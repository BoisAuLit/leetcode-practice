from typing import List

"""
Time complexity: O(S)
Space complexity: O(1)
"""


# Solution 1 --> Sort, then compare the first and the last 👍
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


# Solution 2 --> Vertical scan
class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        index = 0
        result = ""
        if len(strs) == 1:
            return strs[0]
        while True:
            for i in range((len(strs) - 1)):
                if (
                    index > len(strs[i]) - 1
                    or index > len(strs[i + 1]) - 1
                    or strs[i][index] != strs[i + 1][index]
                ):
                    return result
            result += strs[0][index]
            index += 1


s = Solution()
# input_ = ["flower", "flow", "flight"]
input_ = [""]
result = s.longestCommonPrefix(input_)
print(result)
