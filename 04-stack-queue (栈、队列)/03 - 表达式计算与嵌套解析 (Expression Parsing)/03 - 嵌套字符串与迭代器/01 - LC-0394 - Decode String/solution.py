# https://leetcode.com/problems/decode-string/

class Solution:
    def decodeString(self, s: str) -> str:
        stack = []
        for ch in s:
            if ch == "]":
                letters = []
                while stack[-1] != "[":
                    letters.append(stack.pop())
                stack.pop()  # Pop the "["
                numbers = []
                while stack and stack[-1].isdigit():
                    numbers.append(stack.pop())
                for _ in range(int("".join(numbers[::-1]))):
                    for i in range(len(letters)-1, -1, -1):
                        stack.append(letters[i])
            else:
                stack.append(ch)
        return "".join(stack)


# Test case 1: Expecting "aaabcbc"
# s = Solution()
# str_ = "3[a]2[bc]"
# result = s.decodeString(str_)
# print(result)

# Test case 2: Expecting "accaccacc"
s = Solution()
str_ = "3[a2[c]]"
result = s.decodeString(str_)
print(result)

# Test case 3: Expecting "abcabccdcdcdef"
s = Solution()
str_ = "2[abc]3[cd]ef"
result = s.decodeString(str_)
print(result)
