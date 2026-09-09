from typing import List


class Solution_1:
    def trap(self, height: List[int]) -> int:
        if len(height) <= 2:
            return 0
        # ! 不包含 i 自己的左边最大
        from_left = [0] * len(height)
        from_right = [0] * len(height)
        for i in range(1, len(height)):
            from_left[i] = max(from_left[i - 1], height[i - 1])
            from_right[len(height) - i - 1] = max(
                from_right[len(height) - i], height[len(height) - i]
            )
        result = 0
        for i in range(1, len(height) - 1):
            min_l_r = min(from_left[i], from_right[i])
            if height[i] < min_l_r:
                result += min_l_r - height[i]
        return result

# ! Monotonic stack
class Solution_2:
    def trap(self, height: List[int]) -> int:
        if not height:
            return 0
        stack = []
        res = 0

        for i in range(len(height)):
            while stack and height[i] >= height[stack[-1]]:
                mid = height[stack.pop()]
                if stack:
                    right = height[i]
                    left = height[stack[-1]]
                    h = min(right, left) - mid
                    w = i - stack[-1] - 1
                    res += h * w
            stack.append(i)
        return res


class Solution_3:
    def trap(self, height: List[int]) -> int:
        if not height:
            return 0

        l, r = 0, len(height) - 1
        leftMax, rightMax = height[l], height[r]
        res = 0
        while l < r:
            if leftMax < rightMax:
                l += 1
                leftMax = max(leftMax, height[l])
                res += leftMax - height[l]
            else:
                r -= 1
                rightMax = max(rightMax, height[r])
                res += rightMax - height[r]
        return res


s = Solution_1()
input_ = [0, 2, 0, 3, 1, 0, 1, 3, 2, 1]
result = s.trap(input_)
print(result)
