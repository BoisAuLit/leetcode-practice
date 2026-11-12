# 15 - Math & Geometry（数学、几何）

> **一句话**：这个专题不是「数学题集」，而是四件可迁移的手艺 ——
> **安全处理矩阵边界**、**正确定义遍历方向**、**原地修改不污染旧状态**、
> **把几何问题转成整数比较或 Hash 计数**。
> **全程避开浮点，刻意不扩充竞赛数学。**

**24 道题 · 4 个 Level 1 · 11 个核心模板**

---

## 一、完整知识地图

```
Level 1 · 01  矩阵遍历与方向模拟 (Matrix Traversal)      ← 只读：按顺序走遍矩阵
                ├─ 01 螺旋遍历、生成与填充       LC-0054  LC-0059  LC-2326
                ├─ 02 对角线与动态方向遍历       LC-0498  LC-0885
                └─ 03 方向向量旋转与周期性判断   LC-1041

Level 1 · 02  矩阵变换与状态模拟 (Matrix Transformation) ← 开始写：顺序成为正确性问题
                ├─ 01 转置与矩阵旋转             LC-0867  LC-0048
                ├─ 02 原地标记与同步状态更新     LC-0073↗ LC-0289
                └─ 03 多轮矩阵消除与重力模拟     LC-0723  LC-1861★

Level 1 · 03  整数运算与数位处理 (Arithmetic)            ← 单个整数按位拆开
                ├─ 01 数位进位与整数反转         LC-0066  LC-0007
                ├─ 02 字符串解析与大整数乘法     LC-0008  LC-0043
                ├─ 03 Fast Exponentiation 平方快速幂  LC-0050
                └─ 04 筛法与素数计数             LC-0204★

Level 1 · 04  坐标几何与空间计数 (Geometry)              ← 几何 → 整数比较 / Hash 计数
                ├─ 01 Bounding Box 与矩形交集    LC-3195  LC-0223
                ├─ 02 坐标 Hash Map 与正方形计数 LC-2013
                └─ 03 斜率归一化与共线计数       LC-0149★
```

↗️ = 实体在其他专题，本专题只放学习索引 · ★ = 第二轮独立审核新增

---

## 二、四个 Level 1 的学习目标

| Level 1 | 目标 | 难点 | 核心认识 |
|---|---|---|---|
| [**01** 矩阵遍历与方向模拟](<./01 - 矩阵遍历与方向模拟 (Matrix Traversal)>) | 按非行优先顺序走遍矩阵，每格恰好一次；再把方向向量**脱离网格**单独用 | **边界什么时候收缩**；旋转的**阶**是多少 | 螺旋的本质是「矩形在收缩」，不需要 `visited`；90° 旋转的阶是 4 ⟹ `I+R+R²+R³ = 0`（LC-1041） |
| [**02** 矩阵变换与状态模拟](<./02 - 矩阵变换与状态模拟 (Matrix Transformation)>) | 改变矩阵的布局或内容 | **什么时候能安全覆盖** | 新状态依赖旧状态 ⟹ **必须两阶段** |
| [**03** 整数运算与数位处理](<./03 - 整数运算与数位处理 (Arithmetic)>) | 把整数按位拆开处理 | **符号、进位、溢出** | Python 不会溢出，所以范围限制要**手写判断** |
| [**04** 坐标几何与空间计数](<./04 - 坐标几何与空间计数 (Geometry)>) | 几何 → 坐标比较 / Hash 计数 | **`+1` 与否、不用浮点** | 轴对齐让二维退化成两个一维问题 |

**依赖顺序**：01（会走）→ 02（会写）；03 和 04 相对独立，但都共享「避开浮点」的主题。

---

## 三、全部题目（含真实相对路径）

| # | 题 | 优先级 | Pattern | 路径 |
|---|---|---|---|---|
| 1 | LC-0054 Spiral Matrix | **P0** | Spiral Boundary（读） | [→](<./01 - 矩阵遍历与方向模拟 (Matrix Traversal)/01 - 螺旋遍历、生成与填充/01 - LC-0054 - Spiral Matrix>) |
| 2 | LC-0059 Spiral Matrix II | P1 | Spiral Boundary（写） | [→](<./01 - 矩阵遍历与方向模拟 (Matrix Traversal)/01 - 螺旋遍历、生成与填充/02 - LC-0059 - Spiral Matrix II>) |
| 3 | LC-2326 Spiral Matrix IV | P2 | Spiral Boundary（链表→写） | [→](<./01 - 矩阵遍历与方向模拟 (Matrix Traversal)/01 - 螺旋遍历、生成与填充/03 - LC-2326 - Spiral Matrix IV>) |
| 4 | LC-0498 Diagonal Traverse | P1 | `r+c` 分组 + 交替方向 | [→](<./01 - 矩阵遍历与方向模拟 (Matrix Traversal)/02 - 对角线与动态方向遍历/01 - LC-0498 - Diagonal Traverse>) |
| 5 | LC-0885 Spiral Matrix III | P2 | 方向向量 + 递增步长 | [→](<./01 - 矩阵遍历与方向模拟 (Matrix Traversal)/02 - 对角线与动态方向遍历/02 - LC-0885 - Spiral Matrix III>) |
| 6 | LC-1041 Robot Bounded In Circle ✚ | P1 | 旋转的阶 = 4（一遍 + 判据） | [→](<./01 - 矩阵遍历与方向模拟 (Matrix Traversal)/03 - 方向向量旋转与周期性判断/01 - LC-1041 - Robot Bounded In Circle>) |
| 7 | LC-0867 Transpose Matrix | P1 | Coordinate Transformation | [→](<./02 - 矩阵变换与状态模拟 (Matrix Transformation)/01 - 转置与矩阵旋转/01 - LC-0867 - Transpose Matrix>) |
| 8 | LC-0048 Rotate Image | **P0** | 转置 + 翻转（**原地**） | [→](<./02 - 矩阵变换与状态模拟 (Matrix Transformation)/01 - 转置与矩阵旋转/02 - LC-0048 - Rotate Image>) |
| 9 | LC-0073 Set Matrix Zeroes ↗️ | **P0** | In-place Marking | [→](<./02 - 矩阵变换与状态模拟 (Matrix Transformation)/02 - 原地标记与同步状态更新/01 - LC-0073 - Set Matrix Zeroes (学习索引 · 实体在 01-arrays-hashing)>) |
| 10 | LC-0289 Game of Life | P1 | Simultaneous State Update | [→](<./02 - 矩阵变换与状态模拟 (Matrix Transformation)/02 - 原地标记与同步状态更新/02 - LC-0289 - Game of Life>) |
| 11 | LC-0723 Candy Crush | P2 | Multi-phase Simulation | [→](<./02 - 矩阵变换与状态模拟 (Matrix Transformation)/03 - 多轮矩阵消除与重力模拟/01 - LC-0723 - Candy Crush>) |
| 12 | LC-1861 Rotating the Box ★ | P1+ | Gravity + Rotation（解耦） | [→](<./02 - 矩阵变换与状态模拟 (Matrix Transformation)/03 - 多轮矩阵消除与重力模拟/02 - LC-1861 - Rotating the Box>) |
| 13 | LC-0066 Plus One | **P0** | Carry Propagation | [→](<./03 - 整数运算与数位处理 (Arithmetic)/01 - 数位进位与整数反转/01 - LC-0066 - Plus One>) |
| 14 | LC-0007 Reverse Integer | P1 | Digit Extraction + 溢出 | [→](<./03 - 整数运算与数位处理 (Arithmetic)/01 - 数位进位与整数反转/02 - LC-0007 - Reverse Integer>) |
| 15 | LC-0008 String to Integer (atoi) | P1 | Integer Parsing + Bounds | [→](<./03 - 整数运算与数位处理 (Arithmetic)/02 - 字符串解析与大整数乘法/01 - LC-0008 - String to Integer (atoi)>) |
| 16 | LC-0043 Multiply Strings | P1 | Grade-school Multiplication | [→](<./03 - 整数运算与数位处理 (Arithmetic)/02 - 字符串解析与大整数乘法/02 - LC-0043 - Multiply Strings>) |
| 17 | LC-0050 Pow(x, n) ✚ | **P0** | Fast Exponentiation | [→](<./03 - 整数运算与数位处理 (Arithmetic)/03 - Fast Exponentiation 平方快速幂/01 - LC-0050 - Pow(x, n)>) |
| 18 | LC-0204 Count Primes ★ | P2 | Sieve of Eratosthenes | [→](<./03 - 整数运算与数位处理 (Arithmetic)/04 - 筛法与素数计数/01 - LC-0204 - Count Primes>) |
| 19 | LC-3195 Min Area to Cover All Ones | P2 | Bounding Box（**+1**） | [→](<./04 - 坐标几何与空间计数 (Geometry)/01 - Bounding Box 与矩形交集/01 - LC-3195 - Find the Minimum Area to Cover All Ones I>) |
| 20 | LC-0223 Rectangle Area | P1 | Inclusion-Exclusion（**无 +1**） | [→](<./04 - 坐标几何与空间计数 (Geometry)/01 - Bounding Box 与矩形交集/02 - LC-0223 - Rectangle Area>) |
| 21 | LC-2013 Detect Squares | **P0** | Coordinate Hash Counting | [→](<./04 - 坐标几何与空间计数 (Geometry)/02 - 坐标 Hash Map 与正方形计数/01 - LC-2013 - Detect Squares>) |
| 22 | LC-0149 Max Points on a Line ★ | P2 | Slope Normalization + GCD | [→](<./04 - 坐标几何与空间计数 (Geometry)/03 - 斜率归一化与共线计数/01 - LC-0149 - Max Points on a Line>) |

**实体文件夹 21 个 + 跨专题学习索引 1 个 = 22 个条目，涉及 22 道不同题目。**

✚ = 2026-11-11 从已清空的 `99-advanced (进阶专题)` 迁入（LC-0050 原先只在本专题放学习索引，现已是实体）

---

## 四、P0 / P1 / P2

| 等级 | 数量 | 题 |
|---|---|---|
| **P0**（核心模板，必须熟练） | **6** | 0054, 0048, 0073↗️, 0066, 0050↗️, 2013 |
| **P1**（标准面试覆盖面） | **8** | 0059, 0498, 0867, 0008, 0007, 0043, 0289, 0223 |
| **P1+**（第二轮新增，高迁移） | **1** | 1861 |
| **P2**（存档与补充） | **6** | 0885, 2326, 0723, 3195, 0204★, 0149★ |

> P0/P1/P2 是**教学优先级**（学习依赖 + 模板覆盖面），
> **不代表任何公司的实际出题频次** —— 本仓库不编造频次数据。

---

## 五、十个核心模板

> 这**不是**十套要分别背的算法。真正独立的骨架只有四块：
> **①边界收缩 ②坐标映射 ③两阶段更新 ④逐位处理**。其余都是换循环体。

### Template 1 — Matrix Spiral Boundary Traversal

```python
top, bottom, left, right = 0, m - 1, 0, n - 1
while top <= bottom and left <= right:
    for c in range(left, right + 1):  ...(top, c)            # ① 上边
    top += 1
    for r in range(top, bottom + 1):  ...(r, right)          # ② 右边
    right -= 1
    if top <= bottom:                                        # ! ⚠️ 单行时必须拦住
        for c in range(right, left - 1, -1): ...(bottom, c)  # ③ 下边
        bottom -= 1
    if left <= right:                                        # ! ⚠️ 单列时必须拦住
        for r in range(bottom, top - 1, -1): ...(r, left)    # ④ 左边
        left += 1
```
**O(m·n)** / O(1)。📍 LC-0054（读）、LC-0059（写）、LC-2326（从链表写）——
**骨架一字不改，只换循环体那一行。**

### Template 2 — Matrix Transpose + Reverse

```python
for r in range(n):
    for c in range(r + 1, n):            # ! 只走上三角，否则每对换两次
        matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]
for row in matrix: row.reverse()         # ! 顺时针；逆时针改成 matrix.reverse()
```
**O(n²)** / **O(1)**。📍 LC-0048（**仅正方形**）、LC-0867（矩形必须新建）

### Template 3 — In-place Matrix Marking

```python
first_col_zero = any(matrix[i][0] == 0 for i in range(m))   # ! matrix[0][0] 存不下两个 bit
# ① 只写标记  ② 回填内部 i,j >= 1  ③ 最后才清第 0 行  ④ 和第 0 列
```
**O(m·n)** / **O(1)**。📍 LC-0073 —— **顺序是全部难点**。

### Template 4 — Simultaneous State Update

```
Read Original State  →  Record Updates  →  Apply Updates
```
```python
board[r][c] |= 2        # ! 第 1 位存新状态，不碰第 0 位
...
board[r][c] >>= 1       # ! 第二遍统一兑现
```
**O(m·n)** / **O(1)**。📍 LC-0289、LC-0073

### Template 5 — Digit Processing + Carry

```python
for i in range(len(digits) - 1, -1, -1):
    if digits[i] < 9: digits[i] += 1; return digits
    digits[i] = 0
return [1] + digits                      # ! 全 9 ⟹ 新增最高位
```
**O(n)** / O(1)。📍 LC-0066、LC-0043

### Template 6 — Integer Parsing + Bounds

```python
sign = -1 if x < 0 else 1
x = abs(x)                               # ! 剥符号，避开 Python 负数的 // % 语义
...
return 0 if res < -2**31 or res > 2**31 - 1 else res        # ! LC-0007：返回 0
return max(-2**31, min(res, 2**31 - 1))                     # ! LC-0008：夹边界
```
📍 LC-0007、LC-0008 —— **两题的溢出处理不一样，别混。**

### Template 7 — Grade-school String Multiplication

```python
res = [0] * (m + n)                      # ! 最多 m+n 位
total = int(num1[i]) * int(num2[j]) + res[i + j + 1]
res[i + j + 1] = total % 10
res[i + j] += total // 10                # ! 落点 i+j+1，进位溢到 i+j
```
**O(m·n)** / O(m+n)。📍 LC-0043

### Template 8 — Exponentiation by Squaring

```python
if n < 0: x, n = 1 / x, -n               # ! 负指数取倒数
result, base = 1.0, x
while n:
    if n & 1: result *= base             # ! 这一位是 1 ⟹ 选进乘积
    base *= base                          # ! 依次 x^1, x^2, x^4, x^8…
    n >>= 1
```
**O(log |n|)** / O(1)。📍 LC-0050
> 把 `*` 换成取模乘 → **Modular Exponentiation**；
> 换成矩阵乘 → **Matrix Exponentiation**；换成「跳 2^k 步」→ **Binary Lifting**。
> 只要运算满足**结合律**，骨架不变。本次不展开这些进阶算法。

### Template 9 — Rectangle Intersection + 容斥

```python
w = max(0, min(ax2, bx2) - max(ax1, bx1))     # ! max(0,..) 夹住负宽
h = max(0, min(ay2, by2) - max(ay1, by1))
return area_a + area_b - w * h
```
**O(1)** / O(1)。📍 LC-0223

### Template 10 — Coordinate Hash Map Counting

```python
counts = Counter()                            # ! 必须是频率表，不能是 set
for (px, py), k in counts.items():            # ! 枚举对角顶点
    if abs(px-qx) != abs(py-qy) or px == qx:  continue
    total += k * counts[(qx, py)] * counts[(px, qy)]     # ! 乘法原理
```
`add` **O(1)** / `count` **O(P)**。📍 LC-2013

**附加（第二轮新增带来的）**：`gcd` 方向归一化（LC-0149）、埃氏筛（LC-0204）。

---

## 六、哪些题共享模板，哪些题必须换思路

### 共享同一骨架，只换循环体

| 组 | 题 | 唯一差别 |
|---|---|---|
| **Spiral Boundary** | LC-0054 / 0059 / 2326 | 读 / 写 / 从链表写 |
| **Coordinate Transformation** | LC-0867 / 0048 | 矩形（新建） / 正方形（原地） |
| **Original vs Update State 分离** | LC-0073 / 0289 / 0723 | 标记存哪、更新机制不同 |
| **Digit Processing** | LC-0066 / 0007 / 0008 / 0043 | 输出目标不同（数组/整数/整数/字符串） |
| **矩形坐标分析** | LC-3195 / 0223 | **离散格子计数**（`+1`） vs **连续平面面积**（无 `+1`） |
| **旋转 + 模拟** | LC-0048 / 0723 / 1861 | 1861 = 旋转 + 重力，**解耦成两步** |

### 必须换思路（不能互相代入）

- **LC-0054 vs LC-0885**：起点在矩阵内 ⟹ 四边界法；
  起点可在矩阵**外** ⟹ 必须换方向向量 + 递增步长。
- **LC-0073 vs LC-0289**：标记**挤占数据位** ⟹ 顺序敏感；
  标记住**不同 bit** ⟹ 顺序无关。
- **LC-3195 vs LC-0223**：数格子 vs 量长度，**差一个 `+1`**。
- **LC-0149 的叉积 vs 方向哈希**：叉积用于 O(1) **判** 3 点；
  方向哈希用于 O(n²) **求**最大共线集合。不要互换。

### 复杂度不能一律写 O(m·n) / O(n log n)

| 题 | 真实复杂度 | 常见错写 |
|---|---|---|
| LC-0885 | **O((rows+cols)²)** | ❌ O(rows·cols)（忽略界外空转） |
| LC-0723 | **O((m·n)²)** | ❌ O(m·n)（忽略多轮） |
| LC-0050 | **O(log \|n\|)** | ❌ O(n) |
| LC-0204 | **O(n log log n)** | ❌ O(n√n)（那是试除法） |
| LC-0149 | **O(n² log V)** | ❌ O(n²)（忽略 gcd） |
| LC-2013 | `add` O(1) / `count` **O(P)** | ❌ 统称 O(n) |
| LC-0007 | **O(log₁₀ x)** ≈ O(1) | ❌ O(n) |

---

## 七、三张速查表

### ① `+1` 还是不 `+1`

| 在算什么 | 公式 | `[1,1]` 代表 |
|---|---|---|
| **离散格子个数** | `max - min + 1` | **1 个格子** |
| **连续长度 / 面积** | `max - min` | **一个点**（面积 0） |

📍 LC-3195 **有** `+1`；LC-0223 **无** `+1`。

### ② Python 的 `//` `%` 对负数

| 表达式 | Python | C / C++ / Java |
|---|---|---|
| `-123 // 10` | **`-13`**（向 -∞） | `-12`（向 0） |
| `-123 % 10` | **`7`**（符号跟除数） | `-3`（符号跟被除数） |

⟹ **先剥符号，只对绝对值拆位。**

### ③ 32-bit 范围

```python
INT_MIN, INT_MAX = -(2**31), 2**31 - 1       # -2147483648, 2147483647
```
**Python 不会溢出，所以范围限制必须手写判断。**
- LC-0007 超范围 → **返回 0**
- LC-0008 超范围 → **夹到边界**
- C++/Java：`n == INT_MIN` 时 `-n` / `abs(n)` **会溢出**（影响 LC-0007、LC-0050）

完整版见 [整数溢出与数值陷阱](<./_resources/overflow-and-numeric-pitfalls.md>)。

---

## 八、跨专题索引

| 题 | 实体位置 | Primary Pattern | Secondary Pattern | Recommended Algorithm | 本专题的关系 |
|---|---|---|---|---|---|
| **LC-0073** Set Matrix Zeroes | [`01-arrays-hashing`](<../01-arrays-hashing (数组、哈希表)/04 - Array Index Mapping 与 In-place Marking/05 - LC-0073 - Set Matrix Zeroes>) | **In-place Marking** | Simultaneous State Update、Matrix Traversal | 第一行/列当标记位，O(1) 空间 | Level 02 的核心题，放学习索引（与 LC-0289 配对） |
| **LC-0050** Pow(x, n) | [**本专题**](<./03 - 整数运算与数位处理 (Arithmetic)/03 - Fast Exponentiation 平方快速幂/01 - LC-0050 - Pow(x, n)>) | **Fast Exponentiation** | Divide and Conquer、Bit Manipulation | 迭代二进制快速幂 | 2026-11-11 实体从 `99-advanced` 迁入本专题（**5 条复习记录已随之保留**） |
| **LC-0202** Happy Number | [`06-linked-list`](<../06-linked-list (链表)/03 - Floyd 环检测与隐式函数图/02 - 隐式函数图与环检测/01 - LC-0202 - Happy Number>) | **Floyd Cycle Detection** | Digit Processing | 快慢指针 | NeetCode 把它归进 Math，但环检测是它的主归属 ⟹ **本次不重复生成** |
| **LC-0069** Sqrt(x) | `05-binary-search` | Binary Search on Answer | Math | 二分 / 牛顿迭代 | 二分是主归属 |
| **LC-2326** Spiral Matrix IV | **本专题** | Spiral Boundary | Linked List Traversal | 四边界 + 链表游标 | 实体在本专题（螺旋是主模式） |
| **LC-3195** Min Area to Cover All Ones | **本专题** | Bounding Box | Matrix Traversal | 一遍扫极值 | 实体在本专题 |

**跨专题规则**（本次执行遵循指令第七节）：
1. 本专题已有原始资料 ⟹ **完整保留**。
2. 本专题没有、其他专题已有 ⟹ **只建 README 跨专题引用**，不复制 PDF。
3. **不修改其他专题的任何文件。**
4. 一道题在仓库里**只能有一个实体文件夹** —— 否则 `review_due.py` 会重复叫号。
5. 同一道题可以通过多个算法理解，但 **Primary Pattern 必须标清**。
6. **不以 LeetCode 标签作为唯一分类依据**（LC-0202 就是例子）。

---

## 九、第二轮独立审核结果

第一轮（指令给定）建议新增 5 道：LC-0073、LC-0050、LC-0289、LC-0007、LC-0223。
其中 **LC-0073 和 LC-0050 仓库里已有**（且 LC-0050 已有 5 条复习记录）
⟹ 按规则 2 改为**跨专题索引**，**实际新建 3 道**。

**第二轮自主新增 3 道**（上限 3，用满）：

| 题 | 填补的缺口（A） | 面试代表性 / 迁移性（B / C） | 为什么不重复（D） |
|---|---|---|---|
| **LC-0149** Max Points on a Line | **Slope Normalization + GCD** —— 本专题唯一一道「用整数方向向量代替浮点斜率」 | 经典几何题；gcd 归一化迁移到所有「同方向/同比例」计数 | 与 LC-2013 的坐标哈希思路不同（它数**方向**，2013 数**顶点组合**） |
| **LC-1861** Rotating the Box | **Rotation + Gravity 的交汇点** —— 教「把复合问题解耦成两个已会的子问题」 | 高频 OA 题；解耦思路迁移极广 | 与 LC-0048（纯旋转）、LC-0723（纯重力+多轮）都不同 |
| **LC-0204** Count Primes | **唯一一道「预处理出一张表，之后 O(1) 查」** 的算法 | Sieve 是最经典的面试算法之一 | 本专题没有任何筛法/预处理类题目 |

**关于 LC-0204 的特别说明**：指令提醒「不要因此自动扩充完整数论专题」。
**本次只收这一道**，而且收它的理由不是「它是数论」，而是
**它是一个可复用的预处理模板**（同一张筛表直接支持最小质因子分解，
见该题 `solution.py` 末尾的演示），
这正是本专题想要的那类知识 —— **不是一个要背的定理**。

**未新增的候选及原因**：

| 题 | 违反的条件 | 原因 | 建议归属 |
|---|---|---|---|
| LC-0202 Happy Number | **F** | 已在 `06-linked-list` 的 Floyd 环检测（主归属） | 已存在，见跨专题索引 |
| LC-0836 Rectangle Overlap | **D** | 与 LC-0223 的交集公式重合，只是把面积换成布尔 | 可作为 LC-0223 的口头追问（已写进其 `Solution_2`） |
| LC-0939 Minimum Area Rectangle | **D** | 与 LC-2013 的坐标哈希思想大量重合，额外教学收益有限 | 将来若要练「矩形计数」再加 |
| LC-1572 Matrix Diagonal Sum | **A, B** | 太简单（两行），不构成独立 Pattern | 不建议单独收录 |
| LC-0013 / LC-0012 Roman | **C, E** | 主要是查表 + 规则记忆，算法迁移性低 | 本专题不收；用户已归档为低优先级 |
| LC-0067 Add Binary | **D** | Carry Propagation 已由 LC-0066 / LC-0043 覆盖 | 本专题不收；用户已归档为低优先级 |
| LC-0006 Zigzag Conversion | **B, C** | 二维轨迹模拟，但不构成核心 Pattern | 本专题不收；用户已归档为低优先级 |
| Convex Hull / FFT / NTT / 高级数论 / 高级组合数学 / 矩阵快速幂 | **E** | 学习成本远超迁移收益；指令明确要求不自动扩充 | 将来确有需要时**单独建专题**（`99-advanced` 已于 2026-11-11 清空） |
| LC-0218 The Skyline Problem | **E, F** | Sweep Line + Heap 难题 | 将来**单独建专题**（`14-intervals` 的审核也把它列为 Future Candidate） |

判断标准（指令第六节 A–F）：
A 填补重要缺口 · B 面试代表性 · C 可迁移性 · D 不是现有题的简单重复 ·
E 学习成本合理 · F 没有其他专题更合适的主归属。

参考资料：NeetCode 150 / 250、Blind 75、Grind 75/169、LeetCode Top Interview 150
的 Math & Geometry 分区。**未编造任何公司的实际出题频次。**

---

## 十、Pattern Recognition 速查

| 题干关键词 | Pattern | 去哪 |
|---|---|---|
| spiral / clockwise / layer by layer | Spiral Boundary | Level 01 |
| diagonal / zigzag | Direction Vectors | Level 01 |
| rotate 90 / transpose / in-place | Coordinate Transformation | Level 02 |
| set entire row and column | In-place Marking | Level 02 |
| simultaneously / next generation | Simultaneous State Update | Level 02 |
| gravity / fall / crush / until stable | Multi-phase Simulation | Level 02 |
| reverse digits / plus one / no string conversion | Digit Processing | Level 03 |
| multiply strings / big integer | Carry Propagation | Level 03 |
| x^n / very large exponent | Fast Exponentiation | Level 03 |
| primes less than n | Sieve | Level 03 |
| minimum area / bounding rectangle | Bounding Box（**+1**） | Level 04 |
| total area covered / union of rectangles | Inclusion-Exclusion（**无 +1**） | Level 04 |
| count squares / same point added twice | Coordinate Frequency Map | Level 04 |
| points on a line / collinear / slope | Slope Normalization + GCD | Level 04 |

完整决策树（Q1–Q15）见 [Pattern Recognition Guide](<./_resources/pattern-recognition-guide.md>)。

---

## 十一、最终建议学习顺序

```
【第一遍 · 6 道】把核心模板学完（P0）
  0054 → 0048 → 0073 → 0066 → 0050 → 2013

【第二遍 · 14 道】标准面试覆盖面（P0 + P1）
  0054 → 0059 → 0498 → 0048 → 0867 → 0073 → 0289
       → 0066 → 0007 → 0008 → 0043 → 0050 → 0223 → 2013

【第三遍 · 21 道】按 Level 1 顺序，对照最完整
  L1 → 0054 0059 2326 0498 0885
  L2 → 0867 0048 0073 0289 0723 1861
  L3 → 0066 0007 0008 0043 0050 0204
  L4 → 3195 0223 2013 0149
```

**配对练习**（一次打穿各自的坑）：

| 配对 | 对照的是什么 |
|---|---|
| `0054` → `0059` → `2326` | **同一骨架**，读 / 写 / 从链表写 |
| `0867` → `0048` | 矩形（新建） vs 正方形（**原地**） |
| `0073` → `0289` | 标记**挤占数据位**（顺序敏感） vs 住**不同 bit**（顺序无关） |
| `0723` → `1861` | 纯重力多轮 vs **重力 + 旋转解耦** |
| `0066` → `0007` | 进位 vs **位序 + 溢出** |
| `0007` → `0008` | 溢出**返回 0** vs 溢出**夹边界** |
| `3195` → `0223` | **数格子（+1）** vs **量面积（无 +1）** |
| `2013` → `0149` | 数**顶点组合** vs 数**方向** |
| `0054` → `0885` | 四边界法 vs 方向向量（起点可在界外） |

---

## 十二、本专题刻意不做的事

- ❌ **不扩充竞赛数学**：Convex Hull、FFT/NTT、高级数论定理、高级组合数学、矩阵快速幂
- ❌ **不收纯查表题**：Roman numerals 这类主要靠记映射的题
- ❌ **不用浮点**：斜率用 `gcd` 方向向量、距离比**平方**、截断用 `abs` + `//`
- ❌ **不把每道题当独立算法**：10 个模板背后只有 4 块骨架

> 本专题要的是**四件手艺**，不是一堆公式：
> 安全处理矩阵边界 · 正确定义遍历方向 · 原地修改不污染旧状态 ·
> 几何转整数比较或 Hash 计数。

---

## 相关资料

| 文档 | 内容 |
|---|---|
| [Pattern Recognition Guide](<./_resources/pattern-recognition-guide.md>) | Q1–Q15 决策树 + 三秒速判表 + 读题三问 |
| [矩阵坐标与边界速查表](<./_resources/matrix-index-cheat-sheet.md>) | 全部坐标变换公式 + 螺旋四步 + 原地修改安全规则 + 必测边界 |
| [整数溢出与数值陷阱](<./_resources/overflow-and-numeric-pitfalls.md>) | Python 负数 `//` `%` + 32-bit 范围 + 浮点为什么能不用就不用 + `gcd` 的坑 |
| [_audit/post-migration-report.md](<./_audit/post-migration-report.md>) | 迁移映射、SHA-256 校验、NC 正式化、跨专题去重结果 |
| [utils/ListNode.py](<./utils/ListNode.py>) | LC-2326 用到的链表辅助类（**原位置不动**，无 import 依赖） |
