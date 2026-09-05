import collections

"""
Time complexity: O(n)
Space complexity: O(n)
"""


class Solution:
    def firstUniqChar(self, s: str) -> int:
        """
        :type s: str
        :rtype: int
        """
        # build hash map : character and how often it appears
        count = collections.Counter(s)

        # find the index
        for idx, ch in enumerate(s):
            if count[ch] == 1:
                return idx
        return -1


s = Solution()
input_ = "leetcode"  # Expecting 0
# input_ = "loveleetcode" # Expecting 2
# input_ = "aabb" # Expecting -1
result = s.firstUniqChar(input_)
print(result)

"""
Runtime
- 110 ms
- Beats 79.86%

Memory
- 16.5 MB
- Beats 64.57%
"""
