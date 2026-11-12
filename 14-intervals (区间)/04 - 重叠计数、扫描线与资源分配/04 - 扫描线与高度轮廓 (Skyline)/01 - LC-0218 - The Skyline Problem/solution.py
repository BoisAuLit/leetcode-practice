"""LC-0218 - The Skyline Problem

Level 1 · 04 重叠计数、扫描线与资源分配 → Level 2 · 04 扫描线与高度轮廓 (Skyline)

题目在问：给一组矩形建筑 `[left, right, height]`，输出轮廓线的**关键点** `[x, y]`：每一个「最高高度发生变化」的横坐标及变化后的高度。

### 扫描线 + 最大堆：本层的集大成

LC-0253 的扫描线数「当前有几个区间」；本题数的是「当前**最高**的区间有多高」—— 把计数换成最大堆。

    事件：(left, -height, right) 进入   /   (right, 0, 0) 离开        # ! 按 x 排序
    扫到 x：把所有 left == x 的建筑入堆 (−h, right)
            弹掉堆顶所有 right <= x 的（懒删除：已经结束的建筑）
            当前高度 = −heap[0][0]（堆空则 0）
            如果和上一个输出的高度不同 → 输出 [x, 当前高度]

### 三个必须处理的 tie

1. **同一 x 既有开始又有结束**：先处理开始再处理结束（把开始事件排在前面）。否则会先输出一个「掉下去」再「升回来」的假关键点。
   把事件编码成 `(x, -h, r)` 开始、`(x, 0, 0)` 结束，按元组排序：开始事件的 `-h < 0` 自动排在结束事件的 `0` 前面。
2. **同一 x 多个开始**：高的先入堆（`-h` 小的先）—— 元组排序也顺带做到。
3. **同一 x 多个结束**：按任意顺序弹，最后再比较高度一次 —— 用「处理完这个 x 的所有事件再输出」保证。

### 懒删除

堆里不能直接删任意元素。离开事件不做删除，而是在**取堆顶时**检查 `right <= x` 就弹掉 —— 过期的建筑最终都会被弹掉，每个最多一次，总 O(n log n)。
"""
import heapq
from typing import List


##################################################################################################
##### ! Solution 1: 扫描线 + 最大堆 + 懒删除
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：面试标准答案。按唯一横坐标扫；每个 x 先入堆、再清过期、再比较高度
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        # ! 所有关键横坐标：每栋楼的 left 和 right
        xs = sorted({x for l, r, _ in buildings for x in (l, r)})
        buildings.sort()                                # ! 按 left 排，用指针 i 顺序入堆
        heap: List[tuple] = []                          # ! (-height, right)
        out: List[List[int]] = []
        i = 0
        for x in xs:
            while i < len(buildings) and buildings[i][0] == x:   # ! 所有在 x 开始的楼入堆
                l, r, h = buildings[i]
                heapq.heappush(heap, (-h, r)); i += 1
            while heap and heap[0][1] <= x:             # ! 懒删除：堆顶已经结束的楼
                heapq.heappop(heap)
            h = -heap[0][0] if heap else 0
            if not out or out[-1][1] != h:              # ! 高度变了才是关键点
                out.append([x, h])
        return out


##################################################################################################
##### ! Solution 2: 事件元组 (x, -h, r) / (x, 0, 0) 一次排序，逐事件处理
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：另一种组织：把「开始」和「结束」都编码成事件，排序后的元组顺序自动解决全部 tie；
#####         输出前检查「下一个事件是否同 x」避免同一 x 输出两次
##################################################################################################


class Solution_2:
    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        events = sorted([(l, -h, r) for l, r, h in buildings] + [(r, 0, 0) for _, r, _ in buildings])
        heap = [(0, float("inf"))]                      # ! 地面：高度 0，永不结束
        out = []
        for idx, (x, neg_h, r) in enumerate(events):
            if neg_h:
                heapq.heappush(heap, (neg_h, r))        # ! 开始事件
            while heap[0][1] <= x:                      # ! 懒删除
                heapq.heappop(heap)
            if idx + 1 < len(events) and events[idx + 1][0] == x:
                continue                                # ! 同一 x 还有事件没处理完，先不输出
            h = -heap[0][0]
            if not out or out[-1][1] != h:
                out.append([x, h])
        return out


##################################################################################################
##### ! Solution 3: 分治合并（归并排序式）—— 两条轮廓线合并成一条
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：面试官追问「不用堆」时。合并两条轮廓：双指针按 x 推进，当前高度 = max(左当前高, 右当前高)，
#####         高度变化时输出。和归并排序的 merge 完全同构
##################################################################################################


class Solution_3:
    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        def merge(a, b):
            out, i, j, ha, hb = [], 0, 0, 0, 0
            while i < len(a) and j < len(b):
                if a[i][0] < b[j][0]:
                    x, ha = a[i]; i += 1
                elif a[i][0] > b[j][0]:
                    x, hb = b[j]; j += 1
                else:
                    x, ha = a[i]; hb = b[j][1]; i += 1; j += 1
                h = max(ha, hb)
                if not out or out[-1][1] != h:
                    out.append([x, h])
            out += a[i:] + b[j:]
            return out

        def solve(lo, hi):
            if lo == hi:
                l, r, h = buildings[lo]
                return [[l, h], [r, 0]]
            mid = (lo + hi) // 2
            return merge(solve(lo, mid), solve(mid + 1, hi))

        return solve(0, len(buildings) - 1)


def _brute(buildings):
    """按定义：对每个关键 x 直接求覆盖它的最高楼（O(n²)），真值基线。"""
    xs = sorted({x for l, r, _ in buildings for x in (l, r)})
    out = []
    for x in xs:
        h = max((hh for l, r, hh in buildings if l <= x < r), default=0)
        if not out or out[-1][1] != h:
            out.append([x, h])
    return out


if __name__ == "__main__":
    import random
    cases = [
        ([[2, 9, 10], [3, 7, 15], [5, 12, 12], [15, 20, 10], [19, 24, 8]],
         [[2, 10], [3, 15], [7, 12], [12, 0], [15, 10], [20, 8], [24, 0]]),
        ([[0, 2, 3], [2, 5, 3]], [[0, 3], [5, 0]]),                     # ! 等高相接：中间不是关键点
        ([[1, 2, 1], [1, 2, 2], [1, 2, 3]], [[1, 3], [2, 0]]),
        ([[0, 5, 7], [5, 10, 7], [5, 10, 12], [10, 15, 7], [15, 20, 7], [15, 20, 12], [20, 25, 7]],
         [[0, 7], [5, 12], [10, 7], [15, 12], [20, 7], [25, 0]]),
    ]
    for b, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().getSkyline([x[:] for x in b])
            assert got == want, (cls.__name__, b, got, want)
    rng = random.Random(218)
    for _ in range(2000):
        b = []
        for _ in range(rng.randint(1, 8)):
            l = rng.randint(0, 12); r = rng.randint(l + 1, 14); b.append([l, r, rng.randint(1, 6)])
        want = _brute(b)
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().getSkyline([x[:] for x in b])
            assert got == want, (cls.__name__, b, got, want)
    print("所有测试通过 ✓（样例 + 2000 随机对拍）")
