# Math & Geometry Pattern Recognition Guide（题型识别指南）

> 这些是**帮助识别问题的提示，不是绝对互斥的分类**。
> 一道题经常同时命中多条（LC-1861 = Q3 + Q6，LC-2013 = Q12 + Design）。

---

## 决策树

### Q1：是否按指定顺序访问二维矩阵？
→ **Matrix Traversal（矩阵遍历）**。先定义「方向」，再定义「什么时候换方向」。
📍 [Level 1 · 01](<../01 - 矩阵遍历与方向模拟 (Matrix Traversal)>)

### Q2：是否顺时针一圈圈处理矩阵？
→ **Spiral Boundary（螺旋边界）**。维护 `top / bottom / left / right` 四个边界，
每走完一条边就**收缩**它。
📍 [LC-0054](<../01 - 矩阵遍历与方向模拟 (Matrix Traversal)/01 - 螺旋遍历、生成与填充/01 - LC-0054 - Spiral Matrix>)（读）、
[LC-0059](<../01 - 矩阵遍历与方向模拟 (Matrix Traversal)/01 - 螺旋遍历、生成与填充/02 - LC-0059 - Spiral Matrix II>)（写）、
[LC-2326](<../01 - 矩阵遍历与方向模拟 (Matrix Traversal)/01 - 螺旋遍历、生成与填充/03 - LC-2326 - Spiral Matrix IV>)（从链表写）

### Q3：是否需要改变矩阵元素的坐标？
→ **Matrix Transformation（坐标变换）**。写出 `(r, c) → (?, ?)` 的映射公式，拿 2×2 验证。
📍 [LC-0867 Transpose](<../02 - 矩阵变换与状态模拟 (Matrix Transformation)/01 - 转置与矩阵旋转/01 - LC-0867 - Transpose Matrix>)、
[LC-0048 Rotate Image](<../02 - 矩阵变换与状态模拟 (Matrix Transformation)/01 - 转置与矩阵旋转/02 - LC-0048 - Rotate Image>)

### Q4：是否需要原地修改整个行或列？
→ **In-place Marking（原地标记）**。把标记塞进矩阵自己的某一行/列，换 O(1) 空间；
代价是**写入顺序**变得关键。
📍 [LC-0073 Set Matrix Zeroes](<../02 - 矩阵变换与状态模拟 (Matrix Transformation)/02 - 原地标记与同步状态更新/01 - LC-0073 - Set Matrix Zeroes (学习索引 · 实体在 01-arrays-hashing)>) ↗️

### Q5：下一轮状态是否只能依赖旧状态？
→ **Simultaneous State Update（同步状态更新）**。三段式：
`Read Original State → Record Updates → Apply Updates`。
📍 [LC-0289 Game of Life](<../02 - 矩阵变换与状态模拟 (Matrix Transformation)/02 - 原地标记与同步状态更新/02 - LC-0289 - Game of Life>)、LC-0073

### Q6：是否需要模拟重力、消除、重新填充？
→ **Multi-phase Matrix Simulation（多阶段矩阵模拟）**。
把「标记」「消除」「下落」拆成独立的 pass，别缠在一起。
📍 [LC-0723 Candy Crush](<../02 - 矩阵变换与状态模拟 (Matrix Transformation)/03 - 多轮矩阵消除与重力模拟/01 - LC-0723 - Candy Crush>)（多轮）、
[LC-1861 Rotating the Box](<../02 - 矩阵变换与状态模拟 (Matrix Transformation)/03 - 多轮矩阵消除与重力模拟/02 - LC-1861 - Rotating the Box>)（一轮 + 旋转）

### Q7：是否需要逐位处理整数？
→ **Digit Processing（数位处理）**。`digit = x % 10; x //= 10`。
⚠️ Python 对负数是**向下取整**，先剥符号。
📍 [LC-0066 Plus One](<../03 - 整数运算与数位处理 (Arithmetic)/01 - 数位进位与整数反转/01 - LC-0066 - Plus One>)、
[LC-0007 Reverse Integer](<../03 - 整数运算与数位处理 (Arithmetic)/01 - 数位进位与整数反转/02 - LC-0007 - Reverse Integer>)

### Q8：是否需要模拟加法或乘法的进位？
→ **Carry Propagation（进位传播）**。从低位往高位扫，`carry` 一路带着走。
📍 LC-0066、[LC-0043 Multiply Strings](<../03 - 整数运算与数位处理 (Arithmetic)/02 - 字符串解析与大整数乘法/02 - LC-0043 - Multiply Strings>)

### Q9：是否需要计算很大的整数指数？
→ **Fast Exponentiation（平方快速幂）**。按指数的二进制位选平方项，O(log n)。
📍 [LC-0050 Pow(x, n)](<../03 - 整数运算与数位处理 (Arithmetic)/03 - Fast Exponentiation 平方快速幂/01 - LC-0050 - Pow(x, n)>)

### Q10：是否需要覆盖所有有效点的最小矩形？
→ **Bounding Box（最小外接矩形）**。扫一遍记 `minR / maxR / minC / maxC`。
⚠️ **离散格子要 `+1`**。
📍 [LC-3195](<../04 - 坐标几何与空间计数 (Geometry)/01 - Bounding Box 与矩形交集/01 - LC-3195 - Find the Minimum Area to Cover All Ones I>)

### Q11：是否需要两个矩形的面积并集？
→ **Rectangle Intersection + Inclusion-Exclusion（矩形交集 + 容斥）**。
`A∪B = A + B − A∩B`，交集宽高用 `max(0, min(右) - max(左))`。
⚠️ **连续坐标不要 `+1`**。
📍 [LC-0223 Rectangle Area](<../04 - 坐标几何与空间计数 (Geometry)/01 - Bounding Box 与矩形交集/02 - LC-0223 - Rectangle Area>)

### Q12：是否需要统计重复坐标组成的图形数量？
→ **Coordinate Frequency Map（坐标频率表）**。
⚠️ **必须是 Counter，不能是 Set** —— 重复点的组合数要乘起来。
📍 [LC-2013 Detect Squares](<../04 - 坐标几何与空间计数 (Geometry)/02 - 坐标 Hash Map 与正方形计数/01 - LC-2013 - Detect Squares>)

### 补充 Q13：是否要判断/统计点共线？
→ **Slope Normalization + GCD**。用 `gcd` 约简的整数方向向量做 key，
**不要用浮点斜率**；方向相反要统一符号。
📍 [LC-0149 Max Points on a Line](<../04 - 坐标几何与空间计数 (Geometry)/03 - 斜率归一化与共线计数/01 - LC-0149 - Max Points on a Line>)

### 补充 Q14：是否要反复查询「某个范围内的素数 / 因子」？
→ **Sieve（筛法）**：一次预处理出表，之后 O(1) 查。
📍 [LC-0204 Count Primes](<../03 - 整数运算与数位处理 (Arithmetic)/04 - 筛法与素数计数/01 - LC-0204 - Count Primes>)

### 补充 Q15：题目要不要求 **O(1) 额外空间**？
→ 这决定你走哪条路，而不是走哪个 Pattern：
- 矩阵：把标记塞进矩阵本身（LC-0073）或塞进**高位 bit**（LC-0289）
- 数位：用整数运算而不是转字符串
**先写出 O(n) 空间的正确版，再优化。** 面试这样做分更高。

---

## 三秒速判表

| 题干关键词 | Pattern |
|---|---|
| spiral / clockwise / layer by layer | Spiral Boundary |
| diagonal / zigzag | Direction Vectors |
| rotate 90 / transpose / in-place | Coordinate Transformation |
| set entire row and column | In-place Marking |
| simultaneously / next generation / all cells at once | Simultaneous State Update |
| gravity / fall / crush / until stable | Multi-phase Simulation |
| reverse digits / plus one / without converting to string | Digit Processing |
| multiply strings / add binary / big integer | Carry Propagation |
| x^n / modpow / very large exponent | Fast Exponentiation |
| minimum area / bounding rectangle | Bounding Box（**+1**） |
| total area covered / union of rectangles | Inclusion-Exclusion（**不 +1**） |
| count squares / count rectangles / same point added twice | Coordinate Frequency Map |
| points on a line / collinear / slope | Slope Normalization + GCD |
| primes less than n | Sieve |

---

## 读矩阵题时的三问

1. **矩阵是不是正方形？** 正方形才可能原地旋转；矩形旋转后形状都变了。
2. **新状态依赖旧状态吗？** 依赖 ⟹ 必须两阶段（或把新旧状态编码到同一个数里）。
3. **是在数格子还是在量长度？** 数格子要 `+1`，量长度不要。

## 读数值题时的三问

1. **会不会有负数？** 有 ⟹ Python 的 `//` `%` 语义和 C 不同，先剥符号。
2. **有没有 32-bit 范围限制？** 有 ⟹ Python 不会溢出，但**必须手写判断**。
3. **要不要避免转字符串？** 要 ⟹ 用 `% 10` / `// 10`。
