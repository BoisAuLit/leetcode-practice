"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def countBinarySubstrings(self, s: str) -> int:
        index = 0
        previous_count = 0
        result = 0
        while index < len(s):
            count = 0
            current_streak = s[index]
            while True:
                if index == len(s) or s[index] != current_streak:
                    break
                count += 1
                index += 1
            result += min(count, previous_count)
            previous_count = count
        return result


# class Solution:
#     def countBinarySubstrings(self, s: str) -> int:
#         index = 0
#         previous_count = 0
#         result = 0
#         while index < len(s):
#             count = 0
#             current_streak = s[index]
#             while True:
#                 if index == len(s) or s[index] != current_streak:
#                     break
#                 count += 1
#                 index += 1
#             result += min(count, previous_count)
#             previous_count = count
#         return result


s = Solution()
# input_ = "00110011"  # Expecting 6
input_ = "10101"  # Expecting 4
result = s.countBinarySubstrings(input_)
print(result)

"""
Runtime
- 179ms
- Beats 43.34%

Memory
16.81mb
- Beats 49.25%
"""
