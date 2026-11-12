"""LC-0815 - Bus Routes

阶段 0 · 显式建图 —— **「点」选错就做不出来的典型题**
题目在问：每条公交路线是一个循环的车站序列。从 source 站到 target 站，
         最少需要**乘坐几条路线**（换乘次数 + 1）。

点是什么：**路线（bus route）**，不是车站！
边是什么：两条路线**共享至少一个车站** ⟹ 它们之间可以换乘 ⟹ 连一条边。

决定性观察（这题的全部价值）：
  1. **如果把车站当点，就跑偏了**：那样 BFS 的层数是「经过几个站」，
     而题目要的是「坐了几条线」。一条线上坐 10 站和坐 1 站，代价是一样的。
  2. **把路线当点**之后，BFS 的层数**恰好**就是乘坐的路线数 —— 问题立刻变成裸 BFS。
     **这就是「选对点」的威力。**
  3. 怎么建边：对每个车站，记下「哪些路线经过它」（`stop -> [route_ids]`）。
     同一个车站下的任意两条路线之间都可以换乘。
     **不要真的去两两连边**（最坏 O(n²) 条边）——
     BFS 时直接通过 `stop -> routes` 这张表跳转就行，这叫**隐式建图**。
  4. **每个车站只需要被「展开」一次**：一旦从某个车站把所有经过它的路线都入过队，
     以后再遇到这个车站就没有新信息了。
     所以要么标记 `visited_stops`，要么用完就把这个车站的列表清空 ——
     否则复杂度会退化。

```python
stop_to_routes = defaultdict(list)
for i, route in enumerate(routes):
    for s in route: stop_to_routes[s].append(i)

q = deque([(source, 0)]); seen_stops = {source}; seen_routes = set()
while q:
    stop, cnt = q.popleft()
    if stop == target: return cnt
    for r in stop_to_routes[stop]:
        if r in seen_routes: continue
        seen_routes.add(r)
        for nxt in routes[r]:
            if nxt not in seen_stops:
                seen_stops.add(nxt); q.append((nxt, cnt + 1))
```

**`source == target` 必须特判返回 0**（一辆车都不用坐）。

复杂度：设所有路线的车站总数为 N。
      建表 O(N)；BFS 中每条路线最多被展开一次、每个车站最多入队一次
      ⟹ **O(N)** 时间、O(N) 空间。
      不要说成 O(路线数²) —— 只要不真的两两连边，就不会有那个平方项。

和 LC-0127 Word Ladder 的关系：两题都在考「**点到底是什么**」。
      Word Ladder 的点是单词、边是「差一个字母」；
      本题的点是路线（或车站），边是「共享车站」。
      **建图题的第一步永远是：先问清楚点和边是什么。**

边界：
  - `source == target` → 0
  - target 不在任何路线上 → -1
  - 只有一条路线
  - 多条路线共享同一个车站
  - 路线之间完全不连通 → -1
"""

from collections import defaultdict, deque
from typing import List


##################################################################################################
##### ! Solution 1: 隐式建图 —— stop → routes 表 + BFS（层数 = 乘坐路线数）
##### ! 时间复杂度: O(N)（N = 所有路线的车站总数）   空间复杂度: O(N)
##### ! 适用：所有「换乘次数最少」类题；核心是把**路线**当点而不是车站
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def numBusesToDestination(self, routes: List[List[int]], source: int, target: int) -> int:
        if source == target:
            return 0                              # ! 必须特判
        stop_to_routes = defaultdict(list)
        for i, route in enumerate(routes):
            for s in route:
                stop_to_routes[s].append(i)       # ! 隐式建图：不两两连边
        if source not in stop_to_routes or target not in stop_to_routes:
            return -1
        q = deque([(source, 0)])
        seen_stops = {source}
        seen_routes = set()
        while q:
            stop, cnt = q.popleft()
            for r in stop_to_routes[stop]:
                if r in seen_routes:
                    continue                      # ! 每条路线只展开一次
                seen_routes.add(r)
                for nxt in routes[r]:
                    if nxt == target:
                        return cnt + 1
                    if nxt not in seen_stops:
                        seen_stops.add(nxt)
                        q.append((nxt, cnt + 1))
        return -1


##################################################################################################
##### ! Solution 2: 显式建「路线图」—— 路线之间两两判断是否共享车站，再 BFS
##### ! 时间复杂度: O(R^2 · L + N)（R = 路线数）   空间复杂度: O(R^2)
##### ! 适用：用来说明「把路线当点」这件事；但两两建边有平方项，R 大时不如 Solution_1
##################################################################################################


class Solution_2:
    def numBusesToDestination(self, routes: List[List[int]], source: int, target: int) -> int:
        if source == target:
            return 0
        n = len(routes)
        sets = [set(r) for r in routes]
        adj = defaultdict(list)
        for i in range(n):
            for j in range(i + 1, n):
                if sets[i] & sets[j]:             # ! 共享车站 ⟹ 可以换乘
                    adj[i].append(j)
                    adj[j].append(i)
        starts = [i for i in range(n) if source in sets[i]]
        if not starts:
            return -1
        q = deque((i, 1) for i in starts)         # ! 多源：所有经过 source 的路线
        seen = set(starts)
        while q:
            r, cnt = q.popleft()
            if target in sets[r]:
                return cnt
            for nb in adj[r]:
                if nb not in seen:
                    seen.add(nb)
                    q.append((nb, cnt + 1))
        return -1


if __name__ == "__main__":
    import random

    cases = [([[1, 2, 7], [3, 6, 7]], 1, 6, 2),
             ([[7, 12], [4, 5, 15], [6], [15, 19], [9, 12, 13]], 15, 12, -1),
             ([[1, 2, 3]], 1, 3, 1),
             ([[1, 2, 3]], 1, 1, 0),
             ([[1, 2], [3, 4]], 1, 4, -1),
             ([[1, 7], [3, 5]], 5, 5, 0)]
    for routes, s, t, want in cases:
        a = Solution_1().numBusesToDestination([r[:] for r in routes], s, t)
        b = Solution_2().numBusesToDestination([r[:] for r in routes], s, t)
        assert a == b == want, (routes, s, t, a, b, want)
        print(f"source={s}, target={t} -> {a}")

    for _ in range(800):                 # ! 随机对拍：隐式建图 == 显式路线图
        R = random.randint(1, 5)
        routes = [sorted(random.sample(range(0, 8), random.randint(1, 4))) for _ in range(R)]
        s, t = random.randint(0, 8), random.randint(0, 8)
        a = Solution_1().numBusesToDestination([r[:] for r in routes], s, t)
        b = Solution_2().numBusesToDestination([r[:] for r in routes], s, t)
        assert a == b, (routes, s, t, a, b)
    print("随机对拍 800 组通过 ✓（隐式 stop→routes == 显式路线两两建边）")
