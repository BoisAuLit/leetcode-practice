# Level 1 · 09 计数 DP 与多维状态

## 核心定义
前面几章的 dp 大多存「最优值」（max / min）。本章的 dp 存**方案数** ——
转移从 `max(...)` 变成 **`+=`**，同时经常需要**多开几维**来区分状态。

## 计数 DP 的三条通则

**① 初始化是 `1` 而不是 `0`**
`dp[0] = 1` 表示「空方案算一种」。设成 0 会让所有答案都是 0。

**② 转移是 `+=`（累加所有来源），不是 `max`**
```python
dp[i] += dp[i - 1]        # 每一种到 i-1 的方案都能延伸成到 i 的方案
```

**③ 要取模就每步都取**
`dp[i] = (dp[i] + dp[j]) % MOD` —— 不要只在最后取，中间会溢出（C++/Java）。

## 五个小节

### 01 - 线性计数与铺砖

**LC-0790 Domino and Tromino Tiling**：
状态不能只是「填满前 i 列的方案数」—— 还要区分**边界的形状**：
```
full[i]    = 前 i 列完全填满
partial[i] = 前 i 列填满、第 i+1 列多凸出一格
```
转移需要同时维护两个数组。**这是「一个状态不够就多开一维」的典型。**

**LC-0276 Paint Fence**：状态是「最后两根柱子**同色还是异色**」：
```
same[i] = 第 i 根和第 i-1 根同色的方案数
diff[i] = 不同色的方案数
same[i] = diff[i-1]              # 同色 ⟹ 前两根必须异色
diff[i] = (same[i-1] + diff[i-1]) * (k - 1)
```

### 02 - 骰子与受限序列计数

| 题 | 状态 | 转移 |
|---|---|---|
| **LC-1155** Dice Roll Sum | `dp[i][target]` = i 个骰子凑出 target 的方案数 | 枚举这个骰子掷出 1..k |
| **LC-1220** Count Vowels Permutation | `dp[i][vowel]` = 长度 i、以某元音结尾 | 按题给的**允许跟随关系**转移 |
| **LC-0935** Knight Dialer | `dp[i][digit]` = 跳 i 步、停在某数字 | 按**骑士跳跃图**转移 |

**这三题是同一个骨架**：
> `dp[步数][当前状态]`，转移按「允许的后继集合」展开。
> **LC-1220 和 LC-0935 的区别只是那张「谁能跟谁」的转移表。**

把转移关系写成一个邻接表 / 字典，代码就统一了。

### 03 - Paint House 与相邻状态限制

| 题 | 状态 | 复杂度 |
|---|---|---|
| **LC-0256** Paint House | `dp[i][3]`（3 种颜色） | O(n) |
| **LC-0265** Paint House II | `dp[i][k]`（k 种颜色） | 朴素 O(n·k²)，**优化到 O(n·k)** |
| **LC-1473** Paint House III | `dp[i][color][groups]` | O(n · k² · target) |

**LC-0265 的优化（本节最值钱的一点）**：
朴素转移要对每个颜色找「其他颜色的最小值」⟹ O(k) ⟹ 总 O(n·k²)。
优化：只维护上一行的**最小值**和**次小值**：
- 当前颜色 ≠ 上一行最小值的颜色 ⟹ 用最小值
- 相同 ⟹ 用**次小值**

⟹ O(1) 查询，总 O(n·k)。
> **「不能和上一个相同」这类限制，维护 min + second_min 就能 O(1) 转移。**
> 这个技巧可以直接迁移到很多题。

**LC-1473** 的状态要三维（位置、颜色、已形成的街区数），
是本章状态维度最多的一题，但转移逻辑是直接的。

### 04 - 多维决策与任务划分

| 题 | 状态 |
|---|---|
| **LC-1335** Minimum Difficulty of a Job Schedule | `dp[i][d]` = 前 i 个任务分 d 天的最小难度和；枚举「最后一天从哪开始」 |
| **LC-1770** Maximum Score from Multiplication | `dp[i][left]` = 用了 i 个乘数、左边取了 left 个（右边取了 `i - left` 个） |

**LC-1770 的状态压缩技巧**：
两端取数时，**「取了几个」和「左边取了几个」就能确定右边取了几个**
⟹ 不需要开 `dp[left][right]` 的二维，只需要 `dp[i][left]`。
**这是「两个维度有约束关系时压掉一维」的典型。**

### 05 - 特殊输入压缩

**LC-2787 Ways to Express an Integer as Sum of Powers**：
就是 **0-1 背包计数**（每个底数的 x 次幂最多用一次），
候选集合是 `{1^x, 2^x, ...}` 中不超过 n 的那些。
⟹ 倒序遍历（见 Level 1 `03`）。

## 题目总览

| # | 题 | 优先级 |
|---|---|---|
| 01/01 | LC-0790 Domino and Tromino Tiling | P1 |
| 01/02 | LC-0276 Paint Fence | P2 |
| 02/01 | LC-1155 Number of Dice Rolls With Target Sum | P1 |
| 02/02 | LC-1220 Count Vowels Permutation | P2 |
| 02/03 | LC-0935 Knight Dialer | P2 |
| 03/01 | LC-0256 Paint House | P2 |
| 03/02 | LC-0265 Paint House II | P2 |
| 03/03 | LC-1473 Paint House III | P2 |
| 04/01 | LC-1335 Minimum Difficulty of a Job Schedule | P2 |
| 04/02 | LC-1770 Maximum Score from Multiplication Operations | P2 |
| 05/01 | LC-2787 Ways to Express an Integer as Sum of Powers | P2 |

## 常见错误
- `dp[0]` 初始化成 0（计数题必须是 1）。
- 忘记每步取模。
- LC-0790 只用一个状态（没区分边界形状）。
- LC-0265 用朴素 O(n·k²) 而不维护 min/second_min。
- LC-1770 开了 `dp[left][right]` 的冗余二维。
- 转移时漏掉某个来源（计数题漏一个来源答案就偏小，而且不容易发现）。

## 复习时的 Pattern Recognition
> 「有多少种方案」 → 计数 DP：`dp[0] = 1`，转移用 `+=`，记得取模。
> 「状态说不清 / 转移写不出来」 → **多开一维**（上一个是什么颜色？边界什么形状？用了几次？）


---

## 2026-11-11 新增题目（对照大厂高频题单补的缺口）

| 题 | 位置 | 信号 → 模式 | 备注 |
|---|---|---|---|
| [LC-1531 String Compression II](<./04 - 多维决策与任务划分/03 - LC-1531 - String Compression II>) | `09 - 计数 DP 与多维状态/04 - 多维决策与任务划分` | dp[i][k]：删 s[i] 或「s[i] 开一段并向后吞掉相同字符」；enc_len 单独写成函数 | O(n²k) Hard |
| [LC-1986 Minimum Number of Work Sessions to Finish the Tasks](<./05 - 特殊输入压缩与计数 DP/02 - LC-1986 - Minimum Number of Work Sessions to Finish the Tasks>) | `09 - 计数 DP 与多维状态/05 - 特殊输入压缩与计数 DP` | 状压 dp[mask] = (session 数, 最后一个 session 已用)；元组比较即「先少 session 再少 used」 | 装箱问题 n ≤ 14 |

每道题的 `solution.py` 都带：全部主流解法（各自的复杂度与适用场景）、一个 ⭐️ Preferred、和一段对独立真值基线的随机对拍。
