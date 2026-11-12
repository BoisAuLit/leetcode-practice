# Level 1 · 02 旋转数组、峰值与结构性二分 (Structural Search)

## 核心定义
数组**不是全局有序**，但仍有足够的**局部结构**让我们安全丢掉一半。
这一章要打破「二分 = 有序数组」的错误印象。

## 决定性观察
1. **旋转数组**：无论怎么旋转，用 mid 切开后**至少有一半是有序的**。
   判断出哪一半有序，就能判断 target 在不在那一半里。
2. **峰值**：只要比较 `nums[mid]` 和 `nums[mid+1]`，**往更高的那一侧走**必然能找到峰。
   不需要全局有序，只需要「边界外视为 -∞」这个约定。
3. **奇偶结构**：元素成对出现时，配对的起始下标有固定的奇偶规律；
   单独那个元素会**打破**这个规律，于是「规律是否还成立」就是一个单调谓词。
4. **自己构造谓词**：数组本身没有可二分的性质时，可以构造一个与下标相关的
   单调函数（LC-1539 的 `missing(i)`、LC-0275 的 `citations[i] >= n-i`）再二分。

## 各小节的不变量

### 01 Rotated Sorted Array
```python
# LC-0153 找最小值：和「右边界」比较
while lo < hi:
    mid = (lo + hi) // 2
    if nums[mid] > nums[hi]: lo = mid + 1   # 最小值一定在右半
    else:                    hi = mid       # 最小值在左半（含 mid）
return nums[lo]
```
**为什么和 `nums[hi]` 比而不是 `nums[lo]` 比**：
和 `nums[lo]` 比时，完全未旋转的数组（`[1,2,3]`）会被误判。和右边界比则没有这个问题。

```python
# LC-0033 找 target
if nums[lo] <= nums[mid]:                   # 左半有序
    if nums[lo] <= target < nums[mid]: hi = mid - 1
    else:                              lo = mid + 1
else:                                       # 右半有序
    if nums[mid] < target <= nums[hi]: lo = mid + 1
    else:                              hi = mid - 1
```
**为什么至少一半有序**：旋转只有一个「断点」，mid 把数组切两半，
断点只能落在其中一半里，另一半必然连续有序。

**这个论证的前提是「无重复元素」**。LC-0081 就是它的反例，见下。

### 02 Peak 与奇偶结构
```python
# LC-0162 找峰值
while lo < hi:
    mid = (lo + hi) // 2
    if nums[mid] < nums[mid + 1]: lo = mid + 1   # 上坡 → 右边一定有峰
    else:                         hi = mid       # 下坡或平 → 左边（含 mid）一定有峰
return lo
```
**为什么往高处走一定有峰**：若 `nums[mid] < nums[mid+1]`，从 mid+1 继续往右，
要么一直升到边界（边界外是 -∞，所以末元素就是峰），要么中途下降（下降点就是峰）。
两种情况右半都有峰 ⟹ 丢左半安全。

```python
# LC-0540 单一元素
while lo < hi:
    mid = (lo + hi) // 2
    mid -= mid & 1                     # 把 mid 对齐到偶数（每对的起点）
    if nums[mid] == nums[mid + 1]: lo = mid + 2   # 前面全部配对正常 → 答案在右
    else:                          hi = mid
return nums[lo]
```
**奇偶规律**：单一元素**之前**，每一对都从偶数下标开始（`nums[even] == nums[even+1]`）；
单一元素**之后**，配对错位一格，这个等式不再成立。
谓词「`nums[even] == nums[even+1]`」正是 `T T T F F F` ⟹ 找 First False。

### 03 索引单调状态
- **LC-1539**：`missing(i) = arr[i] - (i + 1)` = 前 i+1 个位置之前缺失的数字个数。
  数组严格递增且都是正整数 ⟹ missing 单调不减 ⟹ 二分找第一个 `missing(i) >= k`。
  **注意**：它是对**下标与缺失量的关系**二分，不是对答案做成本模拟，
  所以不算典型的 Binary Search on Answer。
- **LC-0658**：对**定长窗口的起点**二分，比较 `x - arr[mid]` 和 `arr[mid+k] - x`。
- **LC-0275**：谓词 `citations[i] >= n - i`，单调性需要自己证（见 solution.py）。

## 题目

| # | 题 | 优先级 |
|---|---|---|
| 01/01 | LC-0153 Find Minimum in Rotated Sorted Array | P0 |
| 01/02 | LC-0033 Search in Rotated Sorted Array | P0 |
| 01/03 | LC-0081 Search in Rotated Sorted Array II | P1（第二轮新增） |
| 02/01 | LC-0162 Find Peak Element | P0 |
| 02/02 | LC-0540 Single Element in a Sorted Array | P1 |
| 03/01 | LC-1539 Kth Missing Positive Number | P1 |
| 03/02 | LC-0658 Find K Closest Elements | P1 |
| 03/03 | LC-0275 H-Index II | P1（第二轮新增） |

## 重复元素会让旋转二分退化（LC-0081 的核心教训）
`[3,1,3,3,3]`：lo=0, mid=2 时 `nums[lo] == nums[mid] == 3`，
但左半 `[3,1,3]` **不是**有序的 —— LC-0033 的论证在这里失效。
唯一安全的处理是 `lo += 1; hi -= 1`（各收缩一格），
代价是最坏 **O(n)**（例如 `[1,1,1,1,1,0,1]` 找 0）。

**结论：有重复元素时，旋转数组搜索无法保证 O(log n)。** 面试里要主动说出来。
LC-0154（旋转数组找最小值 + 重复）是同一现象的另一面。

## 常见错误
- LC-0153 和 `nums[lo]` 比较（未旋转数组会误判）。
- LC-0033 的区间判断漏掉等号（`nums[lo] <= target` 的那个 `=`）。
- LC-0162 写成 `nums[mid] > nums[mid-1]`（mid=0 时越界）。
- LC-0540 忘了把 mid 对齐到偶数。
- 把 LC-0033 的代码直接用在有重复元素的输入上。

## 复习时的 Pattern Recognition
> 「旋转过的有序数组」「找峰 / 局部最大」「成对出现只有一个落单」
> 「我能不能自己构造一个关于下标的单调量」 → 本章。
