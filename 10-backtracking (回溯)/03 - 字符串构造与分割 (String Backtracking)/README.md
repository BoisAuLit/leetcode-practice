# Level 1 · 03 字符串构造与分割 (String Backtracking)

两类问题，骨架不同：
- **01 逐位置生成**：每一步决定「这个位置放什么字符」。
- **02 分割**：每一步决定「下一段切到哪里」。

## 01 - 逐位置字符串生成与前缀约束

### LC-0017 Letter Combinations（最纯粹的多叉枚举）
每个数字对应 3–4 个字母，第 i 层就是第 i 个数字的候选集。
**没有去重、没有剪枝**，纯笛卡尔积。
复杂度 O(4^n · n)。
**唯一的坑**：输入为空串时返回 `[]` 而不是 `[""]`。

### LC-0022 Generate Parentheses（**前缀约束剪枝**，本节重点）
不要先生成所有 2^(2n) 个字符串再筛 —— 要在生成过程中就剪掉非法分支。

```python
def dfs(path, open_cnt, close_cnt):
    if len(path) == 2 * n: res.append("".join(path)); return
    if open_cnt < n:                      # 还能放左括号
        path.append('('); dfs(path, open_cnt + 1, close_cnt); path.pop()
    if close_cnt < open_cnt:              # ★ 右括号数必须始终 <= 左括号数
        path.append(')'); dfs(path, open_cnt, close_cnt + 1); path.pop()
```

**两个条件就是全部的剪枝**：
- `open_cnt < n`：左括号不能超过 n 个。
- **`close_cnt < open_cnt`**：这是合法括号序列的**前缀性质** ——
  任意前缀中右括号数都不能超过左括号数。
  一旦违反，后面怎么补都救不回来 ⟹ 整个分支砍掉。

**「前缀一旦非法就永远非法」是剪枝成立的根本理由**，值得单独记住 ——
它和 LC-0020 Valid Parentheses 的栈判据是同一条性质的两种用法。

复杂度：O(Catalan(n) · n)，第 n 个卡特兰数约 4^n / n^1.5。
**不是 O(2^(2n))** —— 剪枝之后只生成合法的那些。

> **跨专题**：LC-0022 常被列进 Stack 题单，但**标准解法是回溯**，
> 所以主归属在本专题。04-stack-queue 只建索引。

## 02 - 字符串分割与合法片段判断

### 共同骨架
```python
def dfs(start, parts):
    if start == len(s): res.append(parts[:]); return
    for end in range(start + 1, len(s) + 1):
        seg = s[start:end]
        if 合法(seg):
            parts.append(seg); dfs(end, parts); parts.pop()
```
**枚举「下一段切到哪里」**，`合法()` 换一下就是另一道题。

### LC-0131 Palindrome Partitioning vs LC-0093 Restore IP Addresses

| | LC-0131 | LC-0093 |
|---|---|---|
| 段数 | **不固定** | **恰好 4 段** |
| 合法条件 | 是回文 | 0–255 且**无前导零** |
| 段长 | 任意 | **1–3**（最大 255） |
| 额外剪枝 | 不回文就不递归 | 段数够了 / **剩余长度检查** |
| 复杂度 | O(2^n · n) | **O(1)**（段数和段长都有常数上界） |

### LC-0131 的优化
朴素做法每次 `seg == seg[::-1]` 是 O(len)。
可以先用 **区间 DP** 预处理 `is_pal[i][j]`（O(n²)），
之后每次判断 O(1)。总体从 O(2^n · n) 降到 O(2^n)。

### LC-0093 的三条剪枝
1. 长度 < 4 或 > 12 ⟹ 直接无解。
2. **剩余长度检查**：剩 `r` 段时，剩余字符数必须在 `[r, 3r]` 内。
3. **前导零**：`len(seg) > 1 and seg[0] == '0'` ⟹ 非法。
   `"0"` 合法，`"01"` 不合法 —— 这是最常漏的一条。
   硬核用例：`"010010"` → `["0.10.0.10", "0.100.1.0"]`。

## 题目

| # | 题 | 优先级 |
|---|---|---|
| 01/01 | LC-0017 Letter Combinations of a Phone Number | **P0** |
| 01/02 | LC-0022 Generate Parentheses | **P0** |
| 02/01 | LC-0131 Palindrome Partitioning | **P0** |
| 02/02 | LC-0093 Restore IP Addresses | P1 |

## 常见错误
- LC-0017 输入空串时返回了 `[""]`。
- LC-0022 先全生成再过滤（复杂度爆炸），或者剪枝条件写成 `close_cnt <= open_cnt`。
- LC-0131 每次重新判回文而不预处理（能过，但说不清复杂度）。
- LC-0093 漏掉前导零判断。
- LC-0093 没做剩余长度剪枝（能过，但分支多很多）。
- 分割类题忘了 `parts.pop()`。

## 复习时的 Pattern Recognition
> 「每个位置填什么」 → 逐位置生成，想清楚**前缀约束**能不能剪枝。
> 「把字符串切成若干段」 → 枚举下一段的结束位置，想清楚**合法片段**的判据。
