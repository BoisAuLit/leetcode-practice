"""LC-2251 - Number of Flowers in Full Bloom

Level 1 · 04 重叠计数、扫描线与资源分配 → Level 2 · 02 差分事件与容量约束

题目在问：每朵花在 `[start, end]`（闭区间）开放；对每个到访时间 `t`，问当时有多少朵花开着。n、q 都到 5×10⁴，值域 10⁹。

### 决定性观察：开着的花数 = 「开始时间 ≤ t 的花」−「结束时间 < t 的花」

    answer(t) = #{start_i <= t} − #{end_i < t}

两个计数都是「有序数组里 ≤ / < 某值的个数」⟹ 把 starts 和 ends 分别排序，每个查询两次二分。
不需要扫描线、不需要把查询排序 —— 这是本题最优雅的点。

### 两处开闭

- `#{start <= t}` 用 `bisect_right(starts, t)`（≤）
- `#{end < t}` 用 `bisect_left(ends, t)`（<）—— 闭区间 `[s, e]` 在 t == e 时还开着，所以不能算成已结束
LC-0253 是半开区间 `[s, e)`，那里结束要用 `<=`。这两题放在一起就是「端点语义决定 bisect 方向」的教材。

### 对比：离线扫描线 / 差分

把查询排序后和事件一起扫（`Solution_2`）也是 O((n + q) log(n + q))，但要记录每个查询的原始下标再放回去 —— 代码更长，
只有当「查询的是区间上的聚合值而不是计数」时才非它不可。值域 10⁹ 不能用差分数组（`Solution_3` 用坐标压缩后的差分展示这一点）。
"""
from bisect import bisect_left, bisect_right
from typing import List


##################################################################################################
##### ! Solution 1: 两个排序数组 + 每个查询两次二分
##### ! 时间复杂度: O((n + q) log n)   空间复杂度: O(n)
##### ! 适用：面试标准答案。公式 #{start <= t} − #{end < t}；注意闭区间 ⟹ end 用 bisect_left
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def fullBloomFlowers(self, flowers: List[List[int]], people: List[int]) -> List[int]:
        starts = sorted(s for s, _ in flowers)
        ends = sorted(e for _, e in flowers)
        return [bisect_right(starts, t) - bisect_left(ends, t) for t in people]   # ! ≤ t 的开始 − < t 的结束


##################################################################################################
##### ! Solution 2: 离线扫描线（查询按时间排序，和事件一起扫）
##### ! 时间复杂度: O((n + q) log(n + q))   空间复杂度: O(n + q)
##### ! 适用：想复用 LC-0253 的扫描线模板时；闭区间 ⟹ 结束事件放在 end + 1，且同时刻先处理「开始」
##################################################################################################


class Solution_2:
    def fullBloomFlowers(self, flowers: List[List[int]], people: List[int]) -> List[int]:
        events = sorted([(s, 1) for s, _ in flowers] + [(e + 1, -1) for _, e in flowers])   # ! 闭区间 → 在 e+1 结束
        order = sorted(range(len(people)), key=lambda i: people[i])
        ans = [0] * len(people)
        cur = j = 0
        for i in order:
            t = people[i]
            while j < len(events) and events[j][0] <= t:        # ! 处理所有时刻 <= t 的事件
                cur += events[j][1]; j += 1
            ans[i] = cur
        return ans


##################################################################################################
##### ! Solution 3: 坐标压缩 + 差分数组 + 前缀和
##### ! 时间复杂度: O((n + q) log(n + q))   空间复杂度: O(n + q)
##### ! 适用：展示「值域太大时差分怎么办」：把所有出现过的坐标（start、end+1、查询 t）压缩成下标再差分。
#####         代码最长，面试里只在被问「差分数组能不能做」时提
##################################################################################################


class Solution_3:
    def fullBloomFlowers(self, flowers: List[List[int]], people: List[int]) -> List[int]:
        coords = sorted({x for s, e in flowers for x in (s, e + 1)} | set(people))
        idx = {x: i for i, x in enumerate(coords)}
        diff = [0] * (len(coords) + 1)
        for s, e in flowers:
            diff[idx[s]] += 1
            diff[idx[e + 1]] -= 1
        pref, cur = [], 0
        for d in diff[:-1]:
            cur += d; pref.append(cur)
        return [pref[idx[t]] for t in people]


def _brute(flowers, people):
    return [sum(1 for s, e in flowers if s <= t <= e) for t in people]


if __name__ == "__main__":
    import random
    cases = [([[1, 6], [3, 7], [9, 12], [4, 13]], [2, 3, 7, 11], [1, 2, 2, 2]),
             ([[1, 10], [3, 3]], [3, 3, 2], [2, 2, 1]),
             ([[5, 5]], [4, 5, 6], [0, 1, 0])]                      # ! 闭区间端点
    for f, p, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().fullBloomFlowers(f, p)
            assert got == want, (cls.__name__, f, p, got, want)
    rng = random.Random(2251)
    for _ in range(3000):
        f = []
        for _ in range(rng.randint(1, 8)):
            s = rng.randint(1, 20); f.append([s, rng.randint(s, 22)])
        p = [rng.randint(0, 24) for _ in range(rng.randint(1, 8))]
        want = _brute(f, p)
        for cls in (Solution_1, Solution_2, Solution_3):
            assert cls().fullBloomFlowers(f, p) == want, (cls.__name__, f, p)
    print("所有测试通过 ✓（样例 + 3000 随机对拍）")
