# Level 1 · 04 — 时间窗口、计数器与限流（Sliding Time Window / Rate Limiting）

> **本层的统一目标：维护「最近一段时间内」的状态，并在 O(1) 或均摊 O(1) 回答。**
> 四道题的算法都很短 —— **难点全在不等号的方向**。

---

## 核心定义

| 术语 | 定义 |
|---|---|
| **Sliding Time Window（滑动时间窗口）** | 只关心 `[now - W, now]` 内的事件 |
| **Streaming Counter（流式计数器）** | 事件一个个来，随时要答「窗口内有几个」 |
| **Rate Limiting（限流）** | 同一个 key 在窗口内只允许通过一次 |
| **Expiration Semantics（过期语义）** | 每个条目有自己的失效时刻 |
| **Lazy Cleanup（懒清理）** | 不主动删过期项，只在读取时过滤/清理 |

---

## 三个决定性观察

### ① 时间**单调不减** ⟹ 过期的**永远不会复活** ⟹ 可以放心丢

这是本层**所有**解法的正确性基石。题目都保证 `timestamp` 非递减，所以：

> 一旦某条记录「出了窗口」或「过期了」，
> 对后续更大的 `now'` 它必然**仍然**出窗口/过期
> ⟹ **可以安全地永久删除**，不需要保留以备复活。∎

没有这条保证的话，队列就不能弹、过期项就不能删，整层的 O(1) 全部垮掉。

### ② 队列 + 懒弹出 = **均摊 O(1)**

```python
def ping(self, t):
    self.q.append(t)
    while self.q[0] < t - 3000:        # ! 队首出窗口就弹掉
        self.q.popleft()
    return len(self.q)
```

**为什么是均摊 O(1) 而不是 O(n)？**
每个时间戳**最多入队一次、出队一次** ⟹ `n` 次 `ping` 的总弹出代价是 O(n)
⟹ **均摊每次 O(1)**。
单次调用可能弹很多（最坏 O(n)），但**总量有界**。∎

> **这是均摊分析最干净的例子** ——
> 「每个元素一生只被处理常数次」就是均摊 O(1) 的标准论证。

### ③ 「每个 key 独立限流」只需要一张 `key -> 上次时刻` 的字典

```python
def shouldPrintMessage(self, t, message):
    if t - self.last.get(message, float('-inf')) >= 10:
        self.last[message] = t          # ! 只在允许时才更新
        return True
    return False
```

**为什么被拒绝时不能更新 `last`？**
若每次调用都更新，一个被疯狂调用的 message 会把 `last` 一直往后推
⟹ **永远不会再被允许打印** ⟹ 语义错。
**被拒绝的调用必须完全不留痕迹。**

---

## ⚠️ 四道题的不等号各不相同（本层最该记的一张表）

| 题 | 存什么 | 判定条件 | 边界语义 |
|---|---|---|---|
| [LC-0933 Recent Calls](<./01 - Recent Calls 与流式时间窗口/01 - LC-0933 - Number of Recent Calls>) | 请求时刻的**队列** | 弹掉 `t < now - 3000` | 窗口是 **`[now-3000, now]` 闭区间**（两端都算） |
| [LC-0362 Hit Counter](<./01 - Recent Calls 与流式时间窗口/02 - LC-0362 - Design Hit Counter>) | 环形数组 / 队列 | 保留 `t > now - 300` | 窗口是**过去 300 秒**（`now-300` 那一秒已经出去了） |
| [LC-0359 Logger Rate Limiter](<./02 - 消息去重与时间限流/01 - LC-0359 - Logger Rate Limiter>) | `message -> 上次打印时刻` | `now - last >= 10` **才允许** | **允许**恰好相隔 10 秒 |
| [LC-1797 Auth Manager](<./02 - 消息去重与时间限流/02 - LC-1797 - Design Authentication Manager>) | `token -> **过期时刻**` | `expiry > now` **才算活** | **不允许**恰好到期 |

> **四道题都在做「时间窗口」，但不等号全不一样。**
> 唯一可靠的办法：**拿官方样例的边界时刻手算一遍**，别凭感觉。
>
> 例：LC-1797（`ttl=5`，`generate("a",1)` ⟹ `expiry=6`）
> ⟹ `count(5)` 算活（`6>5`），`count(6)` 算**死**（`6>6` 为假）。
> 写成 `>=` 会让 token 多活一个时刻，`renew` 还会**复活一个已死的 token**。

---

## 核心不变量

**队列版（LC-0933 / LC-0362）**：
> 队列恒为「**仍在窗口内**的全部事件时刻」，且**按时间升序**。
> ⟹ 队首是最老的；队首出窗口 ⟹ 弹掉；`len(queue)` 就是答案。

**环形数组版（LC-0362）**：
> `buckets[t % 300]` 恒存「秒 `t` 的命中数」，`times[t % 300]` 恒存「这个桶属于哪一秒」。
> 读取时若 `times[i]` 已经出窗口 ⟹ 该桶的值作废（视为 0）。

**限流字典（LC-0359）**：
> `last[msg]` 恒为「该 message **上一次被允许打印**的时刻」（不是上次被调用的时刻）。

**过期表（LC-1797）**：
> `expiry[t]` 恒为「token `t` 最近一次 `generate`/`renew` 所确定的过期时刻」；
> `t` 存活 ⟺ `expiry[t] > now`。

---

## 为什么选这些结构

### LC-0362 为什么可以用「环形数组」而不是队列？

窗口固定 300 秒 ⟹ **最多只需要 300 个桶**。
```python
self.times = [0] * 300        # ! 这个桶代表哪一秒
self.counts = [0] * 300       # ! 那一秒的命中数
def hit(self, t):
    i = t % 300
    if self.times[i] != t:
        self.times[i] = t; self.counts[i] = 1    # ! 桶过期 ⟹ 重置
    else:
        self.counts[i] += 1
```
**空间从 O(命中总数) 降到 O(300) = O(1)**，而队列版在「同一秒大量命中」时会爆。

**代价**：`getHits` 要扫 300 个桶 ⟹ **O(300) = O(1)**（常数较大）。

> **队列 vs 环形数组的分界线**：
> 命中稀疏 ⟹ 队列（空间按实际事件数）；
> 命中密集 / 窗口固定且不大 ⟹ 环形数组（空间 O(窗口长度)）。

### LC-1797 为什么存「过期时刻」而不是「生成时刻」？

判断「是否过期」是最频繁的操作：
- 存过期时刻 ⟹ `expiry[t] > now`，**一次比较**
- 存生成时刻 ⟹ `created[t] + ttl > now`，每次都要**多一次加法**

而 `renew` 本来就是「重置过期时刻」⟹ 直接赋值。
**存过期时刻让三个操作都变成最简形式。**

---

## 简短正确性证明

### 队列弹出不会丢解

队列按时间升序 ⟹ 队首是最老的。
若队首仍在窗口内，则后面的全都在窗口内 ⟹ **可以停止弹出**。
若队首出窗口，由时间单调性，它对后续查询也永远出窗口 ⟹ **可以永久删除**。∎

### 懒清理的正确性（LC-1797 解法 2）

`currentTime` 单调不减 ⟹ 一旦 `expiry <= now`，
对后续 `now' >= now` 必然还有 `expiry <= now'` ⟹ **永久失效，不会复活**
⟹ 在 `countUnexpiredTokens` 时删掉它们是安全的。
且每个 token 一生最多被删一次 ⟹ 总删除代价 O(n) ⟹ **均摊 O(1)**。∎

---

## Python 核心模板

```python
# ① 队列 + 懒弹出（LC-0933）
def ping(self, t):
    self.q.append(t)
    while self.q[0] < t - 3000:            # ! 闭区间 ⟹ 严格小于才弹
        self.q.popleft()
    return len(self.q)
# 均摊 O(1)，空间 O(窗口内事件数)

# ② 环形数组（LC-0362）
def hit(self, t):
    i = t % 300
    if self.times[i] != t:
        self.times[i], self.counts[i] = t, 1    # ! 桶属于旧的一秒 ⟹ 重置
    else:
        self.counts[i] += 1

def getHits(self, t):
    return sum(c for tm, c in zip(self.times, self.counts) if t - tm < 300)
# hit O(1)，getHits O(300) = O(1)，空间 O(300) = O(1)

# ③ 每 key 限流（LC-0359）
def shouldPrintMessage(self, t, message):
    if t - self.last.get(message, float('-inf')) >= 10:   # ! >= 允许恰好 10 秒
        self.last[message] = t                             # ! 只在允许时更新
        return True
    return False
# O(1) 平均，空间 O(不同 message 数)

# ④ 过期语义 + 懒清理（LC-1797）
def renew(self, tokenId, currentTime):
    # ! get(..,-1) 让「不存在」和「已过期」走同一分支；> 是严格大于
    if self.expiry.get(tokenId, -1) > currentTime:
        self.expiry[tokenId] = currentTime + self.ttl

def countUnexpiredTokens(self, currentTime):
    return sum(1 for e in self.expiry.values() if e > currentTime)   # ! O(n)
```

---

## 时间与空间复杂度

| 题 | 主要操作 | 时间 | 空间 |
|---|---|---|---|
| LC-0933 | `ping` | **均摊 O(1)** | O(窗口内事件数) |
| LC-0362 | `hit` / `getHits` | **O(1)** / **O(300) = O(1)** | **O(300) = O(1)** |
| LC-0359 | `shouldPrintMessage` | **O(1) 平均** | O(不同 message 数) |
| LC-1797 | `generate` / `renew` | **O(1) 平均** | O(历史 token 数) |
| | `countUnexpiredTokens` | **O(n)**（懒清理版） | — |

⚠️ **LC-1797 的 `count` 不是 O(1)** —— 不要声称「全部 O(1)」。
若要 O(1)，得用「计数时清理」（均摊）或「堆 + 懒删除」（O(log n)）。
⚠️ LC-0933 是**均摊** O(1)，单次可能弹很多。

---

## 代表题目

| # | 题 | 优先级 | 结构 | 边界语义 |
|---|---|---|---|---|
| 1 | [LC-0933 Number of Recent Calls](<./01 - Recent Calls 与流式时间窗口/01 - LC-0933 - Number of Recent Calls>) | **P0** | 队列 + 懒弹出 | 闭区间 `[now-3000, now]` |
| 2 | [LC-0362 Design Hit Counter](<./01 - Recent Calls 与流式时间窗口/02 - LC-0362 - Design Hit Counter>) | P1 | 环形数组 / 队列 | 过去 300 秒 |
| 3 | [LC-0359 Logger Rate Limiter](<./02 - 消息去重与时间限流/01 - LC-0359 - Logger Rate Limiter>) | P1 | `key -> 上次时刻` | `>= 10` **允许** |
| 4 | [LC-1797 Design Authentication Manager](<./02 - 消息去重与时间限流/02 - LC-1797 - Design Authentication Manager>) ★ | P1 | 过期时刻 + 懒清理 | `> now` **才算活** |

★ 第二轮审核新增。
⚠️ **LC-0362 和 LC-0359 是 LeetCode Premium 题目**（原始资料已完整保留）。

---

## 典型边界情况

| 边界 | 期望 |
|---|---|
| 窗口**恰好**的边界时刻 | 每题不同 —— 见上面的不等号对照表 |
| 同一时刻**多次**调用 | LC-0362 要累加同一个桶；LC-0933 队列里会有重复时刻 |
| 时间**跳跃**（中间很久没调用） | 队列要一次弹掉很多；环形数组的桶要按 `times[i] != t` 重置 |
| 被拒绝的调用 | **完全不留痕迹**（LC-0359 不更新 `last`；LC-1797 的 `renew` 是 no-op） |
| `renew` 一个**不存在**的 token | no-op |
| `renew` 一个**恰好过期**的 token | **no-op**，不能复活 |
| 所有条目都过期 | 返回 0 |
| `ttl = 1` | 下一个时刻就过期 |
| 第一次调用（表为空） | `get(.., 哨兵)` 要能正确走到「不存在」分支 |

---

## 典型反例

| 错误做法 | 反例 | 结果 |
|---|---|---|
| LC-0359 被拒绝时也更新 `last` | 同一 message 每秒调用一次 | `last` 一直后推 ⟹ **永远不再允许打印** ❌ |
| LC-1797 用 `expiry >= now` | `ttl=5`，`generate("a",1)`，`count(6)` | 得 1，正确是 **0**（恰好到期算死）❌ |
| LC-1797 的 `renew` 不检查是否过期 | `renew` 一个已死 token | **复活了一个已过期的 token** ❌ |
| LC-0933 用 `<=` 弹队首 | 边界时刻 | 少算一个（窗口是闭区间）❌ |
| LC-0362 用队列但不限桶 | 同一秒 10^5 次 hit | 空间爆炸（环形数组是 O(300)）⚠️ |
| LC-0362 的桶不判 `times[i] != t` | 时间跳过 300 秒的倍数 | 读到**上一轮**的陈旧计数 ❌ |
| 懒清理但时间**不单调** | 假设的变体 | 过期的可能"复活" ⟹ 删掉就错 ❌ |
| LC-1797 声称 `count` 是 O(1) | — | 懒清理版是 O(n) ⚠️ |
| 把四题的不等号互相套用 | — | 每题边界语义不同 ❌ |

---

## 容易混淆的 Pattern

### 队列 vs 环形数组 vs 字典

| | **队列**（0933） | **环形数组**（0362） | **字典**（0359 / 1797） |
|---|---|---|---|
| 回答什么 | 窗口内**事件总数** | 窗口内**命中总数** | **每个 key 独立**的状态 |
| 空间 | O(窗口内事件数) | **O(窗口长度)** | O(不同 key 数) |
| 同一时刻多事件 | 存多份 | **合并到一个桶** | 不适用 |
| 适用 | 事件稀疏 | 事件密集、窗口固定 | 按 key 限流 / 过期 |

### 懒清理 vs 主动清理 vs 堆

| | 懒清理 | 计数时清理 | 堆 + 懒删除 |
|---|---|---|---|
| 查询 | **O(n)** | 均摊 O(存活数) | **O(log n)** |
| 空间 | O(历史总数) | **O(存活数)** | O(历史总数) |
| 何时用 | 查询少 | 要省空间 | 要单次 O(log n) |

LC-1797 的 `solution.py` **三种都实现了**，并用随机对拍证明它们等价。

### 和 Level 1 · 05 的区别

| | **本层（04）** | [Level 1 · 05](<../05 - 有状态 API、缓冲区与模拟>) |
|---|---|---|
| 状态随什么变化 | **时间**（自动失效） | 调用序列（显式改变） |
| 核心难点 | **不等号 / 过期语义** | 记住什么 + 更新顺序 |
| 共同点 | 都要回答「两次调用之间记住了什么」 | 同 |

---

## 相关资料

- [设计题通用清单](<../_resources/design-checklist.md>) — 懒清理 + 均摊分析 + 复杂度用词
- [Pattern Recognition Guide](<../_resources/pattern-recognition-guide.md>) — Q5 / Q6 / Q8
