# 05 · Binary Search（二分查找）

> **二分查找并不要求数组有序。** 它真正依赖的是：能否用 O(1) 的判断
> **安全地丢掉一半搜索空间**。有序只是最常见的那种结构。
> 但反过来也不能泛化 —— 不是所有优化问题都能二分，**必须先验证谓词的单调性**。

本专题共 **26 道题** + 1 条跨专题索引，6 个 Level 1。

## 一、知识地图

| Level 1 | 主题 | 题数 | README |
|---|---|---|---|
| 01 | 基础查找与边界二分 (Basic and Boundary Search) | 9 | [→](<01 - 基础查找与边界二分 (Basic and Boundary Search)/README.md>) |
| 02 | 旋转数组、峰值与结构性二分 (Structural Search) | 8 | [→](<02 - 旋转数组、峰值与结构性二分 (Structural Search)/README.md>) |
| 03 | 二分答案与可行性判断 (Binary Search on Answer) | 8 | [→](<03 - 二分答案与可行性判断 (Binary Search on Answer)/README.md>) |
| 04 | 二分查找与数据结构设计 (Design) | 1 | [→](<04 - 二分查找与数据结构设计 (Binary Search Design)/README.md>) |
| 05 | 双有序数组与分区二分 (Partition) | 1 | [→](<05 - 双有序数组与分区二分 (Binary Search Partition)/README.md>) |
| 06 | 低优先级与跨专题存档 (Archive) | 3 | [→](<06 - 低优先级与跨专题存档 (Archive)/README.md>) |

```
01 - 基础查找与边界二分/
  01 - 标准精确查找/            01 - LC-0704                        P0
  02 - Lower Bound 与 Upper Bound/ 01 - LC-0035  02 - LC-0034  03 - LC-0278   P0 P0 P1
  03 - 二维有序结构与未知边界/   01 - LC-0074 ←新  02 - LC-0702       P0 P1
  04 - 整数范围与单调数学谓词/   01 - LC-0069  02 - LC-0367  03 - LC-0374     P1 P2 P2
02 - 旋转数组、峰值与结构性二分/
  01 - Rotated Sorted Array/     01 - LC-0153  02 - LC-0033  03 - LC-0081 ←新₂  P0 P0 P1
  02 - Peak 与奇偶结构/          01 - LC-0162  02 - LC-0540       P0 P1
  03 - 索引单调状态与连续窗口起点/ 01 - LC-1539  02 - LC-0658 ←新  03 - LC-0275 ←新₂  P1 P1 P1
03 - 二分答案与可行性判断/
  01 - 最小可行速度、时间与资源/  01 - LC-0875  02 - LC-1011 ←新  03 - LC-1482 ←新  04 - LC-1283 ←新
  02 - Minimize Maximum 与贪心可行性/ 01 - LC-0410 ←新  02 - LC-2616
  03 - Maximize Minimum/         01 - LC-1552 ←新
  04 - 值域二分与计数可行性/      → 跨专题索引（LC-0378 实体目录在 09-heap）
04 - 二分查找与数据结构设计/      01 - LC-0981                      P0
05 - 双有序数组与分区二分/        01 - LC-0004（原 NC 升格）         P1
06 - 低优先级与跨专题存档/        01 - LC-0270  02 - LC-3346  03 - LC-3733   P2
_resources/  00-Theory/（原有理论资料）  templates/（原有模板，含 1 个符号链接）
```

---

## 二、四个核心模板（只需要这四个）

### 模板一 · Exact Binary Search（精确查找）
```python
lo, hi = 0, len(nums) - 1              # 闭区间 [lo, hi]
while lo <= hi:                        # 区间非空就继续
    mid = (lo + hi) // 2
    if nums[mid] == target: return mid
    if nums[mid] < target: lo = mid + 1
    else:                  hi = mid - 1
return -1
```
**不变量**：target 若存在，一定在 `[lo, hi]` 内。
**为什么能丢一半**：`nums[mid] < target` 且数组有序 ⟹ `nums[0..mid]` 全都 < target。
**为什么不会死循环**：每轮 `lo` 严格增或 `hi` 严格减，区间长度至少减 1。
O(log n) / O(1)。

### 模板二 · Lower Bound / First True（找第一个成立的位置）
```python
lo, hi = 0, len(nums)                  # 左闭右开 [lo, hi)，hi = n 表示「都不成立」
while lo < hi:
    mid = (lo + hi) // 2
    if predicate(mid): hi = mid        # 成立 → 答案在左边（含 mid），不能丢 mid
    else:              lo = mid + 1
return lo
```
**不变量**：`[0, lo)` 全部不成立，`[hi, n)` 全部成立；收敛时 `lo == hi` 就是分界点。
**适用前提**：谓词形如 `F F F T T T`。
`predicate = nums[i] >= target` ⟹ **Lower Bound**；`nums[i] > target` ⟹ **Upper Bound**。
复用：35、34、278、74、875、1011、1482、1283、410、378、275。

### 模板三 · Last True / Maximum Feasible（找最后一个成立的位置）
```python
lo, hi = 0, n - 1
while lo < hi:
    mid = (lo + hi + 1) // 2           # ★ 必须向上取整
    if predicate(mid): lo = mid        # 成立 → 答案在右边（含 mid）
    else:              hi = mid - 1
return lo
```
**为什么 mid 要向上取整**：更新 `lo = mid` 时，若 mid 向下取整，
当 `hi == lo + 1` 时 `mid == lo`，`lo = mid` 什么都没变 ⟹ **死循环**。
口诀：**更新哪一边，mid 就往哪一边偏。**
复用：1552。（也可以用「闭区间 + 显式 ans 变量」的写法绕开这个坑。）

### 模板四 · Binary Search on Answer（二分答案）
```python
def feasible(x) -> bool: ...           # 把优化问题变成判定问题
lo, hi = 可能的最小答案, 可能的最大答案
while lo < hi:
    mid = (lo + hi) // 2
    if feasible(mid): hi = mid         # 求最小可行；求最大可行则换模板三
    else:             lo = mid + 1
return lo
```
**三件套**：答案空间上下界 → feasible 函数 → **证明 feasible 的单调性**。
**复杂度是 O(n · log R)，不是 O(log R)** —— 每次 feasible 都要扫一遍数据。

| 模板 | 时间 | 空间 |
|---|---|---|
| 一 精确查找 | O(log n) | O(1) |
| 二 Lower Bound / First True | O(log n) | O(1) |
| 三 Last True | O(log n) | O(1) |
| 四 二分答案 | **O(n · log R)** | O(1) |
| LC-0004 分区二分 | O(log min(m,n)) | O(1) |

### 两种区间约定（不要混用）

| | 闭区间 `[lo, hi]` | 左闭右开 `[lo, hi)` |
|---|---|---|
| 初值 | `hi = n - 1` | `hi = n` |
| 循环条件 | `while lo <= hi` | `while lo < hi` |
| 丢左半 | `lo = mid + 1` | `lo = mid + 1` |
| 丢右半 | `hi = mid - 1` | `hi = mid` |
| 结束状态 | `lo == hi + 1` | `lo == hi` |
| 最适合 | 精确查找 | 边界查找（First/Last True） |

**本仓库的约定**：精确查找用闭区间；一切边界 / 二分答案用左闭右开（或闭区间 + 显式 ans）。
同一份代码里绝不混用两种约定 —— 这是二分写错的头号原因。

---

## 三、Binary Search on Answer 的适用条件

能用二分答案，必须同时满足：

1. 答案落在一个**可枚举的整数（或有限精度）区间**里。
2. 存在 `feasible(x)`，且**可以在多项式时间内判定**。
3. **`feasible` 单调**：`feasible(x)` 为真 ⟹ 所有更大（或更小）的 x 也为真。

第 3 条是关键，**必须逐题证明，不能想当然**。
本专题每道二分答案题的 `solution.py` 里都写了单调性论证，并用暴力枚举对拍验证过。

| | Minimize Maximum | Maximize Minimum |
|---|---|---|
| 谓词形状 | `F F F T T T` | `T T T F F F` |
| 目标 | First True | **Last True** |
| 可行时 | `hi = mid` | `lo = mid` |
| mid 取整 | 向下 | **向上** |
| 例题 | 875、1011、1482、1283、410、378 | 1552 |

**什么时候不能二分**：feasible 不单调（比如目标函数先降后升但不是单峰、
或者存在「资源互相挤占」导致 x 变大反而不可行）。
LC-3733 的可行性涉及周期性不可用时间与容斥，就属于「能二分但 feasible 很特殊」的情形。

---

## 四、与其他算法的边界

| 看起来像二分，其实是 | 为什么 |
|---|---|
| **双指针**（LC-0658 也能做） | 窗口两端收缩是 O(n)，二分是 O(log n + k)。n 和 k 接近时双指针更简单 |
| **堆**（LC-0378 也能做） | k 很小时 O(k log n) 更快；k 接近 n² 时值域二分更优且 O(1) 空间 |
| **Sliding Window**（LC-3346） | 它有 Binary Search 标签，但主解法是排序 + 滑窗 + 前缀和 |
| **BST 遍历**（LC-0270） | 利用的是树的有序性，不是数组二分模板 |
| **DP**（LC-0410 也能做） | DP 是 O(k·n²) 的通用解，不依赖「元素非负」；二分更快但需要贪心前提 |

---

## 五、P0 / P1 / P2

**P0（8 道，核心必练）**
LC-0704、LC-0035、LC-0034、LC-0074、LC-0153、LC-0033、LC-0162、LC-0875、LC-1011、LC-1482、LC-0981

**P1（13 道）**
LC-0278、LC-0540、LC-1539、LC-0702、LC-0069、LC-1283、LC-0410、LC-2616、LC-1552、
LC-0658、LC-0004、LC-0081、LC-0275、LC-0378

**P2（5 道）**
LC-0367、LC-0374、LC-0270、LC-3346、LC-3733

### 推荐学习顺序
```
阶段 A 模板打底   704 → 35 → 34 → 278
阶段 B 结构二分   74 → 153 → 33 → 162 → 540 → 81
阶段 C 自造谓词   69 → 1539 → 275 → 658
阶段 D 二分答案   875 → 1011 → 1283 → 1482 → 410 → 2616
阶段 E 反向边界   1552（Maximize Minimum，注意 mid 向上取整）
阶段 F 值域二分   378
阶段 G 设计与进阶 981 → 4
阶段 H 存档       270、3346、3733
```

---

## 六、跨专题索引

| LC | 本专题的角色 | 主归属 |
|---|---|---|
| LC-0270 Closest BST Value | Level 1 `06`，利用 BST 有序性，不是数组二分 | 更适合 [07-trees](<../07-trees (树)/>) 的 BST 分类复习 |
| LC-2616 Minimize the Max Diff of Pairs | Level 1 `03`，排序 + 二分答案 + 贪心配对 | 本专题（Greedy 专题没有这道题） |
| LC-3346 Max Frequency After Operations I | Level 1 `06`，标签有 Binary Search，实解是排序 + 滑窗 + 差分 | 更接近 [03-sliding-window](<../03-sliding-window (滑动窗口)/>) |
| LC-0378 | 值域二分 + 计数型 feasible | **实体目录在 09-heap**，本专题 `03/04` 只建索引 |
| LC-0004 | 原 `NC - Median of Two Sorted Arrays` 已正式化为 LC-0004 | 本专题 |

---

## 七、第二轮独立审核结果

**自主新增 3 道**（上限 5，没有凑数）：

| 题 | Pattern | 为什么值得加 | 与已有题的区别 | 位置 | 优先级 |
|---|---|---|---|---|---|
| LC-0081 Search in Rotated Sorted Array II | Rotated + 重复元素退化 | **它是 LC-0033 的反例**：`[3,1,3,3,3]` 会让「`nums[lo] <= nums[mid]` ⟹ 左半有序」失效。有了它才知道 033 的证明依赖什么前提，并理解最坏退化为 O(n) | 033 无重复，081 必须处理相等收缩 | `02/01/03` | P1 |
| LC-0275 H-Index II | 下标相关的单调谓词 | 要自己**构造**谓词 `citations[i] >= n - i` 并证明其单调，和 LC-1539 同族；Top Interview 150 题 | 1539 求「第一个达到 k」，275 求「边界换算出的答案」 | `02/03/03` | P1 |
| LC-0378 Kth Smallest in Sorted Matrix | 值域二分 + 计数可行性 | 补上「feasible 是一个**计数**而非贪心模拟」这个重要变体；并证明「答案必然是矩阵中真实存在的元素」 | 其余二分答案题的 feasible 都是贪心模拟；也和 LC-0074 形成「能不能展开成一维」的对比 | **`03/04` 索引**（实体目录在 09-heap，那里已有此题；我把值域二分解法并入了那份 solution.py） | P1 |

**审核过、决定不加（Future Candidates）**

| 题 | 理由 |
|---|---|
| LC-0852 Peak Index in a Mountain Array | 和 LC-0162 高度重复，只是多了「保证是山脉」的条件 |
| LC-0154 Find Minimum in Rotated Array II | 和新增的 LC-0081 是同一个退化现象，加一道就够了 |
| LC-1760 Minimum Limit of Balls in a Bag | 和 Koko / LC-1283 的 feasible 几乎一致 |
| LC-1870 Minimum Speed to Arrive on Time | 同上，只多了「最后一段不取整」的小细节 |

---

## 八、原有资料与 Git 安全

- `00-Theory/` 和 `templates (模板)/` 已整体搬到 [`_resources/`](<_resources>)，
  **内容一字未改**，Template 1 / 2 / 3 和两个 bisect 示例全部保留。
- `_resources/templates/02 - 2616 - Min the Max Diff of Pairs.py` 是一个**符号链接**，
  指向 `leetcode-practice/greedy/003 - 2616 - A - (M) - Min the Max Diff of Pairs.py`。
  该目标**已不存在**（greedy 目录在更早的重构中改名了），所以这是一条**失效链接**。
  按要求：**原样保留、不解引用、不自动修复、不修改外部目录**。
- **修正了一处真实 bug**：`LC-0367 - Valid Perfect Square` 的 `metadata.json` 里，
  `link.leetcode` 原先错误地指向 `minimize-the-maximum-difference-of-pairs`（那是 LC-2616），
  已改为 `valid-perfect-square`。
- 未执行 `git add` / `commit` / `push`；未使用 `rm -rf`；未覆盖任何已有 `solution.py`。

完整校验见 [_audit/post-migration-report.md](<_audit/post-migration-report.md>)。
