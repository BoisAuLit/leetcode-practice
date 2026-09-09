"""LC-0394 - Decode String

合并自 2 个解法文件:
  1. 001 - 0394 - Decode String.py
  2. LC-0394 - Decode String.py
"""


# ============================================================================
# Solution 1: V1    (原文件: 001 - 0394 - Decode String.py)
# ============================================================================

# https://www.youtube.com/watch?v=qB0zZpBJlh8&t=98s&ab_channel=NeetCode

input_ = "leetcode"

class Solution_1_V1:
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

# ============================================================================
# Solution 2: V2    (原文件: LC-0394 - Decode String.py)
# ============================================================================

class Solution_2_V2:
    def decodeString(self, s: str) -> str:
        pass


if __name__ == "__main__":

    # --- Solution 1: V1 ---
    solution = Solution_1_V1()
    result = solution.decodeString(input_)
    print(result)
