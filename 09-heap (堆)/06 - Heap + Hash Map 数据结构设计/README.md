# Level 1 · 06 Heap + Hash Map 数据结构设计

## 核心定义
堆给「最优」，Hash Map 给「按 key 定位」。
设计题几乎总是这两者的组合 —— 因为单独任何一个都有明显短板。

| 结构 | 能做 | 不能做 |
|---|---|---|
| Heap | O(log n) 取最优 | 按 key 查、删任意元素 |
| Hash Map | O(1) 按 key 查改 | 取最优（要 O(n) 扫） |

## 01 - 社交信息流与多路合并（LC-0355 Design Twitter）

**数据结构**：
```python
tweets:    defaultdict(list)   # userId -> [(timestamp, tweetId), ...] 按时间递增
following: defaultdict(set)    # userId -> 关注的人
time:      全局自增计数器       # 用来给推文排序
```

**`getNewsFeed` 是一次 K-way Merge**：
把「自己 + 所有关注的人」的推文列表看成 k 条**按时间降序**的链，
用堆取出最新的 10 条。
**优化**：每条链只需要看**最后 10 条**（再早的不可能进前 10），
所以可以只取每个人的 `tweets[u][-10:]`。

| 操作 | 复杂度 |
|---|---|
| postTweet | O(1) |
| follow / unfollow | O(1) |
| getNewsFeed | O(k log k + 10 log k)，k = 关注人数 |

**细节**：
- 用**全局递增的 timestamp**，不要用真实时间。
- `unfollow` 要用 `discard` 而不是 `remove`（不存在时不报错）。
- 用户默认关注自己，或者在 `getNewsFeed` 里手动把自己加进去。

## 02 - 动态优先级与 Lazy Deletion（LC-3408 Design Task Manager）

**问题**：任务的优先级会被**修改**，任务也会被**删除**。
但堆**不支持修改/删除任意元素**。

**解法：Lazy Deletion（惰性删除）** —— 本章的重点。

```python
tasks: dict   # taskId -> (userId, priority)   ← 唯一的真相来源（source of truth）
heap:  list   # (-priority, -taskId, userId)   ← 可能包含过期条目

def edit(taskId, newPriority):
    tasks[taskId] = (userId, newPriority)
    heappush(heap, (-newPriority, -taskId, userId))   # 直接推新的，旧的不管

def execTop():
    while heap:
        p, tid, uid = heap[0]
        if tasks.get(-tid) == (uid, -p):    # 和真相一致 → 有效
            heappop(heap); del tasks[-tid]
            return uid
        heappop(heap)                        # 过期条目，丢弃
    return -1
```

**三个要点**：
1. **Hash Map 是唯一的真相来源**，堆只是「候选池」，里面可能有过期条目。
2. **验证**：弹出时拿堆顶和 Hash Map 比对，不一致就说明它是旧版本，直接丢掉。
3. **摊还复杂度**：每次 `edit` 最多往堆里加一个条目，所以堆里总条目数 = O(操作数)，
   每个条目最多被弹出一次 ⟹ 总体摊还 **O(log n)**。
   **单次 `execTop` 最坏可能连续丢弃很多过期条目**，不能说单次 O(log n)。

同样的技巧在 LC-0480（Level 1 `03`）里用来支持「窗口滑出元素」。

## 题目

| # | 题 | 优先级 | 核心 |
|---|---|---|---|
| 01/01 | LC-0355 Design Twitter | **P0** | Hash Map + K-way Merge + 全局时间戳 |
| 02/01 | LC-3408 Design Task Manager | P1 | Hash Map 做真相来源 + 堆 Lazy Deletion |

## 跨专题
更多设计题在 [17-design (设计)](<../../17-design (设计)/>)；
LRU Cache（Hash Map + 双向链表）在 [17-design](<../../17-design (设计)/02 - Cache 与 O(1) 淘汰策略/01 - LRU Cache/01 - LC-0146 - LRU Cache>)。

**三者的对照很值得看**：
| 题 | 组合 | 为什么是这个组合 |
|---|---|---|
| LC-0146 LRU | Hash Map + **双向链表** | 要 O(1) 把任意节点挪到头部 |
| LC-0355 Twitter | Hash Map + **堆** | 要按时间取 Top-10 |
| LC-3408 Task Manager | Hash Map + **堆 + 惰性删除** | 优先级会变，堆里会有过期条目 |

## 常见错误
- LC-0355 用真实时间戳（粒度不够，同一毫秒的推文无法排序）。
- LC-0355 遍历所有关注者的**全部**推文（应该只看每人最后 10 条）。
- LC-3408 试图在堆里「修改」已有条目（堆做不到）。
- LC-3408 弹出时不做有效性验证，返回了已被修改/删除的任务。
- 把 Lazy Deletion 的单次复杂度说成 O(log n)（应说**摊还**）。


---

## 2026-11-11 新增题目（对照大厂高频题单补的缺口）

| 题 | 位置 | 信号 → 模式 | 备注 |
|---|---|---|---|
| [LC-1244 Design A Leaderboard](<./02 - 动态优先级与 Lazy Deletion/02 - LC-1244 - Design A Leaderboard>) | `06 - Heap + Hash Map 数据结构设计/02 - 动态优先级与 Lazy Deletion` | top(K) 用大小为 K 的最小堆 O(n log K)；三种实现对应「谁来付钱」 | 暖场设计题，考复杂度取舍；**Premium 题，当前账号抓不到 PDF**；题面摘要在 solution.py 顶部的 docstring 里；续费后 `python3 tools/intake.py "<文件夹>"` 可补抓 |

每道题的 `solution.py` 都带：全部主流解法（各自的复杂度与适用场景）、一个 ⭐️ Preferred、和一段对独立真值基线的随机对拍。
