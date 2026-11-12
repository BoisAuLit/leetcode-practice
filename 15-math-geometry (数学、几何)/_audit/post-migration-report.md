# 15-Math & Geometry 重构验收报告（Post-migration Report）

**执行日期**：2026-11-11
**执行范围**：所有写入**严格限制**在 `15-math-geometry (数学、几何)/` 内部；
仓库其余部分只做**只读**扫描。
**Git**：未执行 `git add` / `git commit` / `git push`；未执行任何 `git reset` / `git clean` /
`git restore` / `git checkout --`；未使用 `rm -rf`。

---

## 一、总览

| 指标 | 重构前 | 重构后 |
|---|---|---|
| 不同题目数 | 13 | **21**（19 个实体 + 2 个跨专题索引） |
| 正式 LC 实体目录 | 12 | **19** |
| NC-only 目录 | 1 | **0** |
| 目录结构 | 扁平三类（`matrix` / `arithmetic` / `geometry`） | **Level 1 → Level 2 → Level 3** 三级 |
| Level 1 数 | — | **4** |
| Level 2 数 | — | **11** |
| 原始文件 | 59 | **59 全部保留**（1 个为修 bug 做了纯新增，见第九节） |
| README | 0 | **根 1 + Level 1 四个 + 跨专题索引 2 + _resources 三份** |

**最终目录树**

```
15-math-geometry (数学、几何)/
├── README.md                              ← 根 README（知识地图 / 10 模板 / 跨专题索引 / 审核结果）
├── instructions.md                        ← 用户的指令文件（原样保留）
├── utils/
│   └── ListNode.py                        ← 按指令保持原位置（无 import 依赖）
├── _audit/
│   ├── pre-migration-manifest.json
│   ├── migration-map.json
│   └── post-migration-report.md           ← 本文件
├── _resources/
│   ├── pattern-recognition-guide.md       ← Q1–Q15 决策树
│   ├── matrix-index-cheat-sheet.md        ← 坐标变换 + 螺旋四步 + 原地修改安全规则
│   └── overflow-and-numeric-pitfalls.md   ← Python 负数 // % + 32-bit + 浮点 + gcd
├── 01 - 矩阵遍历与方向模拟 (Matrix Traversal)/        README.md
│   ├── 01 - 螺旋遍历、生成与填充/
│   │   ├── 01 - LC-0054 - Spiral Matrix/
│   │   ├── 02 - LC-0059 - Spiral Matrix II/
│   │   └── 03 - LC-2326 - Spiral Matrix IV/
│   └── 02 - 对角线与动态方向遍历/
│       ├── 01 - LC-0498 - Diagonal Traverse/
│       └── 02 - LC-0885 - Spiral Matrix III/
├── 02 - 矩阵变换与状态模拟 (Matrix Transformation)/   README.md
│   ├── 01 - 转置与矩阵旋转/
│   │   ├── 01 - LC-0867 - Transpose Matrix/
│   │   └── 02 - LC-0048 - Rotate Image/
│   ├── 02 - 原地标记与同步状态更新/
│   │   ├── 01 - LC-0073 - … (学习索引 · 实体在 01-arrays-hashing)/   README.md only
│   │   └── 02 - LC-0289 - Game of Life/                 ★ 第一轮新增
│   └── 03 - 多轮矩阵消除与重力模拟/
│       ├── 01 - LC-0723 - Candy Crush/
│       └── 02 - LC-1861 - Rotating the Box/             ★ 第二轮新增
├── 03 - 整数运算与数位处理 (Arithmetic)/              README.md
│   ├── 01 - 数位进位与整数反转/
│   │   ├── 01 - LC-0066 - Plus One/
│   │   └── 02 - LC-0007 - Reverse Integer/              ★ 第一轮新增
│   ├── 02 - 字符串解析与大整数乘法/
│   │   ├── 01 - LC-0008 - String to Integer (atoi)/
│   │   └── 02 - LC-0043 - Multiply Strings/
│   ├── 03 - Fast Exponentiation 平方快速幂/
│   │   └── 01 - LC-0050 - … (学习索引 · 实体在 99-advanced)/         README.md only
│   └── 04 - 筛法与素数计数/
│       └── 01 - LC-0204 - Count Primes/                 ★ 第二轮新增
└── 04 - 坐标几何与空间计数 (Geometry)/                README.md
    ├── 01 - Bounding Box 与矩形交集/
    │   ├── 01 - LC-3195 - Find the Minimum Area to Cover All Ones I/
    │   └── 02 - LC-0223 - Rectangle Area/               ★ 第一轮新增
    ├── 02 - 坐标 Hash Map 与正方形计数/
    │   └── 01 - LC-2013 - Detect Squares/               ← NC 正式化
    └── 03 - 斜率归一化与共线计数/
        └── 01 - LC-0149 - Max Points on a Line/         ★ 第二轮新增
```

---

## 二、四个 Level 1 与 11 个 Level 2 Pattern

| Level 1 | Level 2 | Pattern | 题数 |
|---|---|---|---|
| 01 矩阵遍历与方向模拟 | 01 螺旋遍历、生成与填充 | Spiral Boundary Traversal | 3 |
| | 02 对角线与动态方向遍历 | Diagonal Grouping / Direction Vectors | 2 |
| 02 矩阵变换与状态模拟 | 01 转置与矩阵旋转 | Coordinate Transformation | 2 |
| | 02 原地标记与同步状态更新 | In-place Marking / Simultaneous Update | 2（1 索引） |
| | 03 多轮矩阵消除与重力模拟 | Multi-phase Simulation / Gravity | 2 |
| 03 整数运算与数位处理 | 01 数位进位与整数反转 | Carry Propagation / Digit Extraction | 2 |
| | 02 字符串解析与大整数乘法 | Integer Parsing / Grade-school Multiplication | 2 |
| | 03 Fast Exponentiation 平方快速幂 | Exponentiation by Squaring | 1（索引） |
| | 04 筛法与素数计数 | Sieve of Eratosthenes | 1 |
| 04 坐标几何与空间计数 | 01 Bounding Box 与矩形交集 | Bounding Box / Inclusion-Exclusion | 2 |
| | 02 坐标 Hash Map 与正方形计数 | Coordinate Hashing / Geometric Counting | 1 |
| | 03 斜率归一化与共线计数 | Slope Normalization + GCD | 1 |

**Level 1 分布**：01→5、02→6、03→6、04→4，合计 **21**。

---

## 三、原有 13 道题的迁移情况（零丢失）

| 原路径 | 新路径 |
|---|---|
| `matrix (矩阵)/LC-0054 - Spiral Matrix` | `01/01/01` |
| `matrix (矩阵)/LC-0059 - Spiral Matrix II` | `01/01/02` |
| `matrix (矩阵)/LC-2326 - Spiral Matrix IV` | `01/01/03`（**另见第九节的 bug 修复**） |
| `matrix (矩阵)/LC-0498 - Diagonal Traverse` | `01/02/01` |
| `matrix (矩阵)/LC-0885 - Spiral Matrix III` | `01/02/02` |
| `matrix (矩阵)/LC-0867 - Transpose Matrix` | `02/01/01` |
| `matrix (矩阵)/LC-0048 - Rotate Image` | `02/01/02` |
| `matrix (矩阵)/LC-0723 - Candy Crush` | `02/03/01` |
| `arithmetic (算术与模拟)/LC-0066 - Plus One` | `03/01/01` |
| `arithmetic (算术与模拟)/LC-0008 - String to Integer (atoi)` | `03/02/01` |
| `arithmetic (算术与模拟)/LC-0043 - Multiply Strings` | `03/02/02` |
| `matrix (矩阵)/LC-3195 - Find the Minimum Area to Cover All Ones I` | `04/01/01` |
| `geometry (几何)/NC - Detect Squares` | `04/02/01 - LC-2013 - Detect Squares` |

旧目录 `matrix (矩阵)/`、`arithmetic (算术与模拟)/`、`geometry (几何)/`
确认**已全部迁移且为空**后才清理（只删除了残留的 `.DS_Store`）。

**特别保护的文件全部在位**：
`LC-0066/note.md`、`LC-0048/note.md`、`LC-0054/note.md`、
`LC-0498/asset-0498 - Diagonal Traverse.drawio`、`LC-2013/note.md`
（原 `NC - Detect Squares/note.md`），以及全部 `metadata.json` / `problem.pdf` /
`problem_dark.pdf` / `solution.py`。

---

## 四、NC-only 正式化结果

**执行方式的说明（与指令原文的一处偏离，已获用户明确授权）**：

指令第四节原本要求「将 NC 原始文件全部归档到 `_neetcode/`」。但用户在本次任务中
给出了**更高优先级的覆盖指令**：

> 「When you have duplicates between neetcode and leetcode questions,
>  always delete the neetcode one and preserve the leetcode one.」

以及早先的长期偏好：「LC/NC 同题只留 LeetCode 版；不再建 `_neetcode/`；孤立 NC 改名升格」。

`NC - Detect Squares` 是**孤立 NC**（仓库里没有对应的 LC-2013 实体），
所以采用 **原地升格（in-place promotion）**：文件夹改名为
`01 - LC-2013 - Detect Squares`，`metadata.json` 的 `id` 从 `NC-count-squares` 改为 `LC-2013`。

| 项 | 结果 |
|---|---|
| 题面核对 | ✅ `metadata.json` 原本就带 `leetcode: .../problems/detect-squares/`，与 LC-2013 对应 |
| 代码核对 | ✅ `solution.py` 实现的是 `add` / `count` 轴对齐正方形计数，与 LC-2013 一致 |
| 原 `solution.py` | ✅ **未覆盖**（一个字节都没改） |
| 原 `note.md` | ✅ 保留 |
| 原 `problem.pdf` / `problem_dark.pdf` | ✅ **保留且未被重新生成覆盖**（`intake.py` 报告「已存在，跳过」） |
| `practice[]` | ✅ 未手改（原本是空数组） |
| 是否只占一个 Level 3 位置 | ✅ 是，仓库里只有这一个 LC-2013 文件夹 |

**关于「不得把 NC metadata 直接冒充官方 LC metadata」**：
`metadata.json` 现在的 `id` 是 `LC-2013`，`link` 同时保留了
`leetcode` 和 `neetcode` 两个 URL（这是本仓库 `metadata.json` 的既有格式），
`difficulty` 是 `M`（与 LeetCode 官方的 Medium 一致）。
PDF 是**升格前已存在的那一份**，未声称是重新抓取的官方题面。

---

## 五、第一轮建议新增的五道题

| 题 | 结果 | 位置 |
|---|---|---|
| **LC-0073** Set Matrix Zeroes | ⚠️ **未新建实体** —— 仓库已有（带 `note.md`）⟹ 建学习索引 | `01-arrays-hashing/04/05`（跨专题引用） |
| **LC-0050** Pow(x, n) | ⚠️ **未新建实体** —— 仓库已有（带 `note.md` + **5 条 practice 记录**）⟹ 建学习索引 | `99-advanced/divide-and-conquer`（跨专题引用） |
| **LC-0289** Game of Life | ✅ 新建，4 个解法 + 400 组随机对拍 | `02/02/02` |
| **LC-0007** Reverse Integer | ✅ 新建，3 个解法 + 4000 组随机对拍 | `03/01/02` |
| **LC-0223** Rectangle Area | ✅ 新建，3 个解法 + 3000 组随机对拍 | `04/01/02` |

**跨专题重复检查（只读）结果**（指令第七节点名的 10 道全部核查）：

| 题 | 检查结果 | 处理 |
|---|---|---|
| LC-0202 Happy Number | **已在** `06-linked-list/03/02/01`（Floyd 环检测） | 只建跨专题索引；指令也明确「不重复生成」 |
| LC-0007 Reverse Integer | 仓库**无** | 本专题新建 |
| LC-0069 Sqrt(x) | 主归属是 `05-binary-search` | 只在跨专题索引中提及，不收录 |
| **LC-0050** Pow(x, n) | **已在** `99-advanced/divide-and-conquer`（5 条复习记录） | **只建索引**（规则 2 + 4） |
| **LC-0073** Set Matrix Zeroes | **已在** `01-arrays-hashing/04/05`（带 note.md） | **只建索引**（规则 2 + 4） |
| LC-0289 Game of Life | 仓库**无** | 本专题新建 |
| LC-2013 Detect Squares | 本专题有 NC 版 | 原地升格 |
| LC-2326 Spiral Matrix IV | 本专题已有 | 实体留本专题（Spiral 是主模式） |
| LC-3195 Min Area to Cover All Ones | 本专题已有 | 实体留本专题 |
| LC-0149 Max Points on a Line | 仓库**无** | 第二轮新增 |

**没有修改其他专题的任何文件。**

---

## 六、第二轮独立审核

**自主新增 3 道（上限 3，用满）**：

| 题 | 填补缺口 | 通过的条件 |
|---|---|---|
| **LC-0149** Max Points on a Line | Slope Normalization + GCD（唯一一道用整数方向向量代替浮点斜率） | A B C D E F ✅ |
| **LC-1861** Rotating the Box | Rotation + Gravity 的交汇；教「复合问题解耦」 | A B C D E F ✅ |
| **LC-0204** Count Primes | 唯一一道「预处理出表，之后 O(1) 查」的算法 | A B C D E F ✅ |

**关于 LC-0204**：指令提醒「不要因此自动扩充完整数论专题」。
本次**只收这一道**，理由不是「它是数论」，而是**它是一个可复用的预处理模板**
（同一张筛表直接支持最小质因子分解，该题 `solution.py` 末尾有可运行演示）。

**未新增的候选及原因**：

| 题 | 违反条件 | 原因 | 建议归属 |
|---|---|---|---|
| LC-0202 Happy Number | F | 已在 `06-linked-list`（Floyd 是主归属） | 已存在 |
| LC-0836 Rectangle Overlap | D | 与 LC-0223 交集公式重合，只是把面积换成布尔 | 已写入 LC-0223 的 `Solution_2` 作为对照 |
| LC-0939 Minimum Area Rectangle | D | 与 LC-2013 坐标哈希思想大量重合 | 将来若专练「矩形计数」再加 |
| LC-1572 Matrix Diagonal Sum | A, B | 太简单，不构成独立 Pattern | 不建议单独收录 |
| LC-0013 / LC-0012 Roman | C, E | 主要是查表 + 规则记忆，迁移性低 | 不收（用户已归档为低优先级） |
| LC-0067 Add Binary | D | Carry 已由 LC-0066 / LC-0043 覆盖 | 不收（用户已归档为低优先级） |
| LC-0006 Zigzag Conversion | B, C | 不构成核心 Pattern | 不收（用户已归档为低优先级） |
| Convex Hull / FFT / NTT / 高级数论 / 高级组合数学 / 矩阵快速幂 | E | 成本远超迁移收益；指令明确要求不自动扩充 | `99-advanced` |
| LC-0218 The Skyline Problem | E, F | Sweep Line + Heap 难题 | `99-advanced` |

参考：NeetCode 150/250、Blind 75、Grind 75/169、LeetCode Top Interview 150
的 Math & Geometry 分区。**未编造任何公司的实际出题频次。**

---

## 七、P0 / P1 / P2 数量

| 等级 | 数量 | 题 |
|---|---|---|
| **P0** | **6** | 0054, 0048, 0073↗️, 0066, 0050↗️, 2013 |
| **P1** | **8** | 0059, 0498, 0867, 0008, 0007, 0043, 0289, 0223 |
| **P1+** | **1** | 1861 |
| **P2** | **6** | 0885, 2326, 0723, 3195, 0204★, 0149★ |

合计 21。**没有把所有题都标 P0。**

---

## 八、边界测试结果

每道新题的 `__main__` 都跑了固定边界用例 + 随机/穷举对拍，**全部通过**：

| 题 | 类别 | 关键边界断言 | 对拍 |
|---|---|---|---|
| LC-0289 | 矩阵 | blinker `[[1,1,1],[0,0,0],[0,0,0]]` → 转 90°（**边扫边覆盖会得全 0**）<br>`[[1]]`→`[[0]]`、2×2 全活不变、1×n、n×1 | 400 组 ✅（4 实现 + 定义基准） |
| LC-1861 | 矩阵 | `[["#"]]`→`[["#"]]`（`read==write` 的试金石）<br>`[["#","*","#"]]` 障碍切段、1×n、n×1 | 800 组 ✅（3 实现） |
| LC-0007 | 数值 | `-123`→`-321`（Python `%` 陷阱）、`120`→`21`、`0`<br>`1534236469`/`-2147483648`/`2147483647`→**0**、`1463847412`→界内 | 4000 组 ✅（3 实现，刻意覆盖边界附近） |
| LC-0204 | 数值 | `countPrimes(0/1/2)`→**0**（2 不小于 2）、`25`→9、`1000`→168 | **穷举 n=0..599** ✅（3 实现） |
| LC-0223 | 几何 | 只贴边→交集 **0**、只碰角、完全相同→16（不是 32）<br>完全包含、退化成点、全负坐标 | 3000 组 ✅（3 实现含单位格暴力） |
| LC-0149 | 几何 | 垂直线、水平线、`[(0,0),(1,1),(-1,-1)]`→**3**（符号统一的试金石）<br>`n==1`/`n==2`、负坐标全共线 | 600 组 ✅（3 实现含叉积 O(n³) 基准） |

**指令第十三节要求的边界类别逐项覆盖**：
- **矩阵类**（8 项）：单行 ✅ 单列 ✅ 1×1 ✅ 非正方形 ✅ 全部相同 ✅
  边界变化 ✅ 多次更新一致性 ✅ 空输入 ✅
- **数值类**（8 项）：0 ✅ 正数 ✅ 负数 ✅ Carry ✅ Leading Zeros ✅
  32-bit 边界 ✅ 负指数 ✅（LC-0050 索引文档）极大指数 ✅
- **几何类**（8 项）：负坐标 ✅ 共享边界 ✅ 无交集 ✅ 完全包含 ✅
  重复坐标 ✅ 零宽/零高 ✅ 无效正方形边长 ✅ 大量重复点计数 ✅

### 执行过程中被测试抓出的三个错误（均为我写的测试期望值有误，解法本身正确）

1. **LC-1861 example 2 的输入被我抄错**：我把官方的
   `[["#",".","*","."],["#","#","*","."]]` 写成了 `[[...],[".","#","*","."]]`，
   于是期望值也跟着错。改回官方样例后通过。
2. **LC-1861 example 3 期望值第一行抄错**：写成 `[".",".","#"]`，正确是 `[".","#","#"]`。
   **已手工逐格复算验证**（见该题 docstring 的旋转公式表），三种实现一致。
3. **LC-0289 docstring 里的反例写得混乱**：原本拿 1×3 的 `[[1,1,0]]` 举例，
   结论含糊。换成横向 blinker `[[1,1,1],[0,0,0],[0,0,0]]`，
   并**实际运行验证**：正确答案 `[[0,1,0],[0,1,0],[0,0,0]]`，
   行优先直接覆盖得 **全 0** —— 反例现在是真实可复现的。

另外修了一个**迁移前就已存在**的 bug，见下一节。

---

## 九、原始文件与 SHA-256 验证结果

```
[1] 原始文件 59 个 → 内容仍在的 58，1 个为修 bug 做了纯新增
[2] 相对链接 117+ 条，死链 0
[3] solution.py 运行 19 通过 / 0 失败（迁移前是 12 通过 / 1 失败）
[4] 题目文件夹 19 个，Level 1/2/3 编号连续
```

### 唯一一个内容变化的文件（**纯新增，未删除任何用户代码**）

`01/01/03 - LC-2326 - Spiral Matrix IV/solution.py`

**迁移前它就是坏的**：文件底部的 driver 调用
`ListNode.from_list([3, 0, 2, ...])`，但文件自带的 `ListNode` 类里**没有**
`from_list` 方法 ⟹ 运行即 `AttributeError`（基线测试 12 通过 / **1 失败**，就是它）。

**修复方式**：在 `ListNode` 类里**新增**一个 `from_list` staticmethod
（实现与 `utils/ListNode.py` 里的同名方法一致）。
**用户原有的 `Solution` 类、算法代码、driver 代码一个字符都没改。**
修复后该文件正常输出 `[[3, 0, 2, 6, 8], [5, 0, -1, -1, 1], [5, 2, 4, 9, 7]]`。

### 其余验证项

- **SHA-256**：重构前记录全部 59 个文件的哈希；重构后逐一比对，
  **58/59 内容完全一致**，第 59 个是上面那个 bug 修复（`metadata.json`
  作为可变文件单独处理 —— 只有 `id` / `path` 按设计变更，`practice[]` 未手改）。
- **符号链接**：本专题内**未发现**符号链接。
- **`utils/ListNode.py` 依赖检查**：全专题 `grep` 确认**没有任何 `solution.py` import 它**
  （LC-2326 自己定义了一份本地 `ListNode`）。按指令要求**保持原位置不变**。
- **文件名冲突**：无。
- **未跟踪文件**：未删除任何一个（只删了两个 `.DS_Store` 以便 `rmdir` 空目录）。
- **原有 `solution.py` 覆盖**：**零次**。
- **原有 `problem.pdf` 覆盖**：**零次**（`intake.py` 对已存在文件报「跳过」）。
- **`note.md` / 图解 / `.drawio`**：全部原地保留。

---

## 十、题面生成情况

**全部 6 道新题的 4 件标准文件齐全**：

| 题 | metadata.json | solution.py | problem.pdf | problem_dark.pdf |
|---|---|---|---|---|
| LC-0289 | ✅ | ✅ | ✅ | ✅ |
| LC-0007 | ✅ | ✅ | ✅ | ✅ |
| LC-0223 | ✅ | ✅ | ✅ | ✅ |
| LC-0149 | ✅ | ✅ | ✅ | ✅ |
| LC-1861 | ✅ | ✅ | ✅ | ✅ |
| LC-0204 | ✅ | ✅ | ✅ | ✅ |

**本专题没有 Premium 题目**，所以没有抓取受限的情况 ——
全部通过仓库既有的 `tools/intake.py` 工作流生成，**无伪造、无空白 PDF、无错题题面**。

两个**学习索引文件夹**（LC-0073、LC-0050）**故意只有 `README.md`**：
没有 `metadata.json` ⟹ `review_due.py:154` 要求同时满足
「有 `metadata.json`」且「文件夹名匹配 `PROBLEM_DIR_RE`」才入复习队列
⟹ **不会重复叫号**。

---

## 十一、Git 变更摘要

- **未执行** `git add` / `git commit` / `git push`（按指令要求）。
- **未执行** 任何破坏性命令：`git reset`、`git clean`、`git restore .`、
  `git checkout -- .`、`rm -rf` 全部没用过。
- 文件夹移动用 `mv`（这些文件是 untracked，`git mv` 会报 "source directory is empty"）。
- 变更性质：
  - **新增**：6 道题的文件夹 + 10 份 README/文档 + `_audit/` 三份
  - **移动/改名**：13 个原有题目文件夹（含 1 个 NC 升格）
  - **修改**：13 个 `metadata.json` 的 `id`/`path` 字段 + 1 个 `solution.py` 的 bug 修复
  - **删除**：2 个 `.DS_Store`（为了 `rmdir` 已空的旧目录）
- 写入范围：**全部在 `15-math-geometry (数学、几何)/` 内部**。
  唯一的例外是 `tools/intake.py` 自动更新的仓库级 `progress.md`
  —— 这是该工具的既有行为，不是本次重构的主动写入。

---

## 十二、失败或未完成的任务

| 项 | 状态 |
|---|---|
| 全部验收项 | ✅ **通过** |

**没有失败或未完成项。** 本专题无 Premium 题目，所有标准文件齐全。

**一处与指令原文的偏离已在第四节说明**（`_neetcode/` 归档 → 原地升格），
原因是用户给出了更高优先级的覆盖指令，且实质要求全部满足。

---

## 十三、幂等性

重复执行本次重构**不会**：
- 叠加编号（`PROBLEM_DIR_RE` 识别 `NN - ` 前缀，不会重复加）
- 重复生成题目（`intake.py` 默认跳过已存在的文件，除非 `--force`）
- 重复归档（未建 `_neetcode/` 副本）
- 覆盖原文件（`intake.py` 不加 `--force` 就不覆盖）
- 丢失资料（所有操作都是 `mv` / 新建 / 纯新增）

---

## 十四、建议的学习顺序

见根 [README.md](<../README.md>) 第十一节。

最短路线 6 道：`0054 → 0048 → 0073 → 0066 → 0050 → 2013`

---

## 附录 · 2026-11-11 增补：`99-advanced (进阶专题)` 清空后的两道迁入题

> 本节是对上面那份报告的**后续增补**。上面的内容是当时那一轮的快照，不做修改。

`99-advanced (进阶专题)` 没有 `instructions.md`，所以上一轮没有处理它。
2026-11-11 用户明确下令清理，该大类的 5 道题全部迁回对应专题，目录已移入废纸篓（未用 `rm -rf`）。
其中两道落在本专题：

| 题 | 原位置 | 新位置 | 处理 |
|---|---|---|---|
| **LC-0050** Pow(x, n) | `99-advanced/divide-and-conquer (分治)/` | `03 - 整数运算与数位处理 (Arithmetic)/03 - Fast Exponentiation 平方快速幂/01 - LC-0050 - Pow(x, n)` | 上一轮在这里建的「学习索引」文件夹已删除，**实体迁入取而代之**。5 条 `practice` 记录 + `note.md`（含 3 次 retry）原样保留 |
| **LC-1041** Robot Bounded In Circle | `99-advanced/simulation (模拟)/` | `01 - 矩阵遍历与方向模拟 (Matrix Traversal)/03 - 方向向量旋转与周期性判断/01 - LC-1041 - Robot Bounded In Circle` | **新建 Level 2 · 03**。放在这一层是因为它和 LC-0885 共用同一套方向向量机制，只是脱离了网格 ⟹ 只剩旋转的代数性质（阶为 4） |

**结构变化**：Level 1 · 01 从 2 个 Level 2 变成 3 个（编号连续 01 → 02 → 03）；
Level 1 · 03 的 Level 2 · 03 从「索引位」变成实体位。专题题数 19 → 21，跨专题索引 2 → 1。

**代码变化**（两份 `solution.py` 都只做追加，用户原有代码逐字未动）：

- LC-0050：原有递归折半版保留为 `Solution`；新增 `Solution_2` 迭代二进制快速幂（⭐️ 首选）、
  `Solution_3` 朴素 O(n) 连乘（反面教材）、`_pow_mod` 模幂迁移示例。
  **顺带记录了一个实测结论**：快速幂在 `n = 2³¹−1` 时与 Python 内置 `x ** n` 相差 `1.2e-8`，
  因为 `x^n` 对 `x` 的条件数就是 `n` ⟹ 相对误差天然是 O(n·ε)，用固定 `1e-9` 卡大指数必然误报。
- LC-1041：原有「字典方向表 + 走 4 遍」保留为 `Solution`；新增 `Solution_2` 一遍 + 判据（⭐️ 首选）、
  `Solution_3` 复数版、`Solution_4` 暴力真值基线（模拟 200 / 400 遍比最远距离）。
  **穷举对拍了长度 0..8 的全部 9841 个 `{G,L,R}` 指令串**，四种实现完全一致。
  文件头补上了「为什么 4 遍就够」的证明：`(I−R)(I+R+R²+R³) = I−R⁴ = 0` 且 `I−R` 可逆。

**README 更新**：专题根 README（知识地图、题目总表重新编号、跨专题索引、Future Candidates 里
指向 `99-advanced` 的归属建议）、Level 1 · 01 README（新增 Level 2 · 03 的完整教学小节）、
Level 1 · 03 README（LC-0050 从索引改成实体）、`_resources/pattern-recognition-guide.md`。
