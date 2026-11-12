"""LC-1130 - Minimum Cost Tree From Leaf Values

Level 1 · 03 单调栈与贪心构造 → Level 2 · 03 局部最小消除与合并代价
（intake 的单调栈铁律把它归到 18-monotonic；区间 DP 解法同样完整保留在下面，作为 12-DP Level 1·08 的参照）

题目在问：数组 `arr` 按顺序作为二叉树的叶子（中序），每个内部节点的值 = 左子树最大叶 × 右子树最大叶。求所有内部节点值之和的最小值。

### 区间 DP（教科书解）：枚举最后一刀切在哪

    dp[i][j] = 把 arr[i..j] 建成一棵树的最小内部节点和
    dp[i][j] = min over i <= m < j:  dp[i][m] + dp[m+1][j] + max(arr[i..m]) · max(arr[m+1..j])

和 LC-0312 Burst Balloons / LC-1547 Cut a Stick 一样：**根节点是最后合并的那一步**，所以枚举「根把区间切成左右两半」。
O(n³)，n ≤ 40 完全够。

### 贪心（更聪明的解）：每次合并相邻的最小叶

每次操作：拿掉数组里**最小的**元素 x，它和左右邻居中**较小**的那个 y 合并，代价 `x · y`。
为什么对？x 是全局最小，它迟早要和某个邻居相乘而被「吸收」（因为它小，之后的 max 永远不会是它）；
让它和较小的邻居合并，代价最小且不影响后续。O(n²)。

### 单调栈（最优解，O(n)）

把「每次删最小元素」变成一次扫描：维护**单调递减**栈；新元素 x 进来时，栈顶比 x 小的元素 t 要被弹出 ——
t 的两个邻居是 x 和新栈顶 `stack[-1]`，代价 `t · min(x, stack[-1])`。扫完后栈里剩下的递减序列相邻两两相乘。
这是「贪心 + 单调栈」的经典组合：**每个被弹出的元素 = 一个局部最小，弹出瞬间就知道它的两个邻居** —— 这就是它住在 18-monotonic 的理由；区间 DP 是它在 12-DP 那边的影子。
"""
from functools import lru_cache
from typing import List


##################################################################################################
##### ! Solution 1: 区间 DP，枚举根把区间切成左右
##### ! 时间复杂度: O(n³)   空间复杂度: O(n²)
##### ! 适用：面试标准答案（本层的教学主线）。预处理 mx[i][j] = max(arr[i..j]) 避免内层再扫
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def mctFromLeafValues(self, arr: List[int]) -> int:
        n = len(arr)
        mx = [[0] * n for _ in range(n)]
        for i in range(n):
            mx[i][i] = arr[i]
            for j in range(i + 1, n):
                mx[i][j] = max(mx[i][j - 1], arr[j])
        dp = [[0] * n for _ in range(n)]                # ! 单个叶子：没有内部节点，0
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                dp[i][j] = min(dp[i][m] + dp[m + 1][j] + mx[i][m] * mx[m + 1][j] for m in range(i, j))   # ! 根在 m|m+1 之间
        return dp[0][n - 1]


##################################################################################################
##### ! Solution 2: 贪心 —— 每次删最小元素，和较小的邻居合并
##### ! 时间复杂度: O(n²)   空间复杂度: O(n)
##### ! 适用：面试官追问「能不能比 n³ 快」的第一步；要能口述为什么最小元素可以立刻处理
##################################################################################################


class Solution_2:
    def mctFromLeafValues(self, arr: List[int]) -> int:
        a, res = arr[:], 0
        while len(a) > 1:
            i = a.index(min(a))                         # ! 全局最小
            left = a[i - 1] if i > 0 else float("inf")
            right = a[i + 1] if i + 1 < len(a) else float("inf")
            res += a[i] * min(left, right)              # ! 和较小的邻居合并
            a.pop(i)                                    # ! 它被吸收，不再影响 max
        return res


##################################################################################################
##### ! Solution 3: 单调递减栈，一次扫描
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：最优解。栈顶被弹出的 t 一定是「局部最小」，它的代价 = t × min(两个邻居)；
#####         哨兵 inf 放在栈底，省掉空栈判断
##################################################################################################


class Solution_3:
    def mctFromLeafValues(self, arr: List[int]) -> int:
        stack, res = [float("inf")], 0                  # ! 哨兵
        for x in arr:
            while stack[-1] <= x:                       # ! 栈顶 t 比 x 小：t 的邻居是 x 和新的栈顶
                t = stack.pop()
                res += t * min(x, stack[-1])
            stack.append(x)
        while len(stack) > 2:                           # ! 剩下递减序列，相邻相乘
            res += stack.pop() * stack[-1]
        return res


if __name__ == "__main__":
    import random
    cases = [([6, 2, 4], 32), ([4, 11], 44), ([1, 2, 3, 4], 20), ([5], 0), ([3, 1, 2, 4], 20)]
    for arr, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().mctFromLeafValues(arr)
            assert got == want, (cls.__name__, arr, got, want)
    rng = random.Random(1130)
    for _ in range(3000):
        arr = [rng.randint(1, 15) for _ in range(rng.randint(1, 8))]
        outs = [cls().mctFromLeafValues(arr) for cls in (Solution_1, Solution_2, Solution_3)]
        assert outs[0] == outs[1] == outs[2], (arr, outs)
    print("所有测试通过 ✓")
