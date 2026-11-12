# LC-0986 - Interval List Intersections（学习索引）

> ⚠️ **这里没有 `solution.py` / `metadata.json` / PDF，只有这份索引。**
> 本仓库铁律：**一道题只能有一个实体文件夹**，否则复习队列会重复叫号。
> LC-0986 的实体在 `02-two-pointers`（它更早入库，并且 Two Pointers 是它的主归属）：

**👉 实体位置：**
[02-two-pointers (双指针)/05 - 多序列同步扫描/03 - 双序列归并与区间交集/02 - LC-0986 - Interval List Intersections](<../../../../02-two-pointers (双指针)/05 - 多序列同步扫描 (Two Sequences)/03 - 双序列归并与区间交集/02 - LC-0986 - Interval List Intersections>)

---

## 为什么它在本专题里占一个位置

LC-0986 是 **Intervals 专题 Level 1 · 02「双指针区间交集」的模板题本身**。
不把它列出来，本 Level 2 就成了无源之水 ——
[LC-1229 Meeting Scheduler](<../02 - LC-1229 - Meeting Scheduler>) 和
[LC-0759 Employee Free Time](<../../02 - 多人时间表与公共空闲区间/01 - LC-0759 - Employee Free Time>)
都是直接在它的代码骨架上长出来的。

## 模板（必须背下来的四行）

两组**已排序、组内互不相交**的**闭区间** `A`、`B`，求所有交集：

```python
i = j = 0
while i < len(A) and j < len(B):
    left  = max(A[i][0], B[j][0])
    right = min(A[i][1], B[j][1])
    if left <= right:                 # ! 闭区间 ⟹ 必须是 <=，不能写 <
        res.append([left, right])
    if A[i][1] < B[j][1]:             # ! 谁先结束就弹谁
        i += 1
    else:
        j += 1
```

### 两个必须说清的点

**1. 为什么 `left <= right` 不能写成 `left < right`？**
`[1,2]` 和 `[2,3]` 的交集是 **`[2,2]`** —— 单点区间，在闭区间语义下是合法交集。
写 `<` 会把它漏掉。（半开区间就相反，必须 `<`。
参见 [LC-0729](<../../../05 - 离线区间查询与动态预订/02 - 在线插入与区间冲突检测/01 - LC-0729 - My Calendar I>)。）

**2. 为什么「结束更早的区间」可以安全弹掉？**
设 `A[i].end < B[j].end`。要证 `A[i]` 和 `B[j+1], B[j+2], …` 都不可能相交：
B 组内互不相交且有序 ⟹ `B[j+1].start > B[j].end`。
又 `B[j].end > A[i].end` ⟹ `B[j+1].start > A[i].end`
⟹ `B[j+1]` 整个落在 `A[i]` 右边，无交集。后续的 B 区间起点更大，同理。
所以 `A[i]` 的全部交集都已找完，`i += 1` 不丢解。∎

**复杂度：O(m + n)**，O(1) 额外空间（不计输出）。

## 本 Level 2 的学习路径

1. **LC-0986**（本索引）—— 学模板和那个 `<=`
2. [LC-1229 Meeting Scheduler](<../02 - LC-1229 - Meeting Scheduler>) —— 同一模板 + 一个长度过滤 `right - left >= duration`

然后去
[Level 2 · 02 多人时间表与公共空闲区间](<../../02 - 多人时间表与公共空闲区间>)
把双序列推广到 k 序列（K-way Merge + Min Heap）。
