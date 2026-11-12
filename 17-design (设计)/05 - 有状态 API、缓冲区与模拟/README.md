# Level 1 · 05 — 有状态 API、缓冲区与模拟（Stateful API / Buffers / Simulation）

> **本层的统一目标：回答「两次调用之间，我必须记住什么？」**
> 这是所有设计题的母问题 —— 想清这一句，字段就定了，代码只是搬运。

---

## 核心定义

| 术语 | 定义 |
|---|---|
| **Persistent State Across Calls** | 跨调用保留的实例字段（不是方法内的局部变量） |
| **Buffered Reader（缓冲读取）** | 底层 API 粒度固定，上层要任意长度 ⟹ 需要缓冲残留 |
| **Array Cursor（数组游标）** | 用「数组 + 当前位置 + 有效长度」表示可前进/后退的历史 |
| **Incremental Aggregation（增量聚合）** | 更新时就把统计量算好，查询 O(1) |
| **Versioned Array / Snapshot** | 每个位置一条 `(版本号, 值)` 链，`snap()` 不复制数据 |

---

## 三个决定性观察

### ① 四道题的全部设计，就是四张「我必须记住什么」的答案

| 题 | 跨调用的状态 | 为什么是这些 |
|---|---|---|
| [LC-0158 read4 II](<./01 - Buffered Reader 与跨调用状态/02 - LC-0158 - Read N Characters Given read4 II - Call Multiple Times>) | `buf4` + 指针 `i` + 有效长度 `cnt` | `read4` 一次给 4 个，用不完的**必须留到下次** |
| [LC-1472 Browser History](<./02 - 棋盘状态与历史导航/02 - LC-1472 - Design Browser History>) | 历史数组 + 游标 `cur` + 有效长度 `last` | 要能前进/后退，且 `visit` 要作废前进历史 |
| [LC-1396 Underground System](<./03 - 多对象状态与增量平均值/01 - LC-1396 - Design Underground System>) | 在途乘客 + 每条线路的 `(sum, count)` | 查询要 O(1) ⟹ 不能存明细 |
| [LC-1146 Snapshot Array](<./04 - 版本快照与历史访问/01 - LC-1146 - Snapshot Array>) | 每个 index 一条版本链 + 当前 `snap_id` | `snap()` 必须 O(1) ⟹ 不能复制数组 |

### ② 「把成本从频繁操作挪到稀少操作」——**两个方向都有**

| 方向 | 做法 | 题 |
|---|---|---|
| **更新时多做一点，查询变 O(1)** | 增量聚合 / 增量计数 | LC-1396（sum/count）、[LC-0348](<./02 - 棋盘状态与历史导航/01 - LC-0348 - Design Tic-Tac-Toe>)（行列计数） |
| **更新变 O(1)，查询多做一点** | 版本链 + 二分 | **LC-1146**（`snap` O(1)，`get` O(log k)） |

> **哪个方向取决于哪个操作更频繁。** 这是本专题的中心问题 ——
> 见 [设计题通用清单 · 第 1 步](<../_resources/design-checklist.md>)。

**LC-0348 的具体体现**：不去扫整个棋盘判胜负，而是维护
`rows[r]`、`cols[c]`、`diag`、`anti`，落子时 `+1`（玩家 1）或 `-1`（玩家 2），
某个计数的绝对值达到 `n` 就赢 ⟹ `move` 从 **O(n)** 降到 **O(1)**。

### ③ 「不真删」往往比「真删」快一整个量级

| 技巧 | 做法 | 比什么快 |
|---|---|---|
| **逻辑删除**（LC-1472） | `last = cur`，旧内容留着但不可达 | 比 `del arr[cur+1:]`（**O(n)**）快 |
| **版本链**（LC-1146） | 只在值真的改变时追加一项 | 比 `snap()` 复制整个数组（**O(length)**）快 |
| **持久缓冲**（LC-0158） | 多读的字符留着，不丢 | 丢了就**数据错误**，不只是慢 |

---

## 核心不变量

**LC-0158**：
> `buf4[i : cnt]` 恒为「已从文件读出但**尚未交付**给调用方」的字符。
> 这个区间**跨 `read` 调用持久存在**。

**LC-1472**：
> `history[0 : last+1]` 恒为**当前可达**的历史；`cur` 恒在 `[0, last]` 内。
> `history[last+1:]` 是已作废的旧数据（物理存在，逻辑不可达）。

**LC-1396**：
> `id in in_transit` ⟺ 乘客 `id` 已 `checkIn` 但尚未 `checkOut`。
> `totals[(a,b)] == (所有 a→b 行程的总时长, 次数)`。

**LC-1146**：
> `history[i]` 恒为按 `snap_id` **升序**的变更点序列，首项是哨兵 `(-1, 0)`。
> 查询 `get(i, s)` = 找最后一个 `id <= s` 的项。

**LC-0348**：
> `rows[r]` 恒为「第 `r` 行上，玩家 1 的落子数减玩家 2 的落子数」。
> `abs(rows[r]) == n` ⟺ 该行被某一方占满。

---

## 为什么这些实现是对的

### LC-0158：为什么多读的字符必须留？

`read4` 粒度是 4，`n` 可以是任意数。
若 `n = 1`，一次 `read4` 读回 4 个 —— 本次只用 1 个，**剩下 3 个必须留着**，
否则下一次 `read` 会从文件的第 5 个字符开始 ⟹ **丢数据**。

**实测反例**（文件 `"abcdefg"`，连续 `read(buf,1)` 四次）：

| 实现 | 输出 |
|---|---|
| **持久缓冲区** ✅ | `a`, `b`, `c`, `d` |
| 丢掉多读字符 ❌ | `a`, `e`, ``, `` ← **b, c, d 永久丢失** |

（这个反例在该题的 `solution.py` 里用 `Solution_3_BROKEN` **实际跑出来**了。）

**为什么 `cnt == 0` 才代表文件结束（而不是 `cnt < 4`）？**
`read4` 的契约只保证「最多 4 个」，**不保证**「没到文件尾就一定给 4 个」。
按 `cnt < 4` 判终止是**依赖实现而非契约** —— 面试会被追问。

### LC-1472：为什么 `visit` 要把 `last` 设成 `cur`？

真实浏览器：后退几步后打开新页面 ⟹ **原来的前进历史消失**。
不真删（O(n)），只把 `last = cur` ⟹ `forward` 的上界变成 `cur`
⟹ **旧的前进历史在逻辑上不可达** ⟹ O(1)。

**为什么需要 `last` 而不是 `len(history) - 1`？**
采用「覆盖写」时，数组长度 ≠ 有效长度：
visit 5 次（`len == 6`）→ `back(3)`（`cur == 2`）→ 再 visit ⟹ 写在下标 3，`last = 3`，
但 `len(history)` 还是 6（下标 4、5 是作废数据）⟹ 必须用 `last`。

### LC-1146：为什么 `get` 是「找最后一个 `id <= snap_id`」？

版本链记录的是**变更点**。链 `[(-1,0), (2,5), (7,9)]` 的含义是：
快照 0、1 时是 0；快照 2 到 6 是 5；快照 7 以后是 9。
所以查 `snap_id` 要找「不超过它的最大版本号」⟹ **upper_bound - 1**：
```python
j = bisect_right(chain, (snap_id, float('inf'))) - 1
```
**为什么不用 `bisect_left`？** 链里若恰好有 `snap_id` 这一项，
`bisect_left` 会停在它上面，`-1` 之后就**少取一项**。

**为什么哨兵用 `(-1, 0)`？** `-1` 比任何真实 `snap_id`（从 0 开始）都小
⟹ 二分**一定能找到它** ⟹ 从未 `set` 过的位置返回初值 0，**不会越界**。

---

## Python 核心模板

```python
# ① 跨调用持久缓冲区（LC-0158）
def read(self, buf, n):
    written = 0
    while written < n:
        if self.i == self.cnt:                # ! 缓冲区空了 ⟹ 抓一批
            self.cnt = read4(self.buf4); self.i = 0
            if self.cnt == 0: break           # ! 只有 0 才是文件结束
        buf[written] = self.buf4[self.i]
        self.i += 1; written += 1
    return written                            # ! 返回实际读到的数，不是 n

# ② 数组 + 游标 + 有效长度（LC-1472）
def visit(self, url):
    self.cur += 1
    if self.cur < len(self.history): self.history[self.cur] = url
    else:                           self.history.append(url)
    self.last = self.cur                      # ! 逻辑删除前进历史，O(1)

def back(self, steps):
    self.cur = max(0, self.cur - steps)       # ! 不够退就退到头
    return self.history[self.cur]

def forward(self, steps):
    self.cur = min(self.last, self.cur + steps)   # ! 不够进就进到尾
    return self.history[self.cur]

# ③ 增量聚合（LC-1396）
def checkOut(self, id, station, t):
    start, t0 = self.in_transit.pop(id)       # ! pop = 读取 + 立即删除
    e = self.totals[(start, station)]         # ! key 是有序对，方向不能混
    e[0] += t - t0; e[1] += 1                 # ! 只存标量，不存明细

def getAverageTime(self, a, b):
    total, count = self.totals[(a, b)]
    return total / count                      # ! O(1)

# ④ 版本链 + 二分（LC-1146）
def set(self, index, val):
    chain = self.history[index]
    if chain[-1][0] == self.snap_id: chain[-1] = (self.snap_id, val)   # ! 同周期覆盖
    else:                            chain.append((self.snap_id, val))

def snap(self):
    self.snap_id += 1; return self.snap_id - 1     # ! O(1)：不复制任何数据

def get(self, index, snap_id):
    chain = self.history[index]
    return chain[bisect_right(chain, (snap_id, float('inf'))) - 1][1]

# ⑤ 增量行列计数（LC-0348）
def move(self, row, col, player):
    d = 1 if player == 1 else -1
    self.rows[row] += d; self.cols[col] += d
    if row == col:            self.diag += d
    if row + col == self.n-1: self.anti += d
    if self.n in (abs(self.rows[row]), abs(self.cols[col]), abs(self.diag), abs(self.anti)):
        return player
    return 0
```

---

## 时间与空间复杂度

| 题 | 操作 | 时间 | 空间 |
|---|---|---|---|
| LC-0157 / LC-0158 | `read(buf, n)` | **O(n)** | **O(1)**（缓冲固定 4 字符） |
| LC-0348 | `move` | **O(1)** | **O(n)**（4 个计数数组） |
| LC-1472 | `visit` / `back` / `forward` | **全部 O(1)** | O(访问总数) |
| LC-1396 | 三个方法 | **O(1) 平均** | **O(在途数 + 站点对数)** |
| LC-1146 | `set` / `snap` | **O(1)** | **O(length + set 次数)** |
| | `get` | **O(log k)** | — |

⚠️ **LC-1146 的 `get` 不是 O(1)** —— 不要声称「全部 O(1)」。
⚠️ **LC-1396 的空间不是 O(总行程数)** —— 这正是增量聚合的收益。
⚠️ **LC-1472 双栈版的 `back(steps)` 是 O(steps)**，游标版才是 O(1)。

---

## 代表题目

| # | 题 | 优先级 | 核心技巧 |
|---|---|---|---|
| 1 | [LC-0157 Read N Characters Given Read4](<./01 - Buffered Reader 与跨调用状态/01 - LC-0157 - Read N Characters Given Read4>) | P2 | 单次读取，可丢残留 |
| 2 | [LC-0158 read4 II - Call Multiple Times](<./01 - Buffered Reader 与跨调用状态/02 - LC-0158 - Read N Characters Given read4 II - Call Multiple Times>) ★ | P1 | **跨调用持久缓冲区** |
| 3 | [LC-0348 Design Tic-Tac-Toe](<./02 - 棋盘状态与历史导航/01 - LC-0348 - Design Tic-Tac-Toe>) | P1 | **增量行列计数** |
| 4 | [LC-1472 Design Browser History](<./02 - 棋盘状态与历史导航/02 - LC-1472 - Design Browser History>) ★ | P1 | 游标 + **逻辑删除** |
| 5 | [LC-1396 Design Underground System](<./03 - 多对象状态与增量平均值/01 - LC-1396 - Design Underground System>) ★ | P1 | **增量聚合** |
| 6 | [LC-1146 Snapshot Array](<./04 - 版本快照与历史访问/01 - LC-1146 - Snapshot Array>) ★ | P1 | **版本链 + 二分** |

★ = 本次新增（0158 / 1472 / 1396 第一轮；1146 第二轮）。
⚠️ **LC-0157、LC-0158、LC-0348 是 LeetCode Premium 题目**
（LC-0158 因此没有 PDF，详见 `_audit` 报告）。

---

## 典型边界情况

| 题 | 边界 | 期望 |
|---|---|---|
| LC-0158 | `n = 0` | 返回 0，**不调用 `read4`** |
| | 文件比 `n` 短 | 返回**实际**读到的数 |
| | **`n` 不是 4 的倍数** | 多读的字符必须留存 |
| | 读完后继续 `read` | 恒返回 0 |
| LC-1472 | `back(100)` 在首页 | 停在 homepage，**不报错** |
| | `visit` 后立刻 `forward(1)` | **停在原地**（前进历史已作废） |
| | `back(0)` / `forward(0)` | 原地不动 |
| LC-1396 | 同一乘客多次乘车 | `in_transit` 每次必须清掉 |
| | **方向相反**的两条线路 | 必须是**两个独立 key** |
| | 起点 == 终点 | 合法，不特判 |
| LC-1146 | 从未 `set` 过的位置 | **0**（哨兵生效） |
| | 同周期内多次 `set` 同一位置 | **只留最后一次** |
| | `snap()` 之间没有 `set` | 两张快照值相同，链不增长 |
| LC-0348 | 对角线 / 反对角线 | `row == col` / `row + col == n-1` 要分别判 |

---

## 典型反例

| 错误做法 | 反例 | 结果 |
|---|---|---|
| LC-0158 丢掉 `read4` 多读的字符 | `"abcdefg"`，连续 `read(1)` 四次 | 得 `a, e, '', ''` ⟹ **b,c,d 丢失** ❌ |
| LC-0158 用 `cnt < 4` 判文件结束 | 契约允许少给 | 依赖实现而非契约 ⚠️ |
| LC-0158 返回 `n` 而不是 `written` | 文件比 n 短 | 返回值错 ❌ |
| LC-1472 用 `del history[cur+1:]` | 大量 visit | `visit` 退化成 **O(n)** ⟹ 最坏 O(n²) ⚠️ |
| LC-1472 用 `len(history)-1` 当前进上界 | 覆盖写 + back + visit | 能前进到**作废数据** ❌ |
| LC-1472 用双栈 | `back(10000)` | **O(steps)** 而非 O(1) ⚠️ |
| LC-1396 `checkOut` 后不删在途记录 | 乘客多次乘车 | 内存泄漏 + 语义错 ❌ |
| LC-1396 key 用 `frozenset({a,b})` | A→B 和 B→A | **两个方向被混在一起** ❌ |
| LC-1396 存所有行程时长的列表 | 大量行程 | `getAverageTime` 退化成 **O(k)** ⚠️ |
| LC-1146 `snap()` 复制整个数组 | `length=5e4`，`snap` 5e4 次 | **25 亿** ⟹ MLE/TLE ❌ |
| LC-1146 哨兵用 `(0, 0)` | `get(i, 0)` | 和真实快照 0 混淆 ❌ |
| LC-1146 用 `bisect_left` | 链里恰好有 `snap_id` | **少取一项** ⟹ 返回上一个版本的值 ❌ |
| LC-0348 每次 `move` 扫全盘 | `n` 很大 | **O(n)** 而非 O(1) ⚠️ |

---

## 容易混淆的 Pattern

### 两个方向的「挪成本」

| | **更新时多做**（LC-1396、LC-0348） | **查询时多做**（LC-1146） |
|---|---|---|
| 优化谁 | **查询** 变 O(1) | **更新**（`snap`）变 O(1) |
| 代价 | 更新多一点常数 | 查询变 O(log k) |
| 何时选 | 查询频繁 | 更新（快照）频繁 |

### 逻辑删除 vs swap-with-last

| | **逻辑删除**（LC-1472） | **swap-with-last**（[Level 03](<../03 - Randomized Data Structures>)） |
|---|---|---|
| 数组内容 | 旧内容留着，只缩有效长度 | 真的移动元素，保持紧凑 |
| 顺序 | **保持** | **被打乱** |
| 适用 | 关心顺序（前进/后退） | 不关心顺序 + 要随机访问 |

### LC-0157 vs LC-0158（本 Level 2 的全部内容）

| | LC-0157 | **LC-0158** |
|---|---|---|
| `read` 调用次数 | **一次** | **多次** |
| 多读的字符 | 可以**直接丢** | **必须留到下次** |
| 需要的状态 | 无（纯局部变量） | **实例字段** |

### LC-1146 vs LC-0981（为什么 1146 归在 Design）

| | LC-0981 Time Based KV（在 `05-binary-search`） | **LC-1146** 本题 |
|---|---|---|
| 版本号 | 调用方**传入**的 timestamp | 系统**自增**的 snap_id |
| 版本粒度 | 每次 `set` 一个版本 | **一次 `snap()` 才切一个版本** |
| 考点 | **二分找版本** | **怎么设计存储让 `snap` 变 O(1)** |

**二分只是 LC-1146 的手段，不是考点** —— 所以它归在 Design。

---

## 相关资料

- [设计题通用清单](<../_resources/design-checklist.md>) — 开场五步 + 六个套路
- [Pattern Recognition Guide](<../_resources/pattern-recognition-guide.md>) — Q7 / Q9 / Q10 / Q11 / Q12
