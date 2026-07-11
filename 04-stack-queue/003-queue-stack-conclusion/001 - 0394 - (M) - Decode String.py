"""
https://www.youtube.com/watch?v=qB0zZpBJlh8&t=98s&ab_channel=NeetCode
"""


class Solution:
    def decodeString(self, s: str) -> str:
        stack = []
        for c in s:
            if c != "]":
                stack.append(c)
            else:
                substr = ""
                while stack[-1] != "[":
                    substr = stack.pop() + substr
                stack.pop()

                k = ""
                while stack and stack[-1].isdigit():
                    k = stack.pop() + k
                stack.append(int(k) * substr)
        return "".join(stack)


solution = Solution()

# Test case 1: Expecting "aaabcbc"
# input_ = "3[a]2[bc]"

# Test case 2: Expecting "accaccacc"
# input_ = "3[a2[c]]"

# Test case 3: Expecting "abcabccdcdcdef"
# input_ = "2[abc]3[cd]ef"

# Test case 4: Expecting "deaccaccaccdeaccaccaccdeaccaccaccdeaccaccacc"
# input_ = "4[de3[a2[c]]]"

# Test case 5: Expecting "abcabccdcdcdef"
# input_ = "2[abc]3[cd]ef"

# Test case 6: Expecting "abccdcdcdxyz"
# input_ = "abc3[cd]xyz"

# Test case 7: Expecting ""
# input_ = "3[z]2[2[y]pq4[2[jk]e1[f]]]ef"


# Test case 8: Expecting "leetcode"
# In this case, there are no square brackets at all
input_ = "leetcode"

result = solution.decodeString(input_)
print(result)
