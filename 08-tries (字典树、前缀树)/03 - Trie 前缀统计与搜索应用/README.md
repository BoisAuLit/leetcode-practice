# Level 1 · 03 Trie 前缀统计与搜索应用

## 核心定义：Trie Augmentation（在节点上挂附加信息）
标准 Trie 的节点只有 `children` 和 `is_end`。
**本章的全部内容是：往节点上再挂点东西，让查询变快。**

> **挂什么，取决于你要查什么。**

| 题 | 节点上挂什么 | 回答什么查询 |
|---|---|---|
| LC-2416 | `count`（经过该节点的单词数） | 这个前缀出现了几次 |
| LC-1268 | `top3`（该前缀下字典序最小的 3 个单词） | 自动补全 |
| LC-1032 | （反向 Trie，不挂额外信息） | 流的后缀是不是某个单词 |

## 01 - 自动补全与前缀聚合

### LC-2416 Sum of Prefix Scores（Augmentation 的标准范例）
```python
# 插入：沿路每个节点都 +1（不是只在末尾）
for c in word:
    node = node.children.setdefault(c, TrieNode())
    node.count += 1
# 查询：沿路把 count 累加
for c in word:
    node = node.children[c]
    total += node.count
```

**三个必须讲清的点**：
1. **`count` 的语义是「有多少单词经过这个节点」**，也就是以该前缀开头的单词数。
2. **不能只统计完整单词的出现次数**：
   `["abc","ab","bc","b"]` 里前缀 `"ab"` 出现 2 次，但完整单词 `"ab"` 只有 1 次。
   题目数的是**前缀**出现次数，所以必须沿路累加。
3. **重复单词要照常计数**，不能去重：`["aa","aa"]` 中 `"aa"` 的分数是 2 + 2 = 4。

复杂度：建树 O(Σ|w|)，查询 O(Σ|w|)。对比暴力枚举所有前缀的 O(Σ|w|²)。

### LC-1268 Search Suggestions System
两种都对：
- **Trie 版**：每个节点预存「该前缀下字典序最小的 3 个单词」，查询 O(L)。
- **排序 + 二分版**：products 排序后，对每个前缀用 `bisect_left` 定位，
  再往后取最多 3 个且仍以该前缀开头的。O(n log n + L log n)。

**什么时候 Trie 更好**：查询次数多、前缀共享多时。
单次查询的话排序 + 二分更简单。

## 02 - 层级路径与前缀过滤（LC-1233）

**优先用排序，而不是 Trie。**
```python
folder.sort()
res = []
for f in folder:
    if not res or not f.startswith(res[-1] + "/"):
        res.append(f)
```
**为什么排序后一遍扫描就够**：字典序排序保证**父目录一定排在它的子目录之前**，
所以只需要和「上一个保留下来的目录」比较。

**最关键的坑**：
```
/a  和 /ab      →  /ab 不是 /a 的子目录！
```
判断必须是 `f.startswith(parent + "/")`，**不能只 `f.startswith(parent)`**。
Trie 版也要在节点上正确区分路径分隔符。

本题标 **P2** —— Trie 方案能做但不必背，排序方案才是面试的标准答案。

## 03 - 流式匹配与后缀 Trie（LC-1032）

**本节最有价值的技巧：反转 ⟹ 后缀变前缀。**

前面所有 Trie 题匹配的都是**前缀**（从单词开头往后走）。
LC-1032 要匹配「字符流的**后缀**」。做法：
1. 把每个 word **反着**插进 Trie。
2. 查询时从流的**最新字符往回走**。
3. 走到 `is_end` ⟹ 流的某个后缀是一个单词 ⟹ True；走不动 ⟹ 立刻停。

两个优化：
- 只需要保留流的**最后 L 个字符**（L = 最长单词长度），用 `deque(maxlen=L)`。
- 「走不动就 break」让平均情况远快于最坏。

复杂度：单次查询 **O(L)**，不是 O(1)，也不是 O(流长度)。

这个技巧能迁移到 LC-0745 Prefix and Suffix Search 等一批题。

## 题目

| # | 题 | 优先级 |
|---|---|---|
| 01/01 | LC-1268 Search Suggestions System | P1 |
| 01/02 | LC-2416 Sum of Prefix Scores of Strings | P1 |
| 02/01 | LC-1233 Remove Sub-Folders | P2 |
| 03/01 | LC-1032 Stream of Characters | P1 |

## 常见错误
- LC-2416 只在 `is_end` 处计数。
- LC-2416 对 words 去重。
- LC-1233 用 `startswith(parent)` 而漏掉 `+ "/"`。
- LC-1032 正着插单词（那样只能匹配前缀，匹配不了后缀）。
- LC-1032 不限长地保存整个流 ⟹ 查询退化。

## 复习时的 Pattern Recognition
> 「某个前缀出现了几次」「自动补全」 → Trie Augmentation，**节点上挂东西**。
> 「流的结尾是不是某个词」 → **反向 Trie**。
> 「父目录 / 子目录」 → 先想排序，Trie 是备选。


---

## 2026-11-11 新增题目（对照大厂高频题单补的缺口）

| 题 | 位置 | 信号 → 模式 | 备注 |
|---|---|---|---|
| [LC-1166 Design File System](<./02 - 层级路径与前缀过滤/02 - LC-1166 - Design File System>) | `03 - Trie 前缀统计与搜索应用/02 - 层级路径与前缀过滤` | 父路径 = path[:rfind('/')]，哈希表即可；Trie 版为 ls / rm -r 追问预留 | LC-1233 / LC-0588 同组；Premium 题 |

每道题的 `solution.py` 都带：全部主流解法（各自的复杂度与适用场景）、一个 ⭐️ Preferred、和一段对独立真值基线的随机对拍。
