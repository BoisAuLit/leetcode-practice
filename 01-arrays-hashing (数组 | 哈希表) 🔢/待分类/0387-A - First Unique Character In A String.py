"""
Time complexity: O(n)
Space complexity: O(n)
"""


class Solution:
    def firstUniqChar(self, s: str) -> int:
        first_index, count = {}, {}
        for index, character in enumerate(s):
            if character not in first_index:
                first_index[character] = index
            count[character] = count.get(character, 0) + 1
        min_left_index = len(s)
        for character, frequency in count.items():
            if frequency == 1 and first_index[character] < min_left_index:
                min_left_index = first_index[character]
        return min_left_index if min_left_index != len(s) else -1


s = Solution()
input_ = "leetcode"  # Expecting 0
# input_ = "loveleetcode" # Expecting 2
# input_ = "aabb" # Expecting -1
result = s.firstUniqChar(input_)
print(result)

"""
Runtime
- 141 ms
- Beats 51.78%

Memory
- 16.5 MB
- Beats 64.57%
"""
