class Solution:
    def removeKdigits(self, num: str, k: int) -> str:
        stack = []

        # Construct a monotone increasing sequence of digits
        for digit in num:
            while k and stack and stack[-1] > digit:
                stack.pop()
                k -= 1

            stack.append(digit)

        # - Trunk the remaining K digits at the end
        # - in the case k==0: return the entire list
        finalStack = stack[:-k] if k else stack

        # trip the leading zeros
        return "".join(finalStack).lstrip("0") or "0"


s = Solution()

num = "12345264"
k = 4

result = s.removeKdigits(num, k)
print(result)

"""

"""
