class Solution:
    def robotWithString(self, s: str) -> str:
        n = len(s)
        min_letter = s[-1]
        min_index = n - 1
        minR = [0] * n
        minR[-1] = n - 1
        for i in range(n - 2, -1, -1):
            if s[i] <= min_letter:
                min_letter = s[i]
                min_index = i
                minR[i] = i
            else:
                minR[i] = min_index
        print(minR)
        paper = []
        stack = []
        i = 0
        while i <= n - 1:
            if stack and stack[-1] <= s[minR[i]]:
                paper.append(stack.pop())
            elif i == minR[i]:
                paper.append(s[i])
                i += 1
            else:
                stack.append(s[i])
                i += 1

        return "".join(paper) + "".join(reversed(stack))


# # Test case 1: Expecting "aabvbcdk"
# s = Solution()
# input_ = "abbacdk"
# result = s.robotWithString(input_)
# print(result)

# Test case 2: Expecting "fnohopzv"
s = Solution()
input_ = "vzhofnpo"
result = s.robotWithString(input_)
print(result)
