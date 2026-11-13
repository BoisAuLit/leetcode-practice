# Level 1 · 04 Stack 与 Queue 数据结构设计 (Design)

## 核心定义
不是「用栈解题」，而是「**实现**一个有额外保证的栈 / 队列」。
考点集中在：辅助状态、循环缓冲区（Ring Buffer）、以及**摊还分析（Amortized Analysis）**。

## 决定性观察
1. **辅助状态要和主结构同生共死**：Min Stack 的最小值必须随 push/pop 一起维护，
   否则 pop 之后没法恢复上一个最小值。
2. **环形缓冲区靠取模**，队满和队空都表现为 `head == tail`，
   所以必须额外存一个 `size`（或者浪费一个格子）来区分。
3. **两次反转 = 恢复原序**，这是两个栈实现队列的全部原理。
4. 代价可以**挪到哪一端**是设计者的自由：
   LC-0232 可以 push 便宜 / pop 摊还便宜，也可以 push O(n) / pop O(1)。

## 题目

| # | 题 | 优先级 | 独有的东西 |
|---|---|---|---|
| 01/01 | LC-0155 Min Stack | P0 | 辅助状态；存 `(值, 当前最小)` 或用第二个栈；全部 O(1) |
| 02/01 | LC-0346 Moving Average from Data Stream | P1 | 固定容量队列 + **Running Sum**，不必每次重新求和 |
| 02/02 | LC-0622 Design Circular Queue | P1 | Ring Buffer；`head`/`count`/`capacity`；满空判定 |
| 03/01 | LC-0232 Implement Queue using Stacks | P1 | 两个栈，**只在 out 空时整体搬运** ⇒ 摊还 O(1) |
| 03/02 | LC-0225 Implement Stack using Queues | P1 | Rotation；**没有摊还技巧**，每次操作就是 O(n) |
| 04/01 | LC-0649 Dota2 Senate | P2 | 用队列**建模**循环轮转；下标 `+n` 表示「排到下一轮」 |

## LC-0232 vs LC-0225：**不是对称的**

| | LC-0232 栈 → 队列 | LC-0225 队列 → 栈 |
|---|---|---|
| 核心技巧 | 倒两次恢复原序 | Rotation：前 n-1 个出队再入队 |
| 复杂度 | push O(1)，pop/peek **摊还 O(1)** | push **或** pop 必有一个是 O(n) |
| 能否摊还优化 | **能**（元素一生只搬一次） | **不能**（每次都要重排全部元素） |

这是本章最容易写错的一点：看起来是一对对偶问题，实际上**代价结构完全不同**。
栈能做到摊还 O(1)，是因为「反转两次等于没反转」；队列没有这个性质。

## 摊还分析（面试必须说清楚）
> LC-0232 的 `pop()` 单次最坏是 O(n)（恰好触发整体搬运），
> 但每个元素一生只经历「进 in → 出 in → 进 out → 出 out」4 次操作，
> 所以 n 次调用总代价 O(n)，**摊还 O(1)**。
> 不能笼统说「每次操作都是 O(1)」。

同样的说法适用于 LC-0901（Online Stock Span，在 18-monotonic）。

## 环形队列的满 / 空判定
```python
self.q = [0] * k; self.head = 0; self.count = 0
def enQueue(self, v):
    if self.count == self.k: return False
    self.q[(self.head + self.count) % self.k] = v   # 尾部位置算出来，不单独存 tail
    self.count += 1; return True
def deQueue(self):
    if self.count == 0: return False
    self.head = (self.head + 1) % self.k; self.count -= 1; return True
```
用 `count` 而不是 `tail` 能彻底回避「`head == tail` 到底是满还是空」的歧义。

## 常见错误
- Min Stack 只存一个全局最小值 → pop 掉最小值之后无法恢复。
- LC-0622 用 `head == tail` 判满空而不存 `size`。
- LC-0232 每次操作都整体搬运 → 退化成 O(n)，摊还优势消失。
- LC-0346 每次都遍历整个窗口求和 → 应该维护 Running Sum。

## 备注
LC-0346 可能是 Premium 题，已有的题面资料原样保留。


---

## 2026-11-11 新增题目（对照大厂高频题单补的缺口）

| 题 | 位置 | 信号 → 模式 | 备注 |
|---|---|---|---|
| [LC-0716 Max Stack](<./01 - 带额外状态的 Stack/02 - LC-0716 - Max Stack>) | `04 - Stack 与 Queue 数据结构设计 (Design)/01 - 带额外状态的 Stack` | popMax 要从栈中间删：堆 + 懒删除（栈/堆各存 (val,id)，removed 集合）；两栈 O(n) 版先写 | LC-0155 Min Stack 的 Hard 版；Premium 题 |
| [LC-0895 Maximum Frequency Stack](<./01 - 带额外状态的 Stack/03 - LC-0895 - Maximum Frequency Stack>) | `04 - Stack 与 Queue 数据结构设计 (Design)/01 - 带额外状态的 Stack` | 按频率分层：group[f] 是一个栈，pop 永远在 group[maxfreq]；maxfreq 只会降 1 | O(1) 不需要时间戳 |
| [LC-2296 Design a Text Editor](<./01 - 带额外状态的 Stack/04 - LC-2296 - Design a Text Editor>) | `04 - Stack 与 Queue 数据结构设计 (Design)/01 - 带额外状态的 Stack` | 光标把文本切成两个栈（gap buffer），四个操作全是栈顶操作；str 拼接 O(n) 是反面教材 | LC-1472 同源 |

每道题的 `solution.py` 都带：全部主流解法（各自的复杂度与适用场景）、一个 ⭐️ Preferred、和一段对独立真值基线的随机对拍。
