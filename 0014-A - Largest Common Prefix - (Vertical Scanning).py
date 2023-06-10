from typing import List

"""
Time complexity: O(S)
Space complexity: O(1)
"""


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
