"""
Time complexity: O()
Space complexity: O()
"""

class Solution:
    def removeDuplicates(self, s: str) -> str:
        stack = []
        for letter in s:
            if stack and letter == stack[-1]:
                stack.pop()
            else:
                stack.append(letter)
        return "".join(stack)
        
                    

s = Solution()

# Expection "ca"
input_ = "abbaca"
result = s.removeDuplicates(input_)
print(result)

"""
Runtime
- 68ms
- Beats 94.91%

Memory
17.19mb
- Beats 74.28%
"""
