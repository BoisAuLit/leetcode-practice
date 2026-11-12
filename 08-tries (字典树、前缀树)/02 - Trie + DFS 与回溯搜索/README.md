# Level 1 · 02 Trie + DFS 与回溯搜索

## 核心定义
Trie 不只是查表，它还可以**当成一棵搜索树来 DFS**。
本章两道题分别代表「在 Trie 内部分支搜索」和「用 Trie 给外部搜索剪枝」。

## 01 - LC-0211 Design Add and Search Words（通配符 `.`）

### 决定性观察
1. **普通字符**：只有一条路可走 ⟹ `node.children[c]`，确定性下降。
2. **`.`**：可以匹配任意字符 ⟹ 必须**尝试当前节点的所有 children**，变成**分支搜索**。
3. DFS 的状态是 `(node, index)`：当前走到 Trie 的哪个节点、匹配到 word 的第几个字符。

```python
def dfs(node, i):
    if i == len(word): return node.is_end        # 走完了，还要 is_end 才算单词
    c = word[i]
    if c == '.':
        return any(dfs(child, i + 1) for child in node.children.values())
    return c in node.children and dfs(node.children[c], i + 1)
```

### 什么时候 True / False
- **True**：走完整个 word **且**落点 `is_end == True`。
- **False**：某一步走不动（字符不在 children 里），或走完了但 `is_end == False`。
- `.` 的分支里**只要有一条成功就 True**（`any`），全失败才 False。

### 复杂度 —— 不要说成 O(L)
- 没有 `.` 时确实是 **O(L)**。
- 全是 `.` 时，每一层都要展开所有 children，**最坏退化成遍历整棵 Trie**：
  O(节点数)，也可以写成 O(26^L) 的上界（实际受 Trie 实际节点数限制）。
- **正确说法**：「不含通配符时 O(L)；通配符越多，分支越宽，最坏 O(Trie 节点数)。」

## 02 - LC-0212 Word Search II（Trie 剪枝 + 网格回溯）

> 本专题的 **P0 进阶核心题**。必须先熟练 LC-0208 和 LC-0211 再来。

### 为什么需要 Trie
朴素做法：对 `words` 里每个单词单独在 board 上搜一次 ⟹ **O(len(words) × 搜索代价)**。
不同单词之间**完全没有共享**：搜 `"oath"` 和 `"oat"` 时，前三步是重复的。

Trie 把所有单词的前缀**合并**成一棵树，于是：
**一次 DFS 可以同时推进所有以当前路径为前缀的候选单词。**

### 剪枝为什么成立
DFS 走到格子 `(r,c)`，如果 `board[r][c]` 不在当前 Trie 节点的 children 里，
说明**没有任何一个单词**的下一个字符是它 ⟹ 这条路完全没希望 ⟹ **立刻返回**。
这一行剪枝是本题能过的关键。

### 两个职责要分清
| | 负责什么 |
|---|---|
| **Trie** | 候选单词的前缀集合、什么时候该剪枝、什么时候凑成了一个完整单词 |
| **DFS + visited** | 在 board 上怎么走、不走回头路、走完回溯 |

### 三个实现细节
1. **防止同一条路径重用格子**：进入时 `board[r][c] = '#'`（或用 visited 集合），
   **递归返回后必须恢复**（回溯）。
2. **避免重复返回同一个单词**：推荐在 Trie 节点上存 `node.word = 完整单词`，
   找到后 `res.add(...)` 并把 `node.word = None` **置空**（相当于「摘掉」这个单词）。
   这比用 set 去重更高效。
3. **可选的进一步优化**：找到单词后，如果该 Trie 节点变成叶子（没有 children），
   可以把它从父节点删掉，让 Trie 随着搜索逐渐变小。
   **但删除必须小心**，只删「已被找到且无子节点」的分支。

### 复杂度
最坏 O(M × N × 4^L)，L 是最长单词长度；Trie 剪枝让实际远低于这个上界。
空间 O(Σ|word|) 的 Trie + O(L) 的递归栈。

## 题目

| # | 题 | 优先级 |
|---|---|---|
| 01/01 | LC-0211 Design Add and Search Words Data Structure | **P0** |
| 02/01 | LC-0212 Word Search II | **P0**（进阶） |

## 常见错误
- LC-0211 遇到 `.` 时只试第一个 child。
- LC-0211 走完 word 后忘了检查 `is_end`。
- LC-0211 宣称复杂度恒为 O(L)。
- LC-0212 忘记回溯恢复 `board[r][c]`。
- LC-0212 同一个单词被返回多次（没有置空 `node.word`）。
- LC-0212 对每个单词各跑一次 DFS（白白丢掉了 Trie 的全部意义）。

## 复习时的 Pattern Recognition
> 「支持通配符的字典查询」 → Trie + 分支 DFS。
> 「在网格/图里同时找一批单词」 → Trie 剪枝 + 回溯。
