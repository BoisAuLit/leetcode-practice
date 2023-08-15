from collections import deque


class Solution(object):
    def reverseOnlyLetters(self, S):
        letters = [c for c in S if c.isalpha()]
        ans = []
        for c in S:
            if c.isalpha():
                ans.append(letters.pop())
            else:
                ans.append(c)
        return "".join(ans)


s = Solution()

# Expecting "Qedo1ct-eeLg=ntse-T!"
# input_ = "Test1ng-Leet=code-Q!"

# Expecting "7_28]"
input_ = "7_28]"

result = s.reverseOnlyLetters(input_)
print(result)
