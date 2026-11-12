# Level 1 · 02 单调栈及其变体 (Monotonic Stack) —— 跨专题索引目录

> **本目录刻意不放任何题目文件夹。** 单调栈的全部实体题都在
> [18-monotonic-fuck-you (单调栈、单调队列)](<../../18-monotonic-fuck-you (单调栈、单调队列)/README.md>)。

## 为什么不在这里建题目

1. 本仓库的铁律：**凡是沾单调栈 / 单调队列的题，一律归 18 专题**
   （`tools/intake.py` 甚至会在入库时强制改 target）。
2. 一道题在题库里只能有一个实体文件夹 —— 否则 `review_due.py` 的复习队列
   会对同一道题排两次，复习记录也会分叉。
3. 保留这个 Level 1 的编号位，是为了让 Stack 专题的知识地图**完整**：
   学完基础栈之后，下一站确实就是单调栈，只是走路要走到隔壁专题去。

## 本章应该掌握什么（学习目标）

| 对照项 | 普通 Stack（Level 1 · 01） | Monotonic Stack（本章） |
|---|---|---|
| 栈内性质 | 无约束 | **值单调**（递增或递减） |
| 弹出理由 | 匹配上了 / 抵消了 | **这个元素未来再也赢不了** |
| 答案什么时候产生 | 匹配的那一刻 | 被弹出的那一刻（或当前元素汇总过去） |
| 复杂度论证 | 直接 O(n) | 需要**摊还（Amortized）**论证 |

### Monotonic Stack 对照表

| 问题类型 | 栈的单调方向 | Pop 条件 | 栈中保存 | 代表题 |
|---|---|---|---|---|
| Next Greater | 自底向上**递减** | `nums[top] < cur` | 下标 | LC-0496、LC-0739 |
| Next Greater（环形） | 递减 | 同上，跑 2n 轮 | 下标 | LC-0503 |
| Previous Greater / 跨度 | 递减 | `top.price <= cur` | `(值, 跨度)` | LC-0901 |
| Next Smaller / Histogram 边界 | 自底向上**递增** | `heights[top] > cur` | 下标 | LC-0084、LC-0085 |
| Contribution Counting | 递增 | `arr[top] > cur`（严格） | 下标 | LC-0907、LC-2104 |
| Greedy 字典序删除 | 递增 | `stack[-1] > x` **且可行** | 值 | LC-0402、LC-0316、LC-1673 |

> 注意：单调方向会随**扫描方向**、**严格 / 非严格不等号**和实现习惯改变，
> 上表只对「从左到右扫描 + 本仓库采用的比较符号」成立。
> 不要把它当成放之四海皆准的绝对规则 —— 请以每道题 solution.py 里的不变量为准。

## 跨专题链接

| LC | 题 | 位置 |
|---|---|---|
| 0496 | Next Greater Element I | [18 · 01/01/01](<../../18-monotonic-fuck-you (单调栈、单调队列)/01 - 最近更大元素与跨度/01 - Next Greater Element 与索引栈/01 - LC-0496 - Next Greater Element I>) |
| 0739 | Daily Temperatures | [18 · 01/01/02](<../../18-monotonic-fuck-you (单调栈、单调队列)/01 - 最近更大元素与跨度/01 - Next Greater Element 与索引栈/02 - LC-0739 - Daily Temperatures>) |
| 0503 | Next Greater Element II | [18 · 01/01/03](<../../18-monotonic-fuck-you (单调栈、单调队列)/01 - 最近更大元素与跨度/01 - Next Greater Element 与索引栈/03 - LC-0503 - Next Greater Element II>) |
| 0901 | Online Stock Span | [18 · 01/02/01](<../../18-monotonic-fuck-you (单调栈、单调队列)/01 - 最近更大元素与跨度/02 - Previous Greater 与流式跨度/01 - LC-0901 - Online Stock Span>) |
| 0084 | Largest Rectangle in Histogram | [18 · 02/01/01](<../../18-monotonic-fuck-you (单调栈、单调队列)/02 - 单调边界、矩形与贡献计算/01 - Histogram 与最大矩形/01 - LC-0084 - Largest Rectangle in Histogram>) |
| 0907 | Sum of Subarray Minimums | [18 · 02/02/01](<../../18-monotonic-fuck-you (单调栈、单调队列)/02 - 单调边界、矩形与贡献计算/02 - Subarray 极值贡献计算/01 - LC-0907 - Sum of Subarray Minimums>) |
| 0853 | Car Fleet | [18 · 05/01/01](<../../18-monotonic-fuck-you (单调栈、单调队列)/05 - 单调扫描与跨专题存档/01 - Car Fleet 与到达时间单调扫描/01 - LC-0853 - Car Fleet>) |
| 0402 | Remove K Digits | [18 · 03/01/01](<../../18-monotonic-fuck-you (单调栈、单调队列)/03 - 单调栈与贪心构造/01 - 字典序优化与安全删除/01 - LC-0402 - Remove K Digits>) |

完整的单调栈学习路线、模板、严格 / 非严格速查表，见
[18 专题的根 README](<../../18-monotonic-fuck-you (单调栈、单调队列)/README.md>)。
