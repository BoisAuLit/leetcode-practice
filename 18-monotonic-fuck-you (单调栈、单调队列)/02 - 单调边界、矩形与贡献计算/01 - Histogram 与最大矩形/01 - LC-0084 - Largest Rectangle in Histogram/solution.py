# https://leetcode.com/problems/largest-rectangle-in-histogram/
# https://neetcode.io/problems/largest-rectangle-in-histogram/question?list=neetcode150

class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        heights = [0] + heights + [0]      # 左右各加一堵高度 0 的墙
        stack = [0]                        # 栈底放左墙(下标 0),它永远不会被弹出
        res = 0
        for i in range(1, len(heights)):
            while heights[i] < heights[stack[-1]]:
                top = stack.pop()
                left = stack[-1]           # 栈永远不空,不需要 else -1
                res = max(res, (i - left - 1) * heights[top])
            stack.append(i)
        return res

s = Solution()
input_ = [7,1,7,2,2,4]
result = s.largestRectangleArea(input_)
print(result)

