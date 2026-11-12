"""LC-0503 - Next Greater Element II

Level 1 · 01 最近更大元素与跨度 —— Circular Array（循环数组）上的 Next Greater Element
题目在问：对每个 nums[i]，求**循环意义下**右边第一个严格更大的数；没有就是 -1。

决定性观察：
  1. 这题不是新算法，是 LC-0496 / LC-0739 的**同一个单调栈**换到环上跑。
  2. 环只需要**走两轮**就够了：任何 i 的答案，最远也只会在绕一圈之内被找到。
     理由：如果绕满一圈（n 个元素）都没有比 nums[i] 大的，那 nums[i] 是全局最大值，
     再绕第三圈只会看到同样一批元素，答案只能是 -1。
  3. 不需要真的 `nums * 2` 复制数组，用 `i % n` 即可 —— 省一半空间，语义也更清楚。

Stack 里存什么：**下标**（0..n-1），对应的 nums 值从栈底到栈顶单调不增。
      存下标而不是值，是因为答案要写回 res[下标]，而且环上会重复访问同一个值。

Pop 条件：`nums[i % n] > nums[stack[-1]]` —— 严格大于。
      相等不弹：题目要的是「严格更大」，等值不算答案。

为什么 Pop 是安全的：被弹出的 j 已经拿到了它的答案（当前这个 i 就是右边第一个更大的），
      它对后面的元素再也没有用 —— 后面的元素要是能被 j 挡住，早就被 i 挡住了（nums[i] > nums[j]）。

第二轮为什么只弹不压：第二轮的下标是「同一批元素的第二次出现」。
      它们作为**答案提供者**仍然有用（可以解决第一轮遗留在栈里的元素），
      但作为**待解决者**没有意义（第一轮已经把它们压进去过了）。
      如果第二轮还往栈里压，栈里会出现重复下标，结算时会写错 res。

复杂度：O(n) 时间 —— 2n 次迭代，每个下标最多入栈一次、出栈一次；O(n) 空间。
      虽然代码里有嵌套 while，但总 pop 次数 <= 总 push 次数 <= n，这是摊还（Amortized）分析。

边界：
  - 全递增 [1,2,3,4] → [2,3,4,-1]（最大值绕一圈也找不到）
  - 全递减 [4,3,2,1] → [-1,4,4,4]（后三个全靠第二轮回绕才找到 4）
  - 全相等 [2,2,2]   → [-1,-1,-1]（严格大于，等值不算）
  - 重复最大值 [5,4,5] → [-1,5,-1]
"""

from typing import List


##################################################################################################
##### ! Solution 1: 单调递减索引栈 + 两轮取模遍历（不复制数组）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：环形数组上的 Next Greater / Next Smaller 一律套这个
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def nextGreaterElements(self, nums: List[int]) -> List[int]:
        n = len(nums)
        res = [-1] * n
        stack: List[int] = []            # ! 存下标，对应值单调不增
        for i in range(2 * n):
            cur = nums[i % n]
            while stack and nums[stack[-1]] < cur:   # ! 严格小于才弹 → 找的是严格更大
                res[stack.pop()] = cur
            if i < n:                    # ! 只有第一轮才入栈，第二轮纯粹当“答案提供者”
                stack.append(i)
        return res


##################################################################################################
##### ! Solution 2: 复制成 2n 长度的数组再跑一次普通 Next Greater（最直观，空间翻倍）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：第一次学环形处理时用来建立直觉；面试里写 Solution_1 更好
##################################################################################################


class Solution_2:
    def nextGreaterElements(self, nums: List[int]) -> List[int]:
        n = len(nums)
        doubled = nums + nums            # ! 把环“展开”成一条链
        res = [-1] * n
        stack: List[int] = []
        for i, cur in enumerate(doubled):
            while stack and doubled[stack[-1]] < cur:
                j = stack.pop()
                if j < n:                # ! 只有前半段的下标才需要记答案
                    res[j] = cur
            stack.append(i)
        return res


##################################################################################################
##### ! Solution 3: 暴力 —— 每个 i 往后扫最多 n-1 步（基准答案，用来对拍）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(1)（不算输出）
##### ! 适用：n 很小时可以过；这里主要当正确性参照
##################################################################################################


class Solution_3:
    def nextGreaterElements(self, nums: List[int]) -> List[int]:
        n = len(nums)
        res = [-1] * n
        for i in range(n):
            for step in range(1, n):
                if nums[(i + step) % n] > nums[i]:
                    res[i] = nums[(i + step) % n]
                    break
        return res


if __name__ == "__main__":
    cases = [[1, 2, 1], [1, 2, 3, 4, 3], [1, 2, 3, 4], [4, 3, 2, 1], [2, 2, 2], [5, 4, 5], [1]]
    for nums in cases:
        a = Solution_1().nextGreaterElements(nums)
        b = Solution_2().nextGreaterElements(nums)
        c = Solution_3().nextGreaterElements(nums)
        assert a == b == c, (nums, a, b, c)
        print(f"{nums} -> {a}")
