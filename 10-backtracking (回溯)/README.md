# 10 · Backtracking（回溯）

> 回溯只有**一个**骨架。所有题的差别都在三件事上：
> **① 状态是什么　② 怎么剪枝　③ 怎么去重。**

本专题共 **19 道题** + 1 条跨专题索引，5 个 Level 1。

## 一、唯一的骨架

```python
def dfs(状态):
    if 到达终点:
        记录答案（列表要 path[:] 拷贝）
        return
    for 每个候选 choice:
        if 不合法: continue          # ← ② 剪枝
        if 本层已用过同样的选择: continue   # ← ③ 去重
        做出选择                      # path.append / 改格子 / 占用列
        dfs(新状态)
        撤销选择                      # path.pop / 恢复格子 / 释放列   ← 回溯
```

**三条铁律**：
1. **做出选择和撤销选择必须成对**。漏掉撤销，兄弟分支就会看到污染的状态。
2. **记录答案时必须拷贝**：`res.append(path[:])`。
   直接 `append(path)` 存的是同一个列表对象的引用，后续 pop 会把它改空。
3. **`start` 参数控制「不走回头路」**：组合/子集类题用 `dfs(i + 1)` 保证不重复选，
   允许重复选同一个元素时用 `dfs(i)`（LC-0039）。

## 二、去重的两种方式（本专题最该分清的一组）

> **去重去的是「同一层里的重复选择」，不是「同一条路径上的重复元素」。**
> 同一条路径上出现相同的值是合法的（`[1,1]` 本身就是答案）。

| | 排序 + 相邻跳过 | 每层 set |
|---|---|---|
| 写法 | `if i > start and nums[i] == nums[i-1]: continue` | `if nums[i] in used_this_level: continue` |
| 前提 | **允许排序** | **顺序不能动** |
| 例题 | LC-0090、LC-0040、LC-0047 | **LC-0491**（子序列不能排序！） |
| 额外空间 | O(1) | O(本层宽度) |

**LC-0491 存在的理由**：它是**不能排序**的场合 —— 排序会破坏子序列的原始顺序。
有了它，才知道「排序+相邻跳过」是有前提的。

## 三、目录地图

| Level 1 | 主题 | 题数 | README |
|---|---|---|---|
| 01 | 子集、组合与目标和 | 7 | [→](<01 - 子集、组合与目标和 (Subsets and Combinations)/README.md>) |
| 02 | 排列与重复元素去重 | 2 | [→](<02 - 排列与重复元素去重 (Permutations)/README.md>) |
| 03 | 字符串构造与分割 | 4 | [→](<03 - 字符串构造与分割 (String Backtracking)/README.md>) |
| 04 | 网格搜索与约束满足 | 6 | [→](<04 - 网格搜索与约束满足 (Constraint Search)/README.md>) |
| 05 | 回溯与记忆化的边界 | 0（纯索引） | [→](<05 - 回溯与记忆化的边界 (Backtracking vs DP)/README.md>) |

```
01 子集、组合与目标和/
  01 子集枚举与重复元素去重/  01 LC-0078(NC→)  02 LC-0090(NC→)  03 LC-0491←新₂
  02 固定数量的组合选取/      01 LC-0077
  03 目标和与元素复用限制/    01 LC-0039(NC→)  02 LC-0040(NC→)  03 LC-0216
02 排列与重复元素去重/        01 LC-0046(NC→)  02 LC-0047
03 字符串构造与分割/
  01 逐位置生成与前缀约束/    01 LC-0017(NC→)  02 LC-0022(NC→)
  02 字符串分割与合法片段/    01 LC-0131(NC→)  02 LC-0093←新
04 网格搜索与约束满足/
  01 网格路径与访问状态/      01 LC-0079(NC→)  02 LC-0980←新₂
  02 N-Queens 与冲突检查/     01 LC-0051(NC→)  02 LC-0052
  03 等和分桶与对称性剪枝/    01 LC-0698←新
  04 Sudoku 与多约束回溯/     01 LC-0037
05 回溯与记忆化的边界/        → 跨专题索引（LC-0494 实体目录在 12-DP）
```

## 四、四个模板

**T1 · 子集 / 组合（用 start 不走回头路）**
```python
def dfs(start, path):
    res.append(path[:])              # 子集：每个节点都是答案
    for i in range(start, n):
        path.append(nums[i])
        dfs(i + 1, path)             # i+1：每个元素最多用一次
        path.pop()
```
`dfs(i)` 而不是 `dfs(i+1)` ⟹ 元素可以重复使用（LC-0039）。

**T2 · 排列（用 used 数组，不用 start）**
```python
def dfs(path):
    if len(path) == n: res.append(path[:]); return
    for i in range(n):
        if used[i]: continue
        if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue  # 去重
        used[i] = True; path.append(nums[i])
        dfs(path)
        path.pop(); used[i] = False
```
**排列用 `used` 不用 `start`** —— 因为每个位置都可以从头挑。

**T3 · 字符串分割（枚举下一段的结束位置）**
```python
def dfs(start, parts):
    if start == len(s): res.append(parts[:]); return
    for end in range(start + 1, len(s) + 1):
        seg = s[start:end]
        if 合法(seg):
            parts.append(seg); dfs(end, parts); parts.pop()
```
复用：LC-0131（合法 = 回文）、LC-0093（合法 = 0–255 无前导零，且**段数固定为 4**）。

**T4 · 网格回溯（原地标记 + 恢复）**
```python
def dfs(r, c, ...):
    if 越界 or 不合法 or 已访问: return
    saved = grid[r][c]; grid[r][c] = 标记
    for 四个方向: dfs(...)
    grid[r][c] = saved               # ★ 必须恢复
```
复用：LC-0079、LC-0980、LC-0212（在 08-tries）。

| 模板 | 典型复杂度 |
|---|---|
| T1 子集 | O(2^n · n) |
| T1 组合 C(n,k) | O(C(n,k) · k) |
| T2 排列 | O(n! · n) |
| T3 分割 | O(2^n · n)（LC-0093 是 O(1)，段数固定） |
| T4 网格 | O(4^(m·n)) 最坏 |
| N-Queens | O(n!) |

**这类题的复杂度下界就是答案的规模** —— 要列出 2^n 个子集，就不可能比 O(2^n) 快。

## 五、剪枝才是分水岭（LC-0698 的四条）

LC-0698 不剪枝必 TLE，剪枝后很快。四条缺一不可：

1. **降序排序**：大的先放，失败尽早发生（fail-fast）。
2. **跳过相同容量的桶**：`if buckets[j] == buckets[j-1]: continue` ——
   消除桶之间的**对称性**，这条是复杂度从爆炸降到可行的关键。
3. **放不下就跳过**：`if buckets[j] + x > target: continue`。
4. **空桶等价**：放进空桶失败后 `break`，后面的空桶不用再试。

同样的「对称性剪枝」思想也出现在 N-Queens（第一行只需试前一半列）。

## 六、什么时候**不该**用回溯（Level 1 `05` 的意义）

> **要列出所有方案 ⟹ 只能回溯**（答案规模就是指数级，没法更快）。
> **只要数量 / 最优值 ⟹ 先找状态，能合并分支就上记忆化或 DP。**

**LC-0494 Target Sum** 就是这条分界线的教材：
```
① 朴素回溯 O(2^n)
② 发现状态 (i, cur) 可以合并 → 记忆化 O(n · S)
③ 数学转化成子集和 → 01 背包 O(n · sum)
```
**找到「状态」是唯一的思考步骤**，剩下都是套路。

同类判断：
| 题 | 要什么 | 该用什么 |
|---|---|---|
| LC-0078 Subsets | 所有子集 | 回溯（答案就有 2^n 个） |
| LC-0494 Target Sum | 方案**数** | **DP** |
| LC-0139 Word Break | 能否拆分（bool） | **DP**（见 12-dynamic-programming） |
| LC-0140 Word Break II | 所有拆分方案 | 回溯 + 记忆化 |

## 七、P0 / P1 / P2

**P0** LC-0078、LC-0090、LC-0039、LC-0040、LC-0046、LC-0047、LC-0017、LC-0022、LC-0131、LC-0079、LC-0051
**P1** LC-0077、LC-0216、LC-0052、LC-0093、LC-0698、LC-0494
**P2** LC-0037、LC-0491、LC-0980

### 推荐学习顺序
```
A 子集与组合   078 → 090 → 077 → 039 → 040 → 216
B 另一种去重   491                      ← 不能排序时怎么办
C 排列         046 → 047
D 字符串       017 → 022 → 131 → 093
E 网格与约束   079 → 980 → 051 → 052 → 698 → 037
F 边界         494（在 12-DP）         ← 什么时候该换成 DP
```

## 八、跨专题索引

| LC | 关系 | 位置 |
|---|---|---|
| LC-0212 Word Search II | **Trie 剪枝 + 网格回溯**，是 LC-0079 的批量版 | [08-tries](<../08-tries (字典树、前缀树)/02 - Trie + DFS 与回溯搜索/02 - Grid Backtracking 与 Trie 剪枝/01 - LC-0212 - Word Search II>) |
| LC-0113 Path Sum II | 树上的回溯（append / pop 配对） | [07-trees](<../07-trees (树)/03 - 路径 DFS、状态传递与 Prefix Sum/01 - 根到叶路径与路径状态/02 - LC-0113 - Path Sum II>) |
| LC-0139 / LC-0416 / **LC-0494** | 只要 bool / 计数 ⟹ DP 而不是回溯 | [12-dynamic-programming](<../12-dynamic-programming (动态规划)/>) |
| LC-0473 Matchsticks to Square | **就是 k=4 的 LC-0698**，故未单独收录 | — |

## 九、NC / LC 处理结果

**10 个 NC 来源全部是孤儿**（仓库里没有对应的 LC 目录），按规则**升格**为正式 LC 编号，
`practice` 原样保留，solution.py 一字未改：

| 原 NC | 升格为 | practice |
|---|---|---|
| NC - Subsets | LC-0078 | 0 |
| NC - Subsets II | LC-0090 | 0 |
| NC - Combination Sum | LC-0039 | 0 |
| NC - Combination Sum II | LC-0040 | 0 |
| NC - Permutations | LC-0046 | 0 |
| NC - Letter Combinations of a Phone Number | LC-0017 | **1 条** |
| NC - Generate Parentheses | LC-0022 | **1 条** |
| NC - Palindrome Partitioning | LC-0131 | 0 |
| NC - Word Search | LC-0079 | 0 |
| NC - N-Queens | LC-0051 | 0 |

**没有 LC / NC 重复，因此没有删除任何目录。**

## 十、第二轮独立审核结果

**自主新增 3 道**（上限 4，没有凑数）：

| 题 | Pattern | 为什么值得加 |
|---|---|---|
| **LC-0491** Non-decreasing Subsequences | **每层 set 去重** | 本专题原有的去重全靠「排序 + 相邻跳过」。这题**不能排序**（会破坏子序列顺序），逼出另一种去重技巧。有了它才知道原来那套是有前提的 |
| **LC-0980** Unique Paths III | 网格回溯 + **全覆盖约束 + 计数** | LC-0079 是「存在性」（找到就 return），本题是「计数」（必须走完整棵搜索树）+「必须覆盖所有空格」。两个新维度 |
| **LC-0494** Target Sum | **回溯 → 记忆化 → DP** | 专门用来界定「什么时候该停止回溯」。为此新开了 Level 1 `05`，因为这是本专题最该想清楚、却最容易被忽略的一件事 |

**审核过、决定不加（Future Candidates）**

| 题 | 理由 |
|---|---|
| LC-0473 Matchsticks to Square | **就是 k=4 的 LC-0698**，完全重复 |
| LC-0784 Letter Case Permutation | LC-0078 子集枚举的换皮版 |
| LC-0526 Beautiful Arrangement | 排列 + 剪枝，和 LC-0047 技能点重合 |
| LC-1593 Split a String Into Max Unique Substrings | 字符串分割 + set 去重，LC-0131 + LC-0491 已覆盖 |
| LC-0140 Word Break II | 回溯 + 记忆化，和新增的 LC-0494 定位重合；且 Word Break 系列主归属在 12-DP |

## 十一、修复的已有问题
**LC-0039 Combination Sum 原本跑不起来**：文件底部写的是
`s.combinationSum(input_)`，**少传了 target 参数** ⟹ `TypeError`。
已补上参数并注明，**没有改动任何解法代码**。
迁移前 14 通过 / 1 失败，迁移后 **20 / 20 全部通过**。

未执行 `git add` / `commit` / `push`；未使用 `rm -rf`。
完整校验见 [_audit/post-migration-report.md](<_audit/post-migration-report.md>)。
