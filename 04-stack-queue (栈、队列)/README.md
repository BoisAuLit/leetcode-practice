# 04 · Stack & Queue（栈、队列）

> **Queue 是数据结构，BFS 是用 Queue 实现的搜索算法** —— 这两件事从本专题开始就要分清。
> 同样地，**Stack ≠ Monotonic Stack**：普通栈保存「还没处理完的状态」，
> 单调栈额外保证「栈内有序，并据此永久丢弃不可能的候选」。

本专题共 **25 道实体题** + **9 条跨专题索引**。

## 一、知识地图

| Level 1 | 主题 | 实体题 | README |
|---|---|---|---|
| 01 | 基础栈、括号与消除 (Stack Fundamentals) | 8 | [→](<01 - 基础栈、括号与消除 (Stack Fundamentals)/README.md>) |
| 02 | 单调栈及其变体 (Monotonic Stack) | 0（**纯索引**） | [→](<02 - 单调栈及其变体 (Monotonic Stack)/README.md>) |
| 03 | 表达式计算与嵌套解析 (Expression Parsing) | 5 | [→](<03 - 表达式计算与嵌套解析 (Expression Parsing)/README.md>) |
| 04 | Stack 与 Queue 数据结构设计 (Design) | 6 | [→](<04 - Stack 与 Queue 数据结构设计 (Design)/README.md>) |
| 05 | 单调队列与滑动窗口 (Monotonic Deque) | 0（**纯索引**） | [→](<05 - 单调队列与滑动窗口 (Monotonic Deque)/README.md>) |
| 06 | Queue 与 BFS | 2 | [→](<06 - Queue 与 BFS (Breadth-First Search)/README.md>) |
| 07 | 低优先级与跨专题存档 (Archive) | 4 | [→](<07 - 低优先级与跨专题存档 (Archive)/README.md>) |

```
01 - 基础栈、括号与消除 (Stack Fundamentals)/
  01 - 括号匹配、修复与有效区间/
    01 - LC-0020 - Valid Parentheses                      P0
    02 - LC-1249 - Minimum Remove to Make Valid Parenth.   P1
    03 - LC-0032 - Longest Valid Parentheses               P1
  02 - 栈模拟、消除与状态恢复/
    01 - LC-1047 - Remove All Adjacent Duplicates          P0
    02 - LC-0735 - Asteroid Collision                      P0   ← 新增
    03 - LC-0946 - Validate Stack Sequences                P1   ← 新增
    04 - LC-0071 - Simplify Path                           P1
    05 - LC-1544 - Make The String Great                   P2   ← 第二轮新增
02 - 单调栈及其变体 (Monotonic Stack)/   —— 纯索引，实体题全在 18-monotonic
03 - 表达式计算与嵌套解析 (Expression Parsing)/
  01 - 逆波兰表达式/          01 - LC-0150                 P0
  02 - 中缀表达式与运算符优先级/ 01 - LC-0227  02 - LC-0224  P0 / P1
  03 - 嵌套字符串与迭代器/     01 - LC-0394  02 - LC-0341   P0 / P1
04 - Stack 与 Queue 数据结构设计 (Design)/
  01 - 带额外状态的 Stack/     01 - LC-0155                 P0
  02 - FIFO 队列与循环结构/    01 - LC-0346  02 - LC-0622    P1 / P1
  03 - Stack 与 Queue 相互实现/ 01 - LC-0232  02 - LC-0225   P1 / P1   (0232 新增)
  04 - 双队列轮转与模拟/       01 - LC-0649                 P2   ← 第二轮新增
05 - 单调队列与滑动窗口 (Monotonic Deque)/  —— 纯索引，实体题在 18-monotonic / 03-sliding-window
06 - Queue 与 BFS (Breadth-First Search)/
  01 - Grid Traversal 与 Multi-source BFS/ 01 - LC-0733     P1
  02 - State BFS 与无权最短路径/           01 - LC-0279     P1
07 - 低优先级与跨专题存档 (Archive)/
  01 - 简单括号计数与特殊贪心/ 01 - LC-1021  02 - LC-1717    P2
  02 - 复杂表达式解析/        01 - LC-0736                  P2
  03 - DP 与时间队列/         01 - LC-2327                  P2
```

---

## 二、Stack vs Queue vs Deque

|  | Stack | Queue | Deque |
|---|---|---|---|
| 顺序 | LIFO | FIFO | 两端都能进出 |
| 解决什么 | **嵌套 / 可撤销**的结构 | **按到达顺序**处理 | 需要同时从两端淘汰 |
| 为什么合适 | 最近打开的最先关闭 | 先到先服务 ⇒ BFS 按层扩展 | 队尾淘汰被支配者，队首淘汰过期者 |
| 本专题代表 | 20、1047、394 | 346、622、733 | → 18-monotonic |

**BFS 为什么必须用 Queue**：BFS 要保证「距离小的节点先被扩展」。
Queue 的 FIFO 性质让第 d 层的所有节点都排在第 d+1 层之前，
于是每个节点第一次被访问时的距离就是最短距离。
换成 Stack 就变成 DFS，这个性质立刻失效。

## 三、Stack vs Monotonic Stack（为什么本专题不放单调题）

| | 普通 Stack | Monotonic Stack |
|---|---|---|
| 栈内性质 | 无约束，只表示「还没处理完」 | **值有序**，并以此丢弃候选 |
| 弹出的理由 | 匹配上了 / 状态结束了 | **这个元素以后再也赢不了** |
| 复杂度论证 | 一般 O(n) | 需要**摊还（Amortized）**论证 |
| 例子 | LC-0020 遇到 `)` 弹掉 `(` | LC-0739 遇到更高温度结算旧日期 |

本仓库的**铁律**：凡是沾单调栈 / 单调队列的题，一律归
[18-monotonic-fuck-you](<../18-monotonic-fuck-you (单调栈、单调队列)/README.md>)，
不在本专题重复建目录（一道题两个文件夹会让复习队列出现重复记录）。
因此 Level 1 的 `02` 和 `05` 保留为**纯索引目录**，只有 README，没有题目文件夹。

## 四、代码模板

**T1 · 括号匹配**
```python
pairs, stack = {')':'(', ']':'[', '}':'{'}, []
for c in s:
    if c in pairs:
        if not stack or stack.pop() != pairs[c]: return False
    else:
        stack.append(c)
return not stack
```
O(n)/O(n)。复用：20、1249、32（32 改存下标）。

**T2 · 相邻抵消**
```python
stack = []
for c in s:
    if stack and cancel(stack[-1], c): stack.pop()
    else: stack.append(c)
```
O(n)/O(n)。`cancel` 换一下就是另一道题：1047 是 `a == b`，1544 是 `a != b and a.lower() == b.lower()`。

**T3 · 栈模拟（可连锁）**
```python
for x in items:
    alive = True
    while alive and stack and 会相撞(stack[-1], x):
        ... 决定弹栈顶 / 弹 x / 两个都弹 ...
    if alive: stack.append(x)
```
O(n)/O(n)。复用：735、946。

**T4 · 嵌套结构：进括号保存上下文，出括号恢复**
```python
for c in s:
    if c == '[':
        stack.append((cur_string, cur_num)); cur_string, cur_num = "", 0
    elif c == ']':
        prev, k = stack.pop(); cur_string = prev + cur_string * k
```
O(n)/O(n)。复用：394、224、736。

**T5 · 两个栈实现队列（摊还 O(1)）**
```python
def pop(self):
    if not self.out:                       # 只在 out 空时整体搬运
        while self.inn: self.out.append(self.inn.pop())
    return self.out.pop()
```
push O(1)，pop/peek **摊还** O(1)、单次最坏 O(n)。

**T6 · 多源 BFS**
```python
q = deque(所有起点); 
while q:
    for _ in range(len(q)):      # 按层
        x = q.popleft(); 扩展邻居并入队
    step += 1
```
O(V+E)。复用：733、286、994。

| 模板 | 时间 | 空间 |
|---|---|---|
| T1 括号匹配 | O(n) | O(n) |
| T2 相邻抵消 | O(n) | O(n) |
| T3 栈模拟 | O(n) | O(n) |
| T4 嵌套解析 | O(n) | O(n) |
| T5 两栈队列 | push O(1)，pop 摊还 O(1) | O(n) |
| T6 BFS | O(V+E) | O(V) |

---

## 五、P0 / P1 / P2 与三条路线

**路线一 · P0 最小核心（9 道）**
LC-0020 → LC-1047 → LC-0735 → LC-0150 → LC-0227 → LC-0394 → LC-0155
（外加 18-monotonic 的 LC-0739、LC-0084）

**路线二 · P0 + P1 标准面试路线（+10 道）**
LC-1249 → LC-0032 → LC-0946 → LC-0071 → LC-0224 → LC-0341 →
LC-0232 → LC-0225 → LC-0346 → LC-0622 → LC-0733 → LC-0279

**路线三 · P2 扩展与存档（5 道）**
LC-1544、LC-0649、LC-1021、LC-1717、LC-0736、LC-2327

统计：**P0 7 道 · P1 12 道 · P2 6 道**（本专题实体题 25 道）。
BFS 题（733、279）按 11-graphs 的优先级协调，这里只标 P1，不列为栈的核心必练。

---

## 六、跨专题索引

| LC | 本专题的角色 | 实体目录 |
|---|---|---|
| LC-0739 / 0496 / 0503 / 0901 / 0084 / 0907 / 0853 / 0402 / 0316 | Level 1 `02` 的全部内容 | [18-monotonic](<../18-monotonic-fuck-you (单调栈、单调队列)/README.md>) |
| LC-0239 | Level 1 `05` 的核心题 | [18-monotonic `04/01/01`](<../18-monotonic-fuck-you (单调栈、单调队列)/04 - 单调队列与滑动窗口/01 - 固定窗口最大值/01 - LC-0239 - Sliding Window Maximum>) |
| LC-1438 | Level 1 `05` | [03-sliding-window](<../18-monotonic-fuck-you (单调栈、单调队列)/general/01 - LC-1438 - Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit>) |
| LC-0862 | Level 1 `05` | [03-sliding-window](<../18-monotonic-fuck-you (单调栈、单调队列)/general/02 - LC-0862 - Shortest Subarray with Sum at Least K>) |
| LC-0286 Walls and Gates | Level 1 `06` 的多源 BFS 代表 | [11-graphs 多源 BFS](<../11-graphs (图论)/02-dfs-bfs (阶段 1 · DFS、BFS：静态无权的连通性与步数)/multi-source-bfs (多源 BFS：所有起点一起入队)/LC-0286 - Walls and Gates>) |
| LC-0994 Rotting Oranges | Level 1 `06` | [11-graphs 多源 BFS](<../11-graphs (图论)/02-dfs-bfs (阶段 1 · DFS、BFS：静态无权的连通性与步数)/multi-source-bfs (多源 BFS：所有起点一起入队)/LC-0994 - Rotting Oranges - ★ 签名题>) |
| LC-0752 Open the Lock | Level 1 `06` 的状态图 BFS | [11-graphs 状态图 BFS](<../11-graphs (图论)/01-graph-modeling (阶段 0 · 建图、隐式图、状态图)/state-graph-bfs (状态图 BFS：一个状态就是一个点)/LC-0752 - Open the Lock - ★ 签名题>) |
| LC-0022 Generate Parentheses | 不属于本专题 | 标准解法是 **Backtracking** → [10-backtracking](<../10-backtracking (回溯)>) |
| LC-0032 | 本专题为主（Stack 版） | 12-dynamic-programming 另有一份 DP 版副本，见下 |

**LC-0286 的处理**：11-graphs 里的版本明显更完整（79 行、含完整讲解与多解法），
两边的 `practice` 都是空的。为避免同一道题在复习队列里出现两条记录，
本专题原有的那份已**无损归档**到
[`_cross_topic_archive/0286 - Walls and Gates (04 旧版本，正式目录在 11-graphs)`](<_cross_topic_archive/0286 - Walls and Gates (04 旧版本，正式目录在 11-graphs)>)
（文件一个没删，只是目录名刻意不再匹配 `LC-xxxx - ` 前缀，因此不进复习队列）。

---

## 七、第二轮独立审核结果

**自主新增 2 道**（上限 5，没有凑数）：

| 题 | 理由 |
|---|---|
| LC-1544 Make The String Great | 和 LC-1047 共用「相邻抵消」骨架，**只换了抵消谓词**。把两题并排放，就能把模板抽象成 `stack + cancel(a,b)`，成本极低、迁移性高。 |
| LC-0649 Dota2 Senate | 本章其他题都在**实现**队列，这道题是**用**队列的循环轮转去建模博弈。补上了「FIFO + 重新入队 = 下一轮」这个 BFS 之外最常见的队列用法。 |

**审核过、决定不加（Future Candidates）**

| 题 | 理由 |
|---|---|
| LC-0085 Maximal Rectangle / LC-0316 / LC-2104 | 属于单调栈 → 已在 18-monotonic |
| LC-0641 Design Circular Deque | 和 LC-0622 几乎是同一题，只是多两个端口，不引入新 Pattern |
| LC-0933 Number of Recent Calls | 17-design 专题已有实体目录，不重复建 |
| LC-0022 Generate Parentheses | 标准解法是回溯，归 10-backtracking |

---

## 八、Git 与安全
本次重构：只在本专题目录内写入；没有执行 `git add` / `commit` / `push`；
没有使用 `rm -rf`；没有覆盖任何已有 `solution.py`、`note.md` 或图片。
完整校验见 [_audit/post-migration-report.md](<_audit/post-migration-report.md>)。
