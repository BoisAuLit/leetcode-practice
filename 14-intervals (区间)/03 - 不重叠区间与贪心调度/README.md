# Level 1 · 03 — 不重叠区间与贪心调度（Interval Scheduling / Earliest Finish Time Greedy）

> **本层的统一目标：从一堆区间里「选」或「扎」—— 答案是一个计数，不是区间列表。**
> 本层只有**一个**算法：**按 end 升序排序 + 贪心**。
> 三道题是同一个贪心的三种提问方式。

---

## 核心定义

| 术语 | 定义 |
|---|---|
| **Interval Scheduling** | 经典调度问题：从相互冲突的区间里选出最多的互不冲突子集 |
| **Earliest Finish Time（最早结束时间）** | 贪心的选择规则：**总是选结束最早的那个兼容区间** |
| **Maximum Compatible Intervals** | 最大互不相交子集的大小，记作 `k` |
| **Minimum Removals** | 要删掉的最少个数 = `n - k` |
| **Minimum Covering Points** | 扎破所有区间所需的最少点数 = **`k`** |
| **Conflict Detection** | 只问「有没有冲突」，不需要计数 |

---

## 一个决定性观察（本层的全部内容）

### 三道题是同一个贪心，只是「数什么」不同

| 题 | 问题 | 答案 |
|---|---|---|
| [LC-0252 Meeting Rooms](<./01 - 冲突检测与最大兼容区间数量/01 - LC-0252 - Meeting Rooms>) | 所有区间能否互不冲突？ | `k == n` |
| [LC-0435 Non-overlapping Intervals](<./01 - 冲突检测与最大兼容区间数量/02 - LC-0435 - Non-overlapping Intervals>) | 最少删几个才能互不重叠？ | **`n - k`** |
| [LC-0452 Minimum Arrows](<./02 - 最少覆盖点与区间射击/01 - LC-0452 - Minimum Number of Arrows to Burst Balloons>) | 最少几支箭扎破全部？ | **`k`** |

其中 `k` = 最大互不相交子集的大小，**三题都由同一个贪心算出**。

**为什么「最多能选出 k 个互不重叠的区间」= 「需要 k 支箭」？**
- 选出的 `k` 个区间两两不相交 ⟹ 一支箭最多扎破其中一个 ⟹ **至少需要 k 支箭**（下界）。
- 贪心把箭放在每个选中区间的 end 上，恰好 `k` 支就扎破了所有区间（上界，见下面的证明）。
- 两边一夹 ⟹ 答案就是 `k`。∎

> **看穿这一点，这三道题就只剩一道。**

---

## 核心不变量

> 按 end 升序扫描时，`last_end` 是**已选中的区间中最大的 end**（也就是最后一个选中的区间的 end）。
> 不变量：**`last_end` 是「在已处理的区间上取得最大兼容数」的所有方案里，可能达到的最小值。**

「最小的 `last_end`」= **给后面留下最多空间** ⟹ 后续能选的区间不会变少。

对 LC-0452，等价的不变量是：
> `arrow_x` 是最后一支箭的位置，且它**尽可能地靠右**（在不漏掉任何已处理区间的前提下）。

---

## 为什么排序键是 **end 升序**（不是 start）

**这是本层唯一的失败模式。**

| 排序键 | `[[1,100],[2,3],[3,4]]` 的结果 | 正确答案 |
|---|---|---|
| **end 升序** ✅ | 选 `[2,3]`、`[3,4]` ⟹ `k=2` | `k=2` |
| start 升序 ❌ | 先占 `[1,100]`，后面都冲突 ⟹ `k=1` | ❌ |
| 长度升序 ❌ | 在某些构造下失败 | ❌ |

**直觉**：按 start 排会让一个「又早开始又特别长」的区间抢到位置，挤掉后面很多个。
按 end 排则保证每次「用掉的时间轴最少」。

### 交换论证（Exchange Argument）

**命题**：存在一个最优解，它包含「end 最小的那个区间」`x`。

**证明**：取任意最优解 `S`（`|S| = k`，互不相交）。
- 若 `x ∈ S`，完成。
- 若 `x ∉ S`，设 `y` 是 `S` 中 end 最小的区间。因为 `x` 是全局 end 最小 ⟹ `x.end <= y.end`。
  构造 `S' = S \ {y} ∪ {x}`。
  `S'` 仍然互不相交：`S` 中除 `y` 以外的区间 `z` 都满足 `z.start >= y.end >= x.end`
  （因为 `y` 是 `S` 里 end 最小的，其余区间都在它右边）⟹ `z` 与 `x` 不相交。
  且 `|S'| = |S| = k` ⟹ `S'` 也是最优解，且包含 `x`。∎

**归纳**：取定 `x` 后，删掉所有与 `x` 相交的区间，对剩下的子问题重复同一论证
⟹ 贪心逐步构造出的解是最优的。∎

### LC-0452：为什么把箭放在「最早结束的位置」？

**命题**：存在一个最优解，它的某支箭正好打在「end 最小的区间」`x` 的 `x.end` 上。

**证明**：`x` 必须被某支箭 `p` 扎破 ⟹ `x.start <= p <= x.end`。
把这支箭**右移到 `x.end`**：任何原本被 `p` 扎破的区间 `z` 满足 `z.start <= p <= z.end`。
因为 `x.end` 是全局最小的 end，且 `z.end >= p`，又 `z` 与 `x` 都被 `p` 穿过
⟹ `z.start <= p <= x.end <= z.end` ⟹ `z` **仍然**被 `x.end` 扎破。
所以右移不会丢任何区间，箭数不变 ⟹ 存在最优解把箭放在 `x.end`。∎

> **推论**：把箭放在 end 上是「免费的最优选择」—— 能扎的都还能扎，还顺带往右推到了极限。

---

## 当前选择规则

```python
# LC-0435 / LC-0452：取 / 射
if start > last_end:          # ! LC-0452 闭区间 ⟹ 严格大于（共享端点也能被一箭穿）
    take += 1
    last_end = end
# LC-0435 半开语义时用 start >= last_end
```

### ⚠️ 不等号：LC-0435 用 `>=`，LC-0452 用 `>`

| 题 | 端点 | 条件 | 为什么 |
|---|---|---|---|
| LC-0435 | 区间**可以**端点相接（`[1,2]`、`[2,3]` 不算重叠） | `start >= last_end` | 相接可以都保留 |
| LC-0452 | **闭区间**（气球 `[2,4]` 和 `[4,7]` 共享 4） | `start > arrow_x` | 一箭在 4 能同时扎破两个 ⟹ 不用加箭 |
| LC-0252 | 半开（会议结束即释放） | `prev_end > cur_start` 才冲突 | 背靠背开会不冲突 |

**三道题的不等号各不相同，而且小样例测不出来。**
见 [Endpoint Semantics Cheat Sheet](<../_resources/endpoint-semantics-cheat-sheet.md>)。

---

## Python 模板

### Template 4：End-time Greedy（本层的唯一模板）

```python
# LC-0435：最少删除数
def eraseOverlapIntervals(intervals):
    intervals.sort(key=lambda x: x[1])        # ! end 升序 —— 不是 start！
    kept, last_end = 0, float('-inf')
    for s, e in intervals:
        if s >= last_end:                     # ! 端点相接可以都留 ⟹ >=
            kept += 1
            last_end = e
    return len(intervals) - kept              # ! 删除数 = n - 保留数

# LC-0452：最少箭数（同一个贪心，换个计数）
def findMinArrowShots(points):
    points.sort(key=lambda x: x[1])           # ! end 升序
    arrows, arrow_x = 0, float('-inf')
    for s, e in points:
        if s > arrow_x:                       # ! 闭区间 ⟹ 严格大于
            arrows += 1
            arrow_x = e                        # ! 箭放在 end 上
    return arrows

# LC-0252：只判冲突（这题按 start 排序，因为要检查相邻）
def canAttendMeetings(intervals):
    intervals.sort(key=lambda x: x[0])        # ! start 升序
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i - 1][1]:   # ! 半开 ⟹ 严格小于才冲突
            return False
    return True
```

**复杂度**：全部 **O(n log n)** 时间（排序主导）、**O(1)** 额外空间。

> 💡 **LC-0252 是本层唯一按 start 排序的题** —— 因为它只需要检查相邻对，
> 不需要「选最优子集」。别把它和 435 / 452 的排序键搞混。

### C++ / Java 的溢出警告（LC-0452）

```cpp
// ❌ 错：points[i][1] - points[j][1] 在 end 接近 INT_MAX / INT_MIN 时溢出
sort(points.begin(), points.end(),
     [](auto& a, auto& b){ return a[1] - b[1] < 0; });
// ✅ 对：直接比较，不做减法
sort(points.begin(), points.end(),
     [](auto& a, auto& b){ return a[1] < b[1]; });
```
LeetCode 的 LC-0452 测试数据里**真的**有 `[[-2147483646,-2147483645],[2147483646,2147483647]]`。
Python 整数无限精度，不受影响，但面试写 C++/Java 时这是个真实的坑。

---

## 代表题目

| # | 题 | 优先级 | 排序键 | 不等号 | 答案 |
|---|---|---|---|---|---|
| 1 | [LC-0252 Meeting Rooms](<./01 - 冲突检测与最大兼容区间数量/01 - LC-0252 - Meeting Rooms>) | **P0** | start ↑ | `<` 才冲突 | bool |
| 2 | [LC-0435 Non-overlapping Intervals](<./01 - 冲突检测与最大兼容区间数量/02 - LC-0435 - Non-overlapping Intervals>) | **P0** | **end ↑** | `>=` 可取 | `n - k` |
| 3 | [LC-0452 Minimum Number of Arrows](<./02 - 最少覆盖点与区间射击/01 - LC-0452 - Minimum Number of Arrows to Burst Balloons>) | P1 | **end ↑** | `>` 需新箭 | `k` |

⚠️ **LC-0252 是 LeetCode Premium 题目**；本仓库的实体来自原 NeetCode 版本
（已正式化为 LC-0252，所有原始文件和复习记录保留）。

---

## 典型边界情况

| 边界 | 例子 | 期望 |
|---|---|---|
| 端点相等 | `eraseOverlap([[1,2],[2,3]])` | `0`（相接不算重叠） |
| 端点相等（闭区间） | `findMinArrows([[1,2],[2,3]])` | **`1`**（一箭在 2 穿两个） |
| 完全包含 | `eraseOverlap([[1,100],[2,3]])` | `1` |
| 完全相同 | `eraseOverlap([[1,2],[1,2]])` | `1` |
| 完全相同（闭区间） | `findMinArrows([[1,2],[1,2]])` | `1` |
| 空输入 | `eraseOverlap([])` | `0` |
| 完全无重叠 | `eraseOverlap([[1,2],[5,6]])` | `0` |
| 全部重叠在一点 | `findMinArrows([[1,10],[2,9],[3,8]])` | `1` |
| 嵌套 + 相接 | `findMinArrows([[2,4],[2,2],[5,7],[4,7],[3,7]])` | **`2`** |
| 单区间 | `findMinArrows([[1,2]])` | `1` |
| 极值溢出（C++/Java） | `[[-2147483646,-2147483645],[2147483646,2147483647]]` | `2`，不要用减法比较 |

---

## 错误策略反例

| 错误做法 | 反例 | 结果 |
|---|---|---|
| **按 start 升序**做 LC-0435 | `[[1,100],[2,3],[3,4]]` | 得 `k=1`，正确 `k=2` |
| 按**区间长度**升序 | 构造性反例 | 短区间位置可能很差 |
| LC-0452 用「每次射能扎最多气球的点」 | `[[2,4],[2,2],[5,7],[4,7],[3,7]]` | 得 **3**，正确 **2** |
| LC-0452 用 `start >= arrow_x` | `[[1,2],[2,3]]` | 得 2，正确 1 |
| LC-0435 用 `start > last_end` | `[[1,2],[2,3]]` | 得 1，正确 0 |
| LC-0252 用 `<=` 判冲突 | `[[1,2],[2,3]]` | 得 False，正确 True |
| 删区间时「删后面的」而不是贪心 | — | 需要正确的贪心规则，不能随手删 |
| C++ 用 `a[1] - b[1] < 0` 排序 | 极值用例 | 整数溢出 ⟹ 排序顺序错乱 |

> **`[[2,4],[2,2],[5,7],[4,7],[3,7]]` 这组反例值得专门记住**：
> 「最大覆盖贪心」（每次挑能扎最多气球的点）会先射 7（扎破 `[5,7],[4,7],[3,7]` 三个），
> 然后还需要 2 支 ⟹ 共 3 支。正确做法是射 2（扎 `[2,4],[2,2]`）和 7（扎其余三个）⟹ 2 支。
> **集合覆盖的最大覆盖贪心只有 O(log n) 近似保证，不是最优算法。**

---

## 相邻 Pattern 对比

| | [Level 1 · 01](<../01 - 区间合并、插入与范围整理>) | **本层（03）** | [Level 1 · 04](<../04 - 重叠计数、扫描线与资源分配>) |
|---|---|---|---|
| 优化目标 | 求**并集** | **最大兼容数 / 最少点数** | **最大并发数** |
| 排序键 | **start ↑** | **end ↑** | start ↑ 或事件排序 |
| 输出 | 区间列表 | **一个计数** | 一个计数 / 一条数组 |
| 要 Heap？ | ❌ | ❌ | ✅（或差分 / 扫描线） |
| 典型陷阱 | `max(cur_end, e)` | **排序键是 end** | 端点语义决定不等号 |

### 四个目标的终极对照（必须分清）

| 题 | 目标 | 一句话 |
|---|---|---|
| LC-0056 Merge | 并集（Union） | 把相交的融合 |
| **LC-0435** | **最大化**保留的互不相交区间数 | 选最多 |
| **LC-0452** | **最小化**覆盖全部区间的点数 | 扎最少 |
| LC-0253 Meeting Rooms II | **最大并发数**（Max Overlap） | 最少房间 |

> 四个目标**完全不同**，但 435 和 452 的数值答案相同（见上面的观察）。
> 253 和前三个毫无关系：它要的是「某一时刻最多几个区间同时存在」。

---

## 相关资料

- [Pattern Recognition Guide](<../_resources/pattern-recognition-guide.md>) — Q4 / Q5 / Q6
- [Endpoint Semantics Cheat Sheet](<../_resources/endpoint-semantics-cheat-sheet.md>)
- [Interval Algorithm Comparison Table](<../_resources/interval-algorithm-comparison.md>) — 模板 4
- [P0 / P1 / P2 Roadmap](<../_resources/p0-p1-p2-roadmap.md>)
