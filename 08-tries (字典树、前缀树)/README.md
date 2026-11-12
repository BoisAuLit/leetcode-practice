# 08 · Tries（字典树、前缀树）

> Trie 只有**一个**数据结构和**三个**操作（insert / search / startsWith）。
> 所有变化都来自两件事：**节点上挂什么附加信息**，以及**怎么在 Trie 上做 DFS**。

本专题共 **15 道题**，5 个 Level 1。

## 一、Trie 的本质（整个专题的地基）

```python
class TrieNode:
    children: dict[str, TrieNode]   # 每条边 = 一个字符
    is_end: bool                    # 从根到这里是不是一个完整单词
```

**三条不变量**：
1. **每条边代表一个字符**，从根到任意节点的路径 = 一个前缀。
2. **共享前缀 ⟹ 共享节点**。这就是 Trie 省空间、也省时间的根源：
   `"app"`、`"apple"`、`"apply"` 的前三个字符只占 3 个节点。
3. **`is_end` 和「节点存在」是两件事**：
   - `search(word)` 必须检查 `is_end`（`"app"` 存在不代表它是个单词）
   - `startsWith(prefix)` **不检查** `is_end`（只要路径走得通）

**复杂度**（L = 单词长度，Σ|w| = 所有单词总长度）：
| 操作 | 时间 | 说明 |
|---|---|---|
| insert / search / startsWith | **O(L)** | **与单词数量无关** —— 这是 Trie 打败 Hash Set 的地方 |
| 建树 | O(Σ&#124;w&#124;) | |
| 空间 | O(Trie 节点数) ≤ O(Σ&#124;w&#124;) | 共享前缀越多越省 |

**重复插入**同一个单词是幂等的（路径已存在，只是再把 `is_end` 置 True），
但如果节点上挂了计数（LC-2416），**重复插入必须照常累加**。

## 二、目录地图

| Level 1 | 主题 | 题数 | README |
|---|---|---|---|
| 01 | Trie 基础结构与前缀匹配 | 3 | [→](<01 - Trie 基础结构与前缀匹配/README.md>) |
| 02 | Trie + DFS 与回溯搜索 | 2 | [→](<02 - Trie + DFS 与回溯搜索/README.md>) |
| 03 | Trie 前缀统计与搜索应用 | 4 | [→](<03 - Trie 前缀统计与搜索应用/README.md>) |
| 04 | Trie + DP 与字符串划分 | 1 | [→](<04 - Trie + DP 与字符串划分/README.md>) |
| 05 | 进阶变体与跨专题存档 | 4 | [→](<05 - 进阶变体与跨专题存档/README.md>) |

```
01 Trie 基础结构与前缀匹配/
  01 Trie 基础操作与最短前缀/  01 LC-0208(NC→)  02 LC-0648←新  03 LC-0720←新₂
02 Trie + DFS 与回溯搜索/
  01 通配符查找与分支搜索/     01 LC-0211(NC→)
  02 Grid Backtracking 与剪枝/ 01 LC-0212(NC→)
03 Trie 前缀统计与搜索应用/
  01 自动补全与前缀聚合/       01 LC-1268  02 LC-2416←新
  02 层级路径与前缀过滤/       01 LC-1233
  03 流式匹配与后缀 Trie/      01 LC-1032←新₂
04 Trie + DP 与字符串划分/     01 LC-3291
05 进阶变体与跨专题存档/
  01 Bitwise Trie 与最大 XOR/  01 LC-0421←新
  02 Common Prefix 非 Trie 解/ 01 LC-0014  02 LC-3043
  03 字符串区间标注/           01 LC-0616
_resources/  docs/Trie.png   utils/TrieUtils.py
```

## 三、核心模板

**T1 · 标准 Trie（LC-0208）**
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

def insert(root, word):
    node = root
    for c in word:
        node = node.children.setdefault(c, TrieNode())
    node.is_end = True

def search(root, word):          # 要 is_end
    node = walk(root, word)
    return node is not None and node.is_end

def starts_with(root, prefix):   # 不要 is_end
    return walk(root, prefix) is not None
```

**T2 · Trie + DFS 通配符（LC-0211）**
```python
def dfs(node, i):
    if i == len(word): return node.is_end
    c = word[i]
    if c == '.':
        return any(dfs(child, i + 1) for child in node.children.values())  # 所有分支
    return c in node.children and dfs(node.children[c], i + 1)             # 单条路径
```
**复杂度不是 O(L)**：全是 `.` 时会退化成遍历整棵 Trie，最坏 O(节点数)。

**T3 · Trie 剪枝 + 网格回溯（LC-0212）**
```python
def dfs(r, c, node):
    ch = board[r][c]
    if ch not in node.children: return      # Trie 里没有这条路 → 立刻剪枝
    nxt = node.children[ch]
    if nxt.word: res.add(nxt.word); nxt.word = None   # 去重
    board[r][c] = '#'                       # 标记已用
    for 四个方向: dfs(...)
    board[r][c] = ch                        # 回溯恢复
```
**职责分离**：Trie 管「候选单词的前缀」，DFS 管「网格上的空间搜索」。

**T4 · Trie Augmentation（LC-2416 / LC-1268）**
在节点上挂附加字段，**插入时沿路维护**：
```python
node.count += 1        # LC-2416：有多少单词经过这个前缀
node.top3.append(w)    # LC-1268：这个前缀下字典序最小的 3 个
```

**T5 · Bitwise Trie（LC-0421）**
边从 26 个字母变成 2 个 bit，**从最高位插入**，查询时优先走相反 bit。

**T6 · 反向 Trie（LC-1032）**
**单词反着插 + 流反着走** ⟹ 后缀匹配变成前缀匹配。

## 四、什么时候**不该**用 Trie

| 题 | 更好的解法 | 为什么 |
|---|---|---|
| **LC-0014** Longest Common Prefix | 纵向扫描 / 排序后比首尾 | 只有一次查询，建 Trie 的开销不划算 |
| **LC-1233** Remove Sub-Folders | **排序 + 前缀检查** | 排序后父目录必在子目录之前，一遍扫描即可 |
| **LC-3043** Longest Common Prefix of Two Arrays | Hash Set 存所有数字前缀 | 是 **Digit Trie** 不是 String Trie，用 set 更简单 |
| **LC-1268** Search Suggestions | 排序 + 二分 | 两种都对，Trie 版在多次查询时更优 |

**判据**：Trie 的优势是「**多次前缀查询**」和「**共享前缀的批量匹配**」。
只查一次、或者只比较两个字符串，用不着 Trie。

**LC-1233 的坑**：`/a` 和 `/ab` 中，`/ab` **不是** `/a` 的子目录。
判断必须是 `child.startswith(parent + "/")`，不能只 `startswith(parent)`。

## 五、P0 / P1 / P2

**P0** LC-0208、LC-0211、LC-0212
**P1** LC-0648、LC-1268、LC-2416、LC-1032
**P2** LC-0720、LC-1233、LC-3291、LC-0421、LC-0014、LC-3043、LC-0616

### 推荐学习顺序
```
A 打地基   208 → 648 → 720
B DFS 分支 211 → 212          ← 212 是本专题的 P0 进阶核心题
C 前缀聚合 1268 → 2416 → 1032
D 组合应用 1233 → 3291
E 进阶存档 421 → 014 → 3043 → 616
```
**LC-0212 必须在 208 和 211 都熟练之后再练** —— 它同时需要 Trie 结构和网格回溯。

## 六、NC / LC 处理结果

原目录有 3 个 NC 来源，**全部是孤儿**（仓库里没有对应的 LC 目录），
按规则**升格**为正式 LC 编号，`practice` 原样保留，solution.py 一字未改：

| 原 NC | 升格为 |
|---|---|
| NC - Implement Trie (Prefix Tree) | LC-0208 |
| NC - Design Add and Search Word Data Structure | LC-0211 |
| NC - Word Search II | LC-0212 |

**没有 LC / NC 重复**，所以没有删除任何目录。

## 七、第二轮独立审核结果

**自主新增 2 道**（上限 4，没有凑数）：

| 题 | Pattern | 为什么值得加 |
|---|---|---|
| **LC-1032** Stream of Characters | **反向 Trie**（后缀匹配） | 前面所有题匹配的都是**前缀**，本题匹配**流的后缀**。「单词反着插 + 流反着走 ⟹ 后缀变前缀」是能迁移到 LC-0745 等一批题的技巧，本专题原本完全没有这个视角 |
| **LC-0720** Longest Word in Dictionary | **链式 is_end 约束** | 从「查一个点是否存在」升级到「查整条路径上每个节点都是 is_end」。只在 LC-0208 的 Trie 上加一个 DFS 条件，成本极低 |

**审核过、决定不加（Future Candidates）**

| 题 | 理由 |
|---|---|
| LC-0677 Map Sum Pairs | 也是 Trie Augmentation，和新增的 LC-2416 技能点重合（都是节点挂数值并沿路累加） |
| LC-1804 Implement Trie II | 就是 LC-0208 + LC-2416 的计数合并版，不引入新东西 |
| LC-0745 Prefix and Suffix Search | 需要「前缀+后缀拼接键」的技巧，值得学但学习成本明显高于收益；LC-1032 已经引入了反向 Trie 的核心思想 |
| LC-0676 Implement Magic Dictionary | 和 LC-0211 的通配符 DFS 高度重合（只是把 `.` 换成「恰好改一个字符」） |
| LC-1707 Maximum XOR With an Element | LC-0421 的离线查询加强版，前置依赖是排序 + 离线处理，不适合入门 |

## 八、跨专题提示（重复已全部清理）

| LC | 情况 |
|---|---|
| **LC-0014** | ~~本专题和 99-advanced 的 divide-and-conquer 各有一份实体目录~~ → **2026-11-11 已合并**，见下 |
| **LC-3291** | 本专题、[12-dynamic-programming](<../12-dynamic-programming (动态规划)/>)、[13-greedy 的 Jump Game II - Cluster](<../13-greedy (贪心)/01 - 跳跃、可达性与区间覆盖/02 - 最少跳跃与最远覆盖/01 - LC-0045 - Jump Game II>) **共三份** |

LC-3291 已统一成一份（见上）。

**LC-0014 的合并（2026-11-11）**：原先 `99-advanced (进阶专题)/divide-and-conquer (分治)/`
下另有一份实体目录，两份的代码还不一样 —— 本专题这份是 Trie 解法，那份是纵向扫描
（而且那个目录名写的是「分治」，代码其实不是分治）。处理方式：
保留本专题这份（它有复习记录 🟢 2026-10-04，且在正式三级结构里），
把那份的纵向扫描代码**原样搬入**成为 `Solution_3`（⭐️ 首选解法），
并补齐真正的分治 `Solution_4`、二分答案 `Solution_5`、排序比首尾 `Solution_6`。
原目录已移入废纸篓（未用 `rm -rf`）。**现在全仓库 LC-0014 只有一份实体目录。**

## 九、原有资料与安全
- `docs (资料)/Trie.png` 和 `utils/TrieUtils.py` 已搬到 [`_resources/`](<_resources>)，内容未改。
- 迁移前 9 个 solution.py **全部可运行**，迁移后仍然全部可运行（新增 5 道后共 14/14）。
- 未执行 `git add` / `commit` / `push`；未使用 `rm -rf`。

完整校验见 [_audit/post-migration-report.md](<_audit/post-migration-report.md>)。
