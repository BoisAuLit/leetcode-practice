"""LC-0630 - Course Schedule III

Level 1 · 04 Heap + Greedy 资源优化与选择 → Level 2 · 02 有限资源的最优分配

题目在问：每门课 `[duration, lastDay]`，必须在 `lastDay` 前连续上完，不能并行；最多能修几门。

### 两个贪心叠在一起 + 一个「反悔」堆

1. **按 lastDay 排序**：先考虑截止早的（和 LC-0435 一样的交换论证 —— 如果最优解里有一门截止晚的排在截止早的前面，交换它们不会变差）。
2. 顺序尝试加入每门课，`time += duration`；如果 `time > lastDay`，说明放不下 ——
   **反悔**：把已选课程里**耗时最长的那门**踢掉（最大堆的堆顶）。
   踢掉最长的一定不会更差：课程数不变（换掉一门），而总耗时变小，给后面留更多空间。

注意：被踢的可能就是刚加入的这门（它自己最长）—— 那等价于「不选它」。统一处理不用特判。

### 为什么不是 DP

n ≤ 10⁴、lastDay ≤ 10⁴，DP `dp[i][t]` 是 10⁸，太大。
反悔贪心把它压到 O(n log n)，这是它成为经典的原因 —— 和 LC-1642 Furthest Building（把「用梯子」反悔成「用砖」）同一家族。

### 最朴素的正确版本（对照）

`Solution_3` 对 n ≤ 12 枚举子集：按 lastDay 排序后依次上，检查可行性。它只用来对拍，但也揭示一个事实：
**在任何子集内部，按 lastDay 排序就是最优上课顺序** —— 所以枚举「选哪些」时顺序不用再枚举。
"""
import heapq
from typing import List


##################################################################################################
##### ! Solution 1: 按截止日排序 + 最大堆反悔
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：面试标准答案。堆里存 -duration；超时就弹堆顶（最长的那门）并把它的时长从 time 里减掉
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def scheduleCourse(self, courses: List[List[int]]) -> int:
        courses.sort(key=lambda c: c[1])                # ! 截止早的先考虑
        heap: List[int] = []                            # ! 已选课程的 -duration（最大堆）
        time = 0
        for d, last in courses:
            heapq.heappush(heap, -d)
            time += d
            if time > last:                             # ! 放不下：踢掉最长的（可能就是自己）
                time += heapq.heappop(heap)             # ! 弹出的是负数，加上去等于减掉时长
        return len(heap)


##################################################################################################
##### ! Solution 2: 同一贪心，但先判断再入堆（少一次无用的 push/pop）
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：把「替换」写成显式分支：放得下就放；放不下且堆顶比我长就换掉它；否则跳过。
#####         和 Solution_1 等价，只是把「踢掉自己」这种情况提前短路
##################################################################################################


class Solution_2:
    def scheduleCourse(self, courses: List[List[int]]) -> int:
        courses.sort(key=lambda c: c[1])
        heap: List[int] = []
        time = 0
        for d, last in courses:
            if time + d <= last:                        # ! 放得下
                heapq.heappush(heap, -d); time += d
            elif heap and -heap[0] > d:                 # ! 放不下但有更长的可以换
                time += heapq.heapreplace(heap, -d) + d  # ! 弹出 -longest、放入 -d：time 减 longest 加 d
        return len(heap)


##################################################################################################
##### ! Solution 3: 枚举子集（真值基线，n ≤ 12）
##### ! 时间复杂度: O(2^n · n)   空间复杂度: O(n)
##### ! 适用：只用来对拍。子集内部按 lastDay 排序依次上，检查每门都不超期
##################################################################################################


class Solution_3:
    def scheduleCourse(self, courses: List[List[int]]) -> int:
        cs = sorted(courses, key=lambda c: c[1])
        n, best = len(cs), 0
        for mask in range(1 << n):
            t, ok, cnt = 0, True, 0
            for i in range(n):
                if mask >> i & 1:
                    t += cs[i][0]; cnt += 1
                    if t > cs[i][1]:
                        ok = False; break
            if ok:
                best = max(best, cnt)
        return best


if __name__ == "__main__":
    import random
    cases = [([[100, 200], [200, 1300], [1000, 1250], [2000, 3200]], 3), ([[1, 2]], 1), ([[3, 2], [4, 3]], 0),
             ([[5, 5], [4, 6], [2, 6]], 2), ([[7, 17], [3, 12], [10, 20], [9, 10], [5, 20], [10, 19], [4, 18]], 4)]
    for c, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().scheduleCourse([x[:] for x in c])
            assert got == want, (cls.__name__, c, got, want)
    rng = random.Random(630)
    for _ in range(1500):
        c = [[rng.randint(1, 8), rng.randint(1, 20)] for _ in range(rng.randint(1, 10))]
        want = Solution_3().scheduleCourse([x[:] for x in c])
        for cls in (Solution_1, Solution_2):
            assert cls().scheduleCourse([x[:] for x in c]) == want, (cls.__name__, c)
    print("所有测试通过 ✓（样例 + 1500 随机对拍）")
