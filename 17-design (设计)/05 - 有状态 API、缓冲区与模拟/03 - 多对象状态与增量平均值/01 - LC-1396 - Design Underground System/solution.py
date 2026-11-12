"""LC-1396 - Design Underground System

Level 1 · 05 有状态 API、缓冲区与模拟 —— **在途对象 + 增量聚合（Incremental Aggregation）**
API：
  - `checkIn(id, stationName, t)`：乘客 `id` 在 `t` 时刻从 `stationName` 进站
  - `checkOut(id, stationName, t)`：乘客 `id` 在 `t` 时刻从 `stationName` 出站
  - `getAverageTime(startStation, endStation) -> float`：
    返回**所有**从 `start` 到 `end` 的行程的平均耗时
全部操作要求 **O(1)**。

---

## 决定性观察：两张表，各管一件事

```python
self.in_transit = {}      # ! id -> (进站名, 进站时间)        —— 「在途」的乘客
self.totals = {}          # ! (起点, 终点) -> [累计总时长, 行程次数]  —— 聚合结果
```

| 表 | 生命周期 | 大小 |
|---|---|---|
`in_transit` | `checkIn` 加入，`checkOut` **立即删除** | O(当前在途人数) |
`totals` | 只增不减 | O(不同站点对数) |

**关键**：`getAverageTime` **不遍历任何历史记录** ——
它只做一次字典查找和一次除法：

```python
total, count = self.totals[(start, end)]
return total / count
```

### 为什么能 O(1) 求平均值？—— Incremental Aggregation

**不要存所有行程的时长列表**（那样求平均是 O(k)）。
只存**两个标量**：`sum` 和 `count`。
每次 `checkOut` 时 `sum += duration; count += 1`（**O(1)**），
查询时 `sum / count`（**O(1)**）。

> **这是本题真正要教的东西**：
> **平均值可以增量维护** —— 因为 `avg = sum / count`，而 `sum` 和 `count` 都可增量。
> 同样的技巧适用于「总和、计数、最大值、最小值」。
> ❌ **不适用于中位数、分位数**（那需要有序结构，见 `09-heap` 的双堆）。

---

## 三个必须想清的点

### ① 为什么 `checkOut` 必须**立即删除** `in_transit[id]`？

同一个乘客 `id` 会**反复**乘车（题目保证一个乘客不会同时在两段行程中，
但会先后多次乘车）。不删除的话，下一次 `checkIn` 会覆盖，
看起来「也能跑对」，但：
- `in_transit` 会**无限增长**（内存泄漏）
- 一旦题目变体允许「查询当前在途人数」，答案就错了

**删除是语义正确，不只是省内存。**

### ② 为什么 key 必须是 `(起点, 终点)` 的**有序对**？

`getAverageTime("A", "B")` 和 `getAverageTime("B", "A")` 是**两个不同的查询**
（地铁有方向，耗时可能不同）。
用 `frozenset({A, B})` 或排序后的元组当 key ⟹ **两个方向被混在一起** ⟹ 答案错。

### ③ 为什么不需要处理「进站和出站是同一个站」？

题目保证 `checkIn` / `checkOut` 成对出现，但**没说**起点终点不同。
`("A", "A")` 是合法的 key（乘客进站又从同一站出来）。
公式天然支持，**不需要特判**。

---

## 为什么 `in_transit` 用 `id` 当 key（而不是别的）

**不变量**：
> 任意时刻，`id in self.in_transit` ⟺ 乘客 `id` 已 `checkIn` 但尚未 `checkOut`。

题目保证「一个乘客在 `checkOut` 之前不会再 `checkIn`」
⟹ 一个 `id` 最多对应**一条**在途记录 ⟹ 字典（而不是列表）就够了。∎

---

## 和本 Level 1 其他题的共同主题

| 题 | 跨调用的状态 | 聚合方式 |
|---|---|---|
| [LC-0158 read4 II](<../../01 - Buffered Reader 与跨调用状态/02 - LC-0158 - Read N Characters Given read4 II - Call Multiple Times>) | 未交付的缓冲字符 | 无 |
| [LC-0348 Tic-Tac-Toe](<../../02 - 棋盘状态与历史导航/01 - LC-0348 - Design Tic-Tac-Toe>) | 每行/列/对角线的计数 | **增量计数**（落子时 ±1） |
| [LC-1472 Browser History](<../../02 - 棋盘状态与历史导航/02 - LC-1472 - Design Browser History>) | 历史栈 + 游标 | 无 |
| **LC-1396** 本题 | 在途乘客 + 每条线路的 (sum, count) | **增量平均值** |

> **LC-0348 和 LC-1396 是同一个思想**：
> **把「查询时才算」改成「更新时就算」。**
> LC-0348 不去扫整个棋盘判胜负，而是维护每行/列的计数；
> 本题不去遍历历史行程，而是维护 sum 和 count。
> **这是所有 O(1) 查询设计题的共同套路。**

---

复杂度：

| 操作 | 时间 | 说明 |
|---|---|---|
| `checkIn` | **O(1)** 平均 | 一次字典写 |
| `checkOut` | **O(1)** 平均 | 一次字典读 + 删除 + 一次聚合更新 |
| `getAverageTime` | **O(1)** 平均 | 一次字典读 + 一次除法 |
| 空间 | **O(P + S²)** | `P` = 在途人数，`S²` = 实际出现过的站点对数 |

⚠️ 是「**平均** O(1)」（哈希表），不是最坏 O(1)。
⚠️ 空间**不是** O(总行程数) —— 这正是增量聚合的收益。

边界：
  - 同一乘客**多次**乘车 → `in_transit` 必须每次清掉
  - 同一条线路**多段**行程 → sum / count 累加
  - **方向相反**的两条线路 → 必须是两个独立 key
  - 起点 == 终点 → 合法，不特判
  - 只有一段行程 → 平均值就是它本身
  - 耗时为 0（`checkIn` 和 `checkOut` 同一时刻）→ 合法
  - 题目保证只查询已存在的线路 ⟹ 不需要处理 KeyError（但本实现仍返回 0.0 兜底）
"""

from collections import defaultdict


##################################################################################################
##### ! Solution 1: 在途表 + (sum, count) 增量聚合，全部操作 O(1)
##### ! 时间复杂度: 三个操作均 O(1) 平均   空间复杂度: O(在途人数 + 站点对数)
##### ! 适用：所有「流式数据要 O(1) 查平均/总和/计数」的设计题
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class UndergroundSystem_1:
    def __init__(self):
        self.in_transit = {}                       # ! id -> (进站名, 进站时间)
        self.totals = defaultdict(lambda: [0, 0])  # ! (起点, 终点) -> [总时长, 次数]

    def checkIn(self, id: int, stationName: str, t: int) -> None:
        self.in_transit[id] = (stationName, t)

    def checkOut(self, id: int, stationName: str, t: int) -> None:
        start, t0 = self.in_transit.pop(id)        # ! pop：读取 + 立即删除（语义正确）
        entry = self.totals[(start, stationName)]  # ! key 是有序对，方向不能混
        entry[0] += t - t0                         # ! 增量累加总时长
        entry[1] += 1                              # ! 增量累加次数

    def getAverageTime(self, startStation: str, endStation: str) -> float:
        total, count = self.totals[(startStation, endStation)]
        return total / count if count else 0.0     # ! O(1)：一次除法，不遍历历史


##################################################################################################
##### ! Solution 2: 同上，但把聚合拆成两个独立字典（更显式，便于讲解）
##### ! 时间复杂度: 三个操作均 O(1) 平均   空间复杂度: 同上
##### ! 适用：想明确看到「sum 和 count 各自增量维护」时
##################################################################################################


class UndergroundSystem_2:
    def __init__(self):
        self.in_transit = {}
        self.sum_time = defaultdict(int)           # ! (起点, 终点) -> 总时长
        self.trip_count = defaultdict(int)         # ! (起点, 终点) -> 行程数

    def checkIn(self, id: int, stationName: str, t: int) -> None:
        self.in_transit[id] = (stationName, t)

    def checkOut(self, id: int, stationName: str, t: int) -> None:
        start, t0 = self.in_transit.pop(id)
        key = (start, stationName)
        self.sum_time[key] += t - t0
        self.trip_count[key] += 1

    def getAverageTime(self, startStation: str, endStation: str) -> float:
        key = (startStation, endStation)
        c = self.trip_count[key]
        return self.sum_time[key] / c if c else 0.0


##################################################################################################
##### ! Solution 3: 朴素基准（存下每段行程的时长列表，查询时才求平均）
##### ! 时间复杂度: checkIn/Out O(1)，getAverageTime **O(k)**   空间复杂度: O(总行程数)
##### ! 适用：仅用于对拍。对比之下能看清增量聚合省掉的是什么
##################################################################################################


class UndergroundSystem_3:
    def __init__(self):
        self.in_transit = {}
        self.durations = defaultdict(list)         # ! (起点, 终点) -> [每段行程的时长...]

    def checkIn(self, id: int, stationName: str, t: int) -> None:
        self.in_transit[id] = (stationName, t)

    def checkOut(self, id: int, stationName: str, t: int) -> None:
        start, t0 = self.in_transit.pop(id)
        self.durations[(start, stationName)].append(t - t0)

    def getAverageTime(self, startStation: str, endStation: str) -> float:
        lst = self.durations[(startStation, endStation)]
        return sum(lst) / len(lst) if lst else 0.0   # ! O(k) —— 这就是要优化掉的部分


if __name__ == "__main__":
    import random

    for cls in (UndergroundSystem_1, UndergroundSystem_2, UndergroundSystem_3):
        s = cls()
        # ! LeetCode 官方样例
        s.checkIn(45, "Leyton", 3)
        s.checkIn(32, "Paradise", 8)
        s.checkIn(27, "Leyton", 10)
        s.checkOut(45, "Waterloo", 15)      # Leyton -> Waterloo: 12
        s.checkOut(27, "Waterloo", 20)      # Leyton -> Waterloo: 10
        s.checkOut(32, "Cambridge", 22)     # Paradise -> Cambridge: 14
        assert abs(s.getAverageTime("Paradise", "Cambridge") - 14.0) < 1e-9
        assert abs(s.getAverageTime("Leyton", "Waterloo") - 11.0) < 1e-9
        s.checkIn(10, "Leyton", 24)
        s.checkOut(10, "Waterloo", 38)      # Leyton -> Waterloo: 14
        assert abs(s.getAverageTime("Leyton", "Waterloo") - 12.0) < 1e-9

        # ! 方向相反必须是两条独立线路
        d = cls()
        d.checkIn(1, "A", 0); d.checkOut(1, "B", 10)      # A->B: 10
        d.checkIn(2, "B", 0); d.checkOut(2, "A", 100)     # B->A: 100
        assert abs(d.getAverageTime("A", "B") - 10.0) < 1e-9
        assert abs(d.getAverageTime("B", "A") - 100.0) < 1e-9

        # ! 起点 == 终点；耗时为 0
        e = cls()
        e.checkIn(1, "A", 5); e.checkOut(1, "A", 5)
        assert abs(e.getAverageTime("A", "A") - 0.0) < 1e-9

        # ! 同一乘客多次乘车
        m = cls()
        for k in range(3):
            m.checkIn(7, "X", k * 10)
            m.checkOut(7, "Y", k * 10 + 2 * (k + 1))
        assert abs(m.getAverageTime("X", "Y") - (2 + 4 + 6) / 3) < 1e-9
        assert 7 not in m.in_transit            # ! checkOut 后必须清掉在途记录

    s = UndergroundSystem_1()
    s.checkIn(45, "Leyton", 3); s.checkOut(45, "Waterloo", 15)
    s.checkIn(27, "Leyton", 10); s.checkOut(27, "Waterloo", 20)
    print("Leyton -> Waterloo 平均耗时 =", s.getAverageTime("Leyton", "Waterloo"), "((12+10)/2)")

    for _ in range(2000):                       # ! 随机对拍
        stations = ["A", "B", "C"]
        ops = []
        active = {}
        t = 0
        for _ in range(random.randint(1, 30)):
            t += random.randint(0, 5)
            if active and random.random() < 0.5:
                pid = random.choice(list(active))
                ops.append(("out", pid, random.choice(stations), t))
                del active[pid]
            else:
                pid = random.randint(1, 5)
                if pid in active:
                    continue
                active[pid] = True
                ops.append(("in", pid, random.choice(stations), t))
        queries = [(a, b) for a in stations for b in stations]
        outs = []
        for cls in (UndergroundSystem_1, UndergroundSystem_2, UndergroundSystem_3):
            s = cls()
            for op, pid, st, tt in ops:
                if op == "in":
                    s.checkIn(pid, st, tt)
                else:
                    s.checkOut(pid, st, tt)
            outs.append([round(s.getAverageTime(a, b), 9) for a, b in queries])
        assert outs[0] == outs[1] == outs[2], (ops, outs)
    print("随机对拍 2000 组通过 ✓（增量 (sum,count) == 双字典版 == 存列表再求平均）")
