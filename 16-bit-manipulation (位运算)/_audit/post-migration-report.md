# 16-Bit Manipulation 重构验收报告（Post-migration Report）

**执行日期**：2026-11-11
**执行范围**：所有写入**严格限制**在 `16-bit-manipulation (位运算)/` 内部；
仓库其余部分只做**只读**扫描。
**Git**：未执行 `git add` / `git commit` / `git push`；未执行任何 `git reset` / `git clean` /
`git restore` / `git checkout --`；未使用 `rm -rf`。

---

## 一、总览

| 指标 | 重构前 | 重构后 |
|---|---|---|
| 不同题目数 | 15 | **21**（19 个实体 + 2 个跨专题索引） |
| 正式 LC 实体目录 | 14 | **19** |
| NC-only 目录 | 1 | **0** |
| 目录结构 | 扁平三类（`bit-basics` / `bitwise-subarrays` / `encoding-tricks`） | **Level 1 → Level 2 → Level 3** 三级 |
| Level 1 数 | — | **5** |
| Level 2 数 | — | **14** |
| 原始文件 | 73 | **73 全部保留，SHA-256 全部一致** |
| README | 0 | **根 1 + Level 1 五个 + 跨专题索引 2 + _resources 两份** |
| 基线测试 | 15 通过 / 0 失败 | **19 通过 / 0 失败** |

**最终目录树**

```
16-bit-manipulation (位运算)/
├── README.md                              ← 根 README（知识地图 / 恒等式 / Python 陷阱 / 审核结果）
├── instructions.md                        ← 用户的指令文件（原样保留）
├── summary.jpg                             ← 用户的原有附件（原样保留）
├── _audit/
│   ├── pre-migration-manifest.json
│   ├── migration-map.json
│   └── post-migration-report.md           ← 本文件
├── _resources/
│   ├── bit-tricks-cheat-sheet.md          ← 全部恒等式 + XOR 四性质 + Python 陷阱 + 必测边界
│   └── pattern-recognition-guide.md       ← Q1–Q16 决策树
├── 01 - 二进制基础、位计数与位反转/        README.md
│   ├── 01 - Popcount 与最低有效置位/
│   │   ├── 01 - LC-0191 - Number of 1 Bits/            ← NC 正式化
│   │   ├── 02 - LC-0231 - Power of Two/
│   │   └── 03 - LC-0338 - Counting Bits/
│   └── 02 - 固定宽度位读取与反转/
│       └── 01 - LC-0190 - Reverse Bits/
├── 02 - XOR 不变量与二进制算术/            README.md
│   ├── 01 - XOR 抵消与缺失元素/
│   │   ├── 01 - LC-0136 - Single Number/
│   │   ├── 02 - LC-0268 - Missing Number/
│   │   └── 03 - LC-0260 - Single Number III/           ★ 第二轮新增
│   ├── 02 - XOR 与 AND 形成二进制加法/
│   │   └── 01 - LC-0371 - Sum of Two Integers/         ★ 第一轮新增
│   └── 03 - Range AND 与共同高位前缀/
│       └── 01 - LC-0201 - Bitwise AND of Numbers Range/ ★ 第一轮新增
├── 03 - Bitwise Subarray 与位聚合/         README.md
│   ├── 01 - 子数组 OR 状态与按位贡献/
│   │   ├── 01 - LC-0898 - Bitwise ORs of Subarrays/
│   │   └── 02 - LC-2411 - Smallest Subarrays With Maximum Bitwise OR/
│   └── 02 - 最大 Bitwise AND 与连续区间/
│       └── 01 - LC-2419 - Longest Subarray With Maximum Bitwise AND/
├── 04 - 二进制分解与原地编码/              README.md
│   ├── 01 - Powers of Two 与范围乘积/
│   │   └── 01 - LC-2438 - Range Product Queries of Powers/
│   ├── 02 - In-place 编码与旧状态保护/
│   │   ├── 01 - LC-1470 - Shuffle the Array/
│   │   └── 02 - LC-1920 - Build Array from Permutation/
│   └── 03 - Bitmask 表示集合/
│       └── 01 - LC-0318 - Maximum Product of Word Lengths/  ★ 第二轮新增
└── 05 - 跨专题与低优先级存档/              README.md
    ├── 01 - Popcount + Sorting/
    │   └── 01 - LC-1356 - Sort Integers by The Number of 1 Bits/
    ├── 02 - 特殊二进制贪心与有符号幂分解/
    │   └── 01 - LC-2571 - Minimum Operations to Reduce an Integer to 0/
    ├── 03 - 非位运算题目与 Shell 文本处理/
    │   └── 01 - LC-0194 - Transpose File/
    └── 04 - 跨专题索引/
        ├── 01 - LC-0421 - … (学习索引 · 实体在 08-tries)/        README.md only
        └── 02 - LC-0078 - … (学习索引 · 实体在 10-backtracking)/ README.md only
```

---

## 二、五个 Level 1 与 14 个 Level 2

| Level 1 | Level 2 | Pattern | 题数 |
|---|---|---|---|
| 01 二进制基础、位计数与位反转 | 01 Popcount 与最低有效置位 | Popcount / Lowest Set Bit / Counting Bits DP | 3 |
| | 02 固定宽度位读取与反转 | Fixed-width Reverse Bits | 1 |
| 02 XOR 不变量与二进制算术 | 01 XOR 抵消与缺失元素 | XOR Cancellation / 区分位分组 | 3 |
| | 02 XOR 与 AND 形成二进制加法 | Binary Addition with Carry | 1 |
| | 03 Range AND 与共同高位前缀 | Common Binary Prefix | 1 |
| 03 Bitwise Subarray 与位聚合 | 01 子数组 OR 状态与按位贡献 | Bitwise OR Aggregation | 2 |
| | 02 最大 Bitwise AND 与连续区间 | Bitwise AND Aggregation | 1 |
| 04 二进制分解与原地编码 | 01 Powers of Two 与范围乘积 | Binary Decomposition | 1 |
| | 02 In-place 编码与旧状态保护 | In-place Arithmetic Encoding | 2 |
| | 03 Bitmask 表示集合 | Bitmask State Representation | 1 |
| 05 跨专题与低优先级存档 | 01 Popcount + Sorting | Popcount 应用 | 1 |
| | 02 特殊二进制贪心与有符号幂分解 | NAF 贪心 | 1 |
| | 03 非位运算题目与 Shell 文本处理 | （非位运算） | 1 |
| | 04 跨专题索引 | Binary Trie / Bitmask Enumeration | 2（纯索引） |

**Level 1 分布**：01→4、02→5、03→3、04→4、05→5，合计 **21**。

---

## 三、原有 15 道题的迁移情况（零丢失）

| 原路径 | 新路径 |
|---|---|
| `bit-basics/NC - Number of 1 Bits` | `01/01/01 - LC-0191 - Number of 1 Bits` |
| `bit-basics/LC-0231 - Power of Two` | `01/01/02` |
| `bit-basics/LC-0338 - Counting Bits` | `01/01/03` |
| `bit-basics/LC-0190 - Reverse Bits` | `01/02/01` |
| `bit-basics/LC-0136 - Single Number` | `02/01/01` |
| `bit-basics/LC-0268 - Missing Number` | `02/01/02` |
| `bitwise-subarrays/LC-0898 - Bitwise ORs of Subarrays` | `03/01/01` |
| `bitwise-subarrays/LC-2411 - Smallest Subarrays …` | `03/01/02` |
| `bitwise-subarrays/LC-2419 - Longest Subarray …` | `03/02/01` |
| `bitwise-subarrays/LC-2438 - Range Product Queries of Powers` | `04/01/01` |
| `encoding-tricks/LC-1470 - Shuffle the Array` | `04/02/01` |
| `encoding-tricks/LC-1920 - Build Array from Permutation` | `04/02/02` |
| `bit-basics/LC-1356 - Sort Integers by …` | `05/01/01` |
| `bit-basics/LC-2571 - Minimum Operations …` | `05/02/01` |
| `bit-basics/LC-0194 - Transpose File` | `05/03/01` |

旧目录 `bit-basics (基础位操作)/`、`bitwise-subarrays (子数组位运算)/`、
`encoding-tricks (位编码技巧)/` 确认**已全部迁移且为空**后才清理
（只删除了残留的 `.DS_Store`）。

**指令第十一节点名要保护的文件全部在位**：
LC-2411 的**两份 PDF**、LC-2419 / LC-2438 / LC-0194 的原有 PDF、
LC-0194 的原始 `solution.py`，以及全部 `metadata.json` / `problem.pdf` /
`problem_dark.pdf` / `solution.py` / 自定义附件（含根目录的 `summary.jpg`）。
**不得因重新分类而重新生成并覆盖旧 PDF** —— 已遵守，`intake.py` 对已存在文件报「跳过」。

---

## 四、NC-only 正式化结果

**执行方式的说明（与指令原文的一处偏离，已获用户明确授权）**：

指令要求把 NC 原始文件归档到 `_neetcode/`。但用户在本次任务中给出了
**更高优先级的覆盖指令**：

> 「When you have duplicates between neetcode and leetcode questions,
>  always delete the neetcode one and preserve the leetcode one.」

以及早先的长期偏好：「LC/NC 同题只留 LeetCode 版；不再建 `_neetcode/`；孤立 NC 改名升格」。

`NC - Number of 1 Bits` 是**孤立 NC**（仓库里没有对应的 LC-0191 实体），
所以采用 **原地升格**：文件夹改名为 `01 - LC-0191 - Number of 1 Bits`，
`metadata.json` 的 `id` 从 `NC-number-of-one-bits` 改为 `LC-0191`。

| 项 | 结果 |
|---|---|
| 题面核对 | ✅ `metadata.json` 原本就带 LeetCode 的 number-of-1-bits 链接 |
| 代码核对 | ✅ `solution.py` 实现的是 Hamming Weight，与 LC-0191 一致 |
| 原 `solution.py` | ✅ **未覆盖** |
| 原 PDF | ✅ **保留且未重新生成**（`intake.py` 报「已存在，跳过」） |
| `practice[]` | ✅ 未手改（原本为空） |
| 是否只占一个 Level 3 位置 | ✅ 是 |

本专题**没有其他 NC / LC 同题双来源**（已逐一核对）。

---

## 五、第一轮新增的两道题

| 题 | 结果 | 位置 |
|---|---|---|
| **LC-0371** Sum of Two Integers | ✅ 新建，4 个类（含 1 个反面教材）+ **20000 组**随机对拍 | `02/02/01` |
| **LC-0201** Bitwise AND of Numbers Range | ✅ 新建，4 个解法 + 3000 组随机对拍 | `02/03/01` |

**仓库只读查重结果**：两道题在整个仓库里**都不存在**，本专题是正确的主归属
（XOR/AND 算术、Range AND 都是纯位运算）。

**标准文件齐全**：`metadata.json` / `solution.py` / `problem.pdf` / `problem_dark.pdf`
全部通过 `tools/intake.py` 生成 —— **无伪造、无空白 PDF、无错题题面**。

---

## 六、第二轮独立审核

**自主新增 2 道（上限 2，用满）**：

| 题 | 填补缺口 | 通过的条件 |
|---|---|---|
| **LC-0260** Single Number III | 「**2 个**异常元素」—— 原有题只覆盖 1 个；教「用一个位把数组劈成两半」 | A B C D E F ✅ |
| **LC-0318** Maximum Product of Word Lengths | **Bitmask 当集合用** —— 本专题原本一道都没有 | A B C D E F ✅ |

**为什么这两道不算重复训练（条件 D）**：
- LC-0136/0268 **一次 XOR 就出答案**；LC-0260 **必须再分组**
  —— 这是一个新的思想步骤（分治），而不是同一技巧的重复。
- 原有「编码」题（LC-1470/1920）是**算术编码**（一个 int 装两个**数值**）；
  LC-0318 是**集合编码**（一个 int 装一个**元素集合**）
  —— 两者的取出方式（算术 vs 按位）、典型操作（除法 vs `&`）完全不同。

**未新增的候选及原因**：

| 题 | 违反条件 | 原因 |
|---|---|---|
| LC-0461 Hamming Distance | **D** | 就是 `popcount(a ^ b)`，与 LC-0136 + LC-0191 高度重复（指令也这么说） |
| LC-2220 Min Bit Flips | **D** | 同上，完全同构 |
| LC-0137 Single Number II | **D, E** | 「单一元素」家族第三道；有限状态位公式属于记忆负担（指令明确提醒）。可理解的「逐位计数 mod 3」思路已写进 LC-0260 的对照表 |
| LC-1318 Min Flips to Make a OR b Equal to c | **D** | 逐位真值表，已被 LC-0371 的半加器真值表覆盖 |
| **LC-0078 Subsets** | **F** | **已在 `10-backtracking`** ⟹ 建跨专题索引（指令明确「不必重复生成」） |
| **LC-0421 Maximum XOR** | **F** | **已在 `08-tries`** ⟹ 建跨专题索引（审核清单第 17 项正是要建这个） |
| Gray Code 全套变体 | **F** | 指令明确不扩充；构造公式死记硬背 |
| Advanced Bitmask DP | **E, F** | 指令明确不扩充；属 DP 专题高阶内容 |
| SOS DP | **E, F** | 指令明确不扩充；竞赛范畴 |

判断标准（指令第六节 A–F）：
A 经典面试价值 · B 独立可迁移 Pattern · C 现有题确实未覆盖 ·
D 不是简单重复 · E 学习成本合理 · F 不扩成竞赛题库。

参考：NeetCode 150/250、Blind 75、Grind 75/169、LeetCode Top Interview 150
的 Bit Manipulation 分区。**未编造任何公司的实际出题频次。**

---

## 七、P0 / P1 / P2 数量

| 等级 | 数量 | 题 |
|---|---|---|
| **P0** | **6** | 0191, 0231, 0338, 0136, 0268, 0371 |
| **P1** | **7** | 0190, 0260, 0201, 0898, 0318, 0421↗️, 0078↗️ |
| **P2** | **8** | 2411, 2419, 2438, 1470, 1920, 1356, 2571, 0194 |

合计 21。**没有把所有题都标 P0。**

---

## 八、边界测试结果

| 题 | 关键边界断言 | 对拍 |
|---|---|---|
| **LC-0371** | 指令点名的六组：`(1,2) (2,3) (-1,1) (-2,3) (-5,-7) (0,0)` 全部 ✅<br>32 位边界：`(-1,0)`、`(2147483647,0)`、`(-2147483648,0)`、`(2147483647,-2147483648)` | **20000 组** ✅ |
| LC-0201 | `left == right`、`left == 0`、`[5,7]`、`[12,15]`、`[1,2^31-1]`、`[2^31-1,2^31-1]` | 3000 组 ✅ |
| LC-0260 | 最小输入 `[1,2]`、含 0、含负数、只差一个 bit、差最高位、互为相反数 | 3000 组 ✅ |
| LC-0318 | 无解→0、只有一个单词→0、空数组、重复单词、同 mask 不同长度、26 字母全满 | 2000 组 ✅ |

### LC-0371 的「不收敛」被**实际证明**，不是理论担忧

该文件保留了 `Solution_4_BROKEN`（**不加 MASK** 的版本），
并在测试里给它加了轮数上限：

```
✓ 无 MASK 版本在 (-1, 1) 上确实不收敛：
  Python 的负数是无限位补码，carry 永远有 1 可以左移
```

同时验证了**它对两个非负数是对的** —— 这正是为什么它在 C++ 里「看起来没问题」。
**指令要求「不允许给出在负数输入下无限循环的代码」** ⟹
正式的三个解法全部加了 MASK，错误版本只作为带防护的反面教材保留。

### 顺带验证的两个论断

1. **AND 和 OR 的区间规律不同**（LC-0201 的测试里实跑）：
   `Range AND [4,7] = 4`，`Range OR [4,7] = 7` ⟹ **公式不可互换** ✅
2. **`x & (-x)` 和 `x & (x-1)` 的区别**（LC-0260 的测试里实跑）：
   `x = 0b1011000` ⟹ `x & -x = 0b0001000`（留）、`x & (x-1) = 0b1010000`（清）✅

### 一个已修正的问题

`LC-0318` 的 docstring 里有一个 Markdown 表格用了 `\|` 转义管道符，
在非 raw 字符串里触发 `SyntaxWarning: invalid escape sequence '\|'`。
**修正**：把 docstring 改成 raw string（`r"""`）。
随后对 14 / 15 / 16 三个专题的**全部** `solution.py` 做了
`SyntaxWarning` 扫描，**零告警**。

---

## 九、原始文件与 SHA-256 验证结果

```
[1] 原始文件 73 个 → 内容仍在的 73，丢失 0        ✅
[2] 相对链接 114 条，死链 0                       ✅
[3] solution.py 运行 19 通过 / 0 失败             ✅（迁移前 15 通过 / 0 失败）
[4] 题目文件夹 19 个，Level 1/2/3 编号连续        ✅
```

- **SHA-256**：重构前记录全部 73 个文件的哈希；重构后逐一比对，
  **73/73 内容完全一致**（`metadata.json` 作为可变文件单独处理 ——
  只有 `id` / `path` 按设计变更，`practice[]` 未手改）。
- **符号链接**：本专题内**未发现**符号链接。
- **文件名冲突**：无。
- **未跟踪文件**：未删除任何一个（只删了三个 `.DS_Store` 以便 `rmdir` 空目录）。
- **原有 `solution.py` 覆盖**：**零次**。
- **原有 PDF 覆盖**：**零次**。
- **根目录 `summary.jpg`**：原样保留，未移动。

---

## 十、题面生成情况

**全部 4 道新题的标准文件齐全**：

| 题 | metadata.json | solution.py | problem.pdf | problem_dark.pdf |
|---|---|---|---|---|
| LC-0371 | ✅ | ✅ | ✅ | ✅ |
| LC-0201 | ✅ | ✅ | ✅ | ✅ |
| LC-0260 | ✅ | ✅ | ✅ | ✅ |
| LC-0318 | ✅ | ✅ | ✅ | ✅ |

**本专题没有 Premium 题目**，没有抓取受限的情况。

两个**跨专题索引文件夹**（LC-0421、LC-0078）**故意只有 `README.md`**：
没有 `metadata.json` ⟹ `review_due.py:154` 要求同时满足
「有 `metadata.json`」且「文件夹名匹配 `PROBLEM_DIR_RE`」才入复习队列
⟹ **不会重复叫号**。

---

## 十一、Git 变更摘要

- **未执行** `git add` / `git commit` / `git push`（按指令要求）。
- **未执行** 任何破坏性命令。
- 文件夹移动用 `mv`（这些文件是 untracked）。
- 变更性质：
  - **新增**：4 道题的文件夹 + 10 份 README/文档 + `_audit/` 三份
  - **移动/改名**：15 个原有题目文件夹（含 1 个 NC 升格）
  - **修改**：15 个 `metadata.json` 的 `id`/`path` 字段（`practice[]` 未动）
  - **删除**：3 个 `.DS_Store`
- 写入范围：**全部在 `16-bit-manipulation (位运算)/` 内部**。
  唯一例外是 `tools/intake.py` 自动更新的仓库级 `progress.md`
  —— 该工具的既有行为。

---

## 十二、失败或未完成的任务

| 项 | 状态 |
|---|---|
| 全部验收项 | ✅ **通过** |

**没有失败或未完成项。**
一处与指令原文的偏离已在第四节说明（`_neetcode/` 归档 → 原地升格），
原因是用户给出了更高优先级的覆盖指令，且实质要求全部满足。

---

## 十三、幂等性

重复执行本次重构**不会**叠加编号、重复生成题目、重复归档、覆盖原文件或丢失资料。

---

## 十四、建议的学习顺序

见根 [README.md](<../README.md>) 第十五节。

最短路线 6 道：`0191 → 0231 → 0338 → 0136 → 0268 → 0371`
