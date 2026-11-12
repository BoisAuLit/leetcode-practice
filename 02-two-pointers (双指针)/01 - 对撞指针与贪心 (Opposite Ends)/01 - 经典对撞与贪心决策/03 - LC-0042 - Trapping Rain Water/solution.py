"""LC-0042 - Trapping Rain Water

Level 1 · 01 对撞指针与贪心 —— 每轮确定一侧、当场结算
题目在问：柱状图能接多少雨水

决定性观察：**第 i 格的水量 = `min(左边最高, 右边最高) - height[i]`**（小于 0 按 0 算）。
      难点只有一个：怎么不用两个辅助数组就知道这两个最高值。

对撞指针的论证（本家族的核心）：设当前 `height[l] < height[r]`。
      那么 r 的左边必然存在一面高度 >= `height[r]` > `height[l]` 的墙，
      所以 **l 这一格的瓶颈一定在左侧**，`left_max` 已经是它的最终答案，可以当场结算，
      完全不需要知道右边具体有多高。反之亦然。这和 LC-0011「移短边」是同一个论证。

循环不变量：`left_max` = `height[0..l]` 的最大值，`right_max` = `height[r..n-1]` 的最大值；
      `[l, r]` 之外的水已全部结算完毕。

三种解法的取舍：
  - 前后缀最大值数组：最好想，O(n) 时间 O(n) 空间
  - **对撞双指针：O(n) 时间 O(1) 空间，面试要的就是它**
  - 单调栈：按「层」横着结算，和 LC-0084、LC-0739 共用模板；空间 O(n)

坑：
  - 比较的是 `height[l] < height[r]`，不是 `left_max < right_max`（后者也能写对，但要先更新再比）
  - 结算用 `left_max - height[l]`，而 `left_max` 必须**先用当前高度更新过**，否则会算出负数
  - 空数组要能处理（这题保证 n >= 1，但模板里别假设）
"""

from typing import List

"""
Time complexity: O(N)
Space complexity: O(N)
"""


##################################################################################################
##### ! Solution 1: 后缀最大值数组 + 一次正扫（原解法）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：最容易想到、最不容易写错；right[i] 预处理成「i 右边的最高墙」后一遍扫完
##################################################################################################


class Solution_1:
    def trap(self, height: List[int]) -> int:
        right = height.copy()
        for i in range(len(height) - 2, -1, -1):
            right[i] = max(right[i+1], height[i])
        res = 0
        maxL = height[0]
        for i, h in enumerate(height):
            maxL, maxR = max(maxL, h), right[i]
            if maxL > h and maxR > h:
                res += min(maxL, maxR) - h
        return res


##################################################################################################
##### ! Solution 2: 对撞双指针（矮的一侧当场结算）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：★ 空间最优，本目录要练的就是它；和 LC-0011 共用「移较矮/较短的一侧」这个论证
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_2:
    def trap(self, height: List[int]) -> int:
        if not height:
            return 0
        l, r = 0, len(height) - 1
        left_max = right_max = 0
        water = 0
        while l < r:
            if height[l] < height[r]:
                # ! 右边一定有比 height[l] 高的墙 ⇒ l 的瓶颈在左侧，可以当场结算
                left_max = max(left_max, height[l])
                water += left_max - height[l]
                l += 1
            else:
                right_max = max(right_max, height[r])
                water += right_max - height[r]
                r -= 1
        return water


##################################################################################################
##### ! Solution 3: 单调递减栈（横着一层一层结算）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：和 LC-0084、LC-0739 同一个模板；前两种是「竖着按列算」，这个是「横着按层算」
##################################################################################################


class Solution_3:
    def trap(self, height: List[int]) -> int:
        stack: List[int] = []   # 存下标，对应的高度单调不增
        water = 0
        for i, h in enumerate(height):
            while stack and height[stack[-1]] < h:
                bottom = stack.pop()        # ! 被夹住的那一层的底
                if not stack:
                    break                   # 左边没有墙，接不住水
                left = stack[-1]
                width = i - left - 1
                depth = min(height[left], h) - height[bottom]
                water += width * depth
            stack.append(i)
        return water


s = Solution_1()
height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
result = s.trap(height)
print(result)

if __name__ == "__main__":
    import random
    cases = [([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6), ([4, 2, 0, 3, 2, 5], 9),
             ([1], 0), ([3, 3], 0), ([5, 4, 3, 2, 1], 0), ([2, 0, 2], 2)]
    sols = [Solution_1(), Solution_2(), Solution_3()]
    for sol in sols:
        for h, want in cases:
            got = sol.trap(h[:])
            assert got == want, f"{type(sol).__name__} {h}: got {got}, want {want}"

    def brute(h):   # ! 逐格算 min(左max, 右max) - h[i]
        return sum(max(0, min(max(h[:i + 1]), max(h[i:])) - h[i]) for i in range(len(h)))

    rng = random.Random(42)
    for _ in range(3000):
        h = [rng.randint(0, 6) for _ in range(rng.randint(1, 12))]
        want = brute(h)
        for sol in sols:
            assert sol.trap(h[:]) == want, (type(sol).__name__, h, want)
    print("3 个解法全过（含 3000 组随机对拍）")
