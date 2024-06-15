"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def countAndSay(self, n: int) -> str:
        round = n - 1
        n_str = "1"
        while round > 0:
            count = 1
            result = []

            last_char = n_str[0]
            for char in n_str[1:]:
                if char == last_char:
                    count += 1
                else:
                    result.extend([str(count), last_char])
                    count = 1
                    last_char = char
            result.extend([str(count), last_char])
            n_str = result
            round -= 1
        return "".join(n_str)


s = Solution()
input_ = 4
result = s.countAndSay(input_)
print(result)
