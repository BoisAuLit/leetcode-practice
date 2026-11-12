"""LC-1057 - Campus Bikes

Level 1 · 04 Heap + Greedy 资源优化与选择 → Level 2 · 04 排序与 Heap 的组合选择

题目在问：n 个工人、m ≥ n 辆车，二维网格上的曼哈顿距离。反复做：在所有「未分配的 (工人, 车)」里取**距离最小**的一对
（并列时工人下标小优先，再车下标小优先），分配之，直到每个工人都有车。输出每个工人分到的车。

### 这是「按规则定义的贪心」：顺序由题目钦定，算法只负责**高效地按这个顺序枚举**

所有 n·m 对（≤ 10⁶）按 `(dist, worker, bike)` 排序，然后顺序扫：工人和车都没被用过就配对。
正确性不需要证明 —— 题目就是这么定义的；考点是**怎么排得快**。

### 三档速度

| 解法 | 排序 | 说明 |
|---|---|---|
| 全排序 | O(nm log(nm)) | 一行 sort，10⁶ 个三元组在 Python 里约 1–2 秒，刚好能过 |
| **桶排序** | **O(nm + D)** | 距离 ≤ 2000（坐标 < 1000），按距离开 2001 个桶；桶内按 (worker, bike) 顺序生成就自然有序 |
| 堆 + 每个工人一个指针 | O(nm log n) 最坏，平均好得多 | 每个工人先把**自己最近**的车放进堆；堆顶的车若已被占，这个工人推进到下一近的车再入堆 |

桶排序是本题的「aha」：**距离是小整数 ⟹ 不需要比较排序**。第三种是 K-way merge 的思想（每个工人是一路有序流），面试里当 follow-up。
"""
import heapq
from typing import List


##################################################################################################
##### ! Solution 1: 按距离桶排序，桶内天然按 (worker, bike) 有序
##### ! 时间复杂度: O(n·m + D)（D = 最大距离 ≤ 2000）   空间复杂度: O(n·m)
##### ! 适用：面试最优答案。双重循环按 worker 外层、bike 内层生成 ⟹ 每个桶里的顺序已经是 (worker, bike) 字典序
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def assignBikes(self, workers: List[List[int]], bikes: List[List[int]]) -> List[int]:
        buckets = [[] for _ in range(2001)]             # ! 坐标 < 1000 ⟹ 曼哈顿距离 ≤ 1998
        for i, (wx, wy) in enumerate(workers):
            for j, (bx, by) in enumerate(bikes):        # ! i 外 j 内 → 桶内顺序 = (i, j) 字典序
                buckets[abs(wx - bx) + abs(wy - by)].append((i, j))
        ans = [-1] * len(workers)
        used_bike = [False] * len(bikes)
        left = len(workers)
        for bucket in buckets:
            for i, j in bucket:
                if ans[i] == -1 and not used_bike[j]:
                    ans[i] = j; used_bike[j] = True; left -= 1
                    if left == 0:
                        return ans
        return ans


##################################################################################################
##### ! Solution 2: 全部 (dist, i, j) 三元组排序后顺序扫
##### ! 时间复杂度: O(n·m log(n·m))   空间复杂度: O(n·m)
##### ! 适用：面试「第一版」：最直白地把题面翻译成代码。能过，但追问「更快」时要能说出桶排序
##################################################################################################


class Solution_2:
    def assignBikes(self, workers: List[List[int]], bikes: List[List[int]]) -> List[int]:
        pairs = sorted((abs(wx - bx) + abs(wy - by), i, j)
                       for i, (wx, wy) in enumerate(workers) for j, (bx, by) in enumerate(bikes))
        ans = [-1] * len(workers)
        used = set()
        for _, i, j in pairs:
            if ans[i] == -1 and j not in used:
                ans[i] = j; used.add(j)
        return ans


##################################################################################################
##### ! Solution 3: 堆 + 每个工人一条按距离排好的候选流（K-way merge 思想）
##### ! 时间复杂度: O(n·m log m + n·m log n) 最坏，实际远小于全排序   空间复杂度: O(n·m)
##### ! 适用：追问「不想一次性生成全部 n·m 对」。每个工人把自己的车按 (dist, j) 排好；
#####         堆里每个工人只放「当前最近的未试过的车」；弹出时若车已被占，这个工人推进到下一辆再入堆
##################################################################################################


class Solution_3:
    def assignBikes(self, workers: List[List[int]], bikes: List[List[int]]) -> List[int]:
        order = []                                       # ! order[i] = 工人 i 的车按 (dist, j) 排好
        for wx, wy in workers:
            order.append(sorted((abs(wx - bx) + abs(wy - by), j) for j, (bx, by) in enumerate(bikes)))
        ptr = [0] * len(workers)
        heap = [(order[i][0][0], i, order[i][0][1]) for i in range(len(workers))]   # ! (dist, worker, bike)
        heapq.heapify(heap)
        ans = [-1] * len(workers)
        used = [False] * len(bikes)
        while heap:
            d, i, j = heapq.heappop(heap)
            if used[j]:                                  # ! 这辆被抢了：工人 i 换下一辆再排队
                ptr[i] += 1
                nd, nj = order[i][ptr[i]]
                heapq.heappush(heap, (nd, i, nj))
            else:
                ans[i] = j; used[j] = True
        return ans


if __name__ == "__main__":
    import random
    cases = [([[0, 0], [2, 1]], [[1, 2], [3, 3]], [1, 0]),
             ([[0, 0], [1, 1], [2, 0]], [[1, 0], [2, 2], [2, 1]], [0, 2, 1])]
    for w, b, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().assignBikes(w, b)
            assert got == want, (cls.__name__, w, b, got, want)
    rng = random.Random(1057)
    for _ in range(1500):
        n = rng.randint(1, 6); m = rng.randint(n, 8)
        pts = rng.sample([(x, y) for x in range(8) for y in range(8)], n + m)   # ! 题目保证坐标两两不同
        w = [list(p) for p in pts[:n]]; b = [list(p) for p in pts[n:]]
        outs = [cls().assignBikes(w, b) for cls in (Solution_1, Solution_2, Solution_3)]
        assert outs[0] == outs[1] == outs[2], (w, b, outs)
    print("所有测试通过 ✓（样例 + 1500 随机对拍）")
