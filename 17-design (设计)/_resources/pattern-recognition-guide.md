# Design Pattern Recognition Guide（设计题型识别指南）

> 设计题的识别靠**API 的形状**：看它要你实现哪几个方法，以及哪个方法要求最快。
> 这些提示**不互斥** —— LC-0460 = Q2 + Q3，LC-1797 = Q6 + Q8。

---

## 决策树

### Q1：要手写一个 HashSet / HashMap？
→ **Separate Chaining（链地址法）**：固定桶数 + 每桶一个链表/列表。
桶数选**质数**（如 769）降低碰撞聚集；`hash(key) % buckets` 定位。
📍 [LC-0705 Design HashSet](<../01 - Hash Structures 与稀疏数据设计/01 - HashSet 与 HashMap 基础实现/01 - LC-0705 - Design HashSet>)、
[LC-0706 Design HashMap](<../01 - Hash Structures 与稀疏数据设计/01 - HashSet 与 HashMap 基础实现/02 - LC-0706 - Design HashMap>)

### Q2：要 O(1) 的 `get` / `put` **并且**能按顺序淘汰？
→ **双向链表 + 哈希**。链表管顺序（O(1) 移动），哈希管定位（O(1) 查找）。
Python 可以用 `OrderedDict.move_to_end` 偷懒。
📍 [LC-0146 LRU Cache](<../02 - Cache 与 O(1) 淘汰策略/01 - LRU Cache/01 - LC-0146 - LRU Cache>)

### Q3：淘汰依据是**使用次数**而不是时间？
→ **频率桶 + `min_freq` 指针**。
关键：**freq 一次只 +1** ⟹ `min_freq` 不需要搜索，只需要「桶空了就 +1」。
📍 [LC-0460 LFU Cache](<../02 - Cache 与 O(1) 淘汰策略/02 - LFU Cache 与频率桶/01 - LC-0460 - LFU Cache>)

### Q4：要 O(1) 插入、删除 **+ 均匀随机访问**？
→ **紧凑数组 + `val -> 下标`，删除用 swap-with-last**。
数组给随机访问，字典给定位；交换到末尾再 `pop` 保持紧凑。
📍 [LC-0380](<../03 - Randomized Data Structures/01 - O(1) 插入、删除与均匀随机访问/01 - LC-0380 - Insert Delete GetRandom O(1) (学习索引 · 实体在 01-arrays-hashing)>) ↗️（不许重复）、
[LC-0381](<../03 - Randomized Data Structures/01 - O(1) 插入、删除与均匀随机访问/02 - LC-0381 - Insert Delete GetRandom O(1) - Duplicates allowed>)（允许重复 ⟹ 下标变**集合**）

### Q5：要统计「最近 X 秒内的事件数」？
→ **队列 + 懒弹出**（或环形数组）。
队首不在窗口内就弹掉；每个时间戳**最多入队一次、出队一次** ⟹ **均摊 O(1)**。
📍 [LC-0933 Number of Recent Calls](<../04 - 时间窗口、计数器与限流/01 - Recent Calls 与流式时间窗口/01 - LC-0933 - Number of Recent Calls>)、
[LC-0362 Design Hit Counter](<../04 - 时间窗口、计数器与限流/01 - Recent Calls 与流式时间窗口/02 - LC-0362 - Design Hit Counter>)

### Q6：要对**每个 key 单独**做时间限流 / 去重？
→ **`key -> 上次时刻` 字典**，判 `now - last >= 窗口`。
⚠️ 不等号的方向要拿样例手算。
📍 [LC-0359 Logger Rate Limiter](<../04 - 时间窗口、计数器与限流/02 - 消息去重与时间限流/01 - LC-0359 - Logger Rate Limiter>)

### Q7：底层 API 的粒度固定，上层要任意长度？
→ **跨调用的持久化缓冲区**：实例持有 `buf + 指针 + 有效长度`。
⚠️ **多读出来的数据必须留到下一次调用**，否则丢数据。
📍 [LC-0157](<../05 - 有状态 API、缓冲区与模拟/01 - Buffered Reader 与跨调用状态/01 - LC-0157 - Read N Characters Given Read4>)（调用一次）、
[LC-0158](<../05 - 有状态 API、缓冲区与模拟/01 - Buffered Reader 与跨调用状态/02 - LC-0158 - Read N Characters Given read4 II - Call Multiple Times>)（**调用多次**）

### Q8：有「过期 / 失效」的概念？
→ **只存「过期时刻」，不存「生成时刻」** + **懒清理**。
正确性前提：时间**单调不减** ⟹ 过期的**永远不会复活**。
⚠️ `expiry > now` 还是 `>= now`？拿样例手算。
📍 [LC-1797 Design Authentication Manager](<../04 - 时间窗口、计数器与限流/02 - 消息去重与时间限流/02 - LC-1797 - Design Authentication Manager>)

### Q9：要 O(1) 查「平均值 / 总和 / 计数」？
→ **增量聚合**：只存 `sum` 和 `count` 两个标量，不存明细。
❌ **中位数不行** —— 那需要有序结构（双堆，见 `09-heap`）。
📍 [LC-1396 Design Underground System](<../05 - 有状态 API、缓冲区与模拟/03 - 多对象状态与增量平均值/01 - LC-1396 - Design Underground System>)

### Q10：要判胜负 / 判状态，但不想每次扫全盘？
→ **更新时就算好**：维护每行/每列/每条对角线的计数，落子时 ±1。
📍 [LC-0348 Design Tic-Tac-Toe](<../05 - 有状态 API、缓冲区与模拟/02 - 棋盘状态与历史导航/01 - LC-0348 - Design Tic-Tac-Toe>)

### Q11：要前进 / 后退 / undo-redo？
→ **数组 + 游标 + 有效长度**。
新操作时不删后面的内容，只把「有效长度」缩回来（**逻辑删除**，O(1)）。
⚠️ 双栈版也能对，但 `back(steps)` 是 **O(steps)** 而游标版是 **O(1)**。
📍 [LC-1472 Design Browser History](<../05 - 有状态 API、缓冲区与模拟/02 - 棋盘状态与历史导航/02 - LC-1472 - Design Browser History>)

### Q12：要访问**历史版本 / 快照**？
→ **每个位置一条版本链 `(版本号, 值)` + 二分查找**。
⚠️ **绝不要真的复制整个数组** —— `snap()` 必须是 O(1)。
📍 [LC-1146 Snapshot Array](<../05 - 有状态 API、缓冲区与模拟/04 - 版本快照与历史访问/01 - LC-1146 - Snapshot Array>)

### Q13：数据**极度稀疏**（大部分是 0）？
→ **只存非零项**（`下标 -> 值` 的字典，或 `(下标, 值)` 的有序列表）。
求内积时用**双指针**只扫两边都非零的下标。
📍 [LC-1570 Dot Product of Two Sparse Vectors](<../01 - Hash Structures 与稀疏数据设计/02 - Sparse Representation 与高效内积/01 - LC-1570 - Dot Product of Two Sparse Vectors>)

### Q14：**哪个操作必须最快？**
→ 这一条决定前面所有选择。见 [设计题通用清单 · 第 1 步](<./design-checklist.md>)。
**每道设计题都要先问这一句。**

---

## 三秒速判表

| API 形状 / 关键词 | Pattern |
|---|---|
| `add` / `contains` / `remove`，不许用内置容器 | Separate Chaining |
| `get` / `put` + capacity + "least recently used" | 双向链表 + 哈希（LRU） |
| 同上但 "least frequently used" | **频率桶 + min_freq**（LFU） |
| `insert` / `remove` / `getRandom` | 紧凑数组 + **swap-with-last** |
| `ping(t)` / `hit(t)` / `getHits(t)` | 队列 + 懒弹出（滑动时间窗口） |
| `shouldPrintMessage(t, msg)` | `key -> 上次时刻` 字典 |
| `generate` / `renew` / `countUnexpired` | **过期时刻 + 懒清理** |
| `read(buf, n)` 且"会被调用多次" | **跨调用持久缓冲区** |
| `checkIn` / `checkOut` / `getAverage` | **增量 (sum, count)** |
| `move(row, col, player)` 返回胜者 | **增量行列计数** |
| `visit` / `back` / `forward` | 数组 + 游标 + **有效长度** |
| `set` / `snap` / `get(i, snap_id)` | **版本链 + 二分** |
| 向量很长但大部分是 0 | 只存非零项 + 双指针 |

---

## 读设计题时的三问

1. **两次调用之间，我必须记住什么？** → 决定字段
2. **哪个操作最频繁 / 要求最快？** → 决定成本往哪边挪
3. **边界时刻 / 空容器 / 失败操作的语义是什么？** → 决定不等号和 no-op

---

## 本专题的六个反复套路（速查）

| 套路 | 一句话 | 题 |
|---|---|---|
| **两结构组合** | 一个管顺序/随机，一个管定位（字典总是后者） | 0146, 0460, 0380, 0381 |
| **swap-with-last** | 和末尾交换再 pop ⟹ O(1) 删除 + 数组保持紧凑 | 0380, 0381 |
| **逻辑删除** | 不真删，只缩「有效长度」 | 1472 |
| **懒清理** | 不主动删过期项，读取时才过滤（前提：时间单调） | 1797, 0362, 0933 |
| **增量聚合** | 只存 sum/count，不存明细（中位数不适用） | 1396, 0348 |
| **懒删除堆** | 只保证清理后的**堆顶**有效 | 1797 解法 3 |

详见 [设计题通用清单](<./design-checklist.md>)。
