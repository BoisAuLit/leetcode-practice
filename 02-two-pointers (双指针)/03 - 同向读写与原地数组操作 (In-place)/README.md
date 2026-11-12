# 03 - 同向读写与原地数组操作 (In-place)

## 算法定义

两个指针**同向**移动：`read` 负责遍历，`write` 负责维护「已经处理好的前缀」。
因为 `write <= read` 恒成立，写入永远不会覆盖还没读到的数据，所以可以原地完成。

## Pointer Movement Rules

| 子类 | 规则 |
|---|---|
| 过滤 / 去重（0026、0027、0283、0080）| `read` 每轮必进；满足条件才写入并 `write += 1` |
| 从末尾合并（0088）| 两个 read 从各自末尾往前，`write` 从总末尾往前 |
| 三路分区（0075）| 三个指针 `lo` / `mid` / `hi`，**从 hi 换过来的元素要重新检查** |
| 反转 / 旋转（0189、0031）| 区间反转作为原子操作，组合出旋转和下一个排列 |

## Loop Invariants

1. `nums[0:write]` 永远是一个合法答案（已过滤 / 已去重 / 已排好）。
2. `write <= read` ⇒ 原地安全。
3. 0075 的四段不变量：`[0, lo)` 全是 0、`[lo, mid)` 全是 1、`(hi, n)` 全是 2、`[mid, hi]` 未知。
   **这四句话背下来，Dutch National Flag 就不会写错。**

## 必备模板

```python
# 过滤 / 去重（k = 每个值最多保留几个；k=1 是 LC-0026，k=2 是 LC-0080）
write = 0
for read in range(len(nums)):
    if write < k or nums[read] != nums[write - k]:
        nums[write] = nums[read]
        write += 1
return write

# 三路分区 Dutch National Flag（LC-0075）
lo, mid, hi = 0, 0, len(nums) - 1
while mid <= hi:
    if nums[mid] == 0:
        nums[lo], nums[mid] = nums[mid], nums[lo]
        lo += 1
        mid += 1          # ! 换来的一定是 1（它来自 [lo, mid) 区间），可以放心前进
    elif nums[mid] == 2:
        nums[mid], nums[hi] = nums[hi], nums[mid]
        hi -= 1           # ! mid 不动！换来的元素来自未知区，必须重新检查
    else:
        mid += 1

# 三次反转 = 旋转 k 位（LC-0189）
k %= n
reverse(0, n - 1); reverse(0, k - 1); reverse(k, n - 1)
```

## 本家族题目

| | 题 | 难度 | 这一题新增的东西 |
|---|---|---|---|
| **P0** | [LC-0026 - Remove Duplicates from Sorted Array](01%20-%20%E5%BF%AB%E6%85%A2%E8%AF%BB%E5%86%99%E4%B8%8E%E5%85%83%E7%B4%A0%E8%BF%87%E6%BB%A4/01%20-%20LC-0026%20-%20Remove%20Duplicates%20from%20Sorted%20Array) | E | 读写指针的原型 |
| **P1** | [LC-0027 - Remove Element](01%20-%20%E5%BF%AB%E6%85%A2%E8%AF%BB%E5%86%99%E4%B8%8E%E5%85%83%E7%B4%A0%E8%BF%87%E6%BB%A4/02%20-%20LC-0027%20-%20Remove%20Element) | E | 写入条件从「和前一个不同」换成「不等于目标值」 |
| **P0** | [LC-0283 - Move Zeroes](01%20-%20%E5%BF%AB%E6%85%A2%E8%AF%BB%E5%86%99%E4%B8%8E%E5%85%83%E7%B4%A0%E8%BF%87%E6%BB%A4/03%20-%20LC-0283%20-%20Move%20Zeroes) | E | 要求**保持相对顺序**（稳定），所以不能用对撞交换 |
| **P1** | [LC-0080 - Remove Duplicates from Sorted Array II](01%20-%20%E5%BF%AB%E6%85%A2%E8%AF%BB%E5%86%99%E4%B8%8E%E5%85%83%E7%B4%A0%E8%BF%87%E6%BB%A4/04%20-%20LC-0080%20-%20Remove%20Duplicates%20from%20Sorted%20Array%20II) | M | 和 `nums[write - k]` 比较，一行推广到「最多 k 个」 |
| **P0** | [LC-0088 - Merge Sorted Array](02%20-%20%E4%BB%8E%E6%9C%AB%E5%B0%BE%E5%8E%9F%E5%9C%B0%E5%90%88%E5%B9%B6/01%20-%20LC-0088%20-%20Merge%20Sorted%20Array) | E | **倒着**合并才不会覆盖 nums1 里尚未处理的数据 |
| **P0** | [LC-0075 - Sort Colors](03%20-%20%E4%B8%89%E8%B7%AF%E5%88%86%E5%8C%BA%E4%B8%8E%E5%A4%9A%E6%8C%87%E9%92%88/01%20-%20LC-0075%20-%20Sort%20Colors) | M | 三指针 + 四段不变量；从 hi 换来的元素要重新检查 |
| **P1** | [LC-0189 - Rotate Array](04%20-%20%E5%8F%8D%E8%BD%AC%E3%80%81%E6%97%8B%E8%BD%AC%E4%B8%8E%E6%8E%92%E5%88%97/01%20-%20LC-0189%20-%20Rotate%20Array) | M | 三次反转的恒等式 |
| **P1** | [LC-0031 - Next Permutation](04%20-%20%E5%8F%8D%E8%BD%AC%E3%80%81%E6%97%8B%E8%BD%AC%E4%B8%8E%E6%8E%92%E5%88%97/02%20-%20LC-0031%20-%20Next%20Permutation) | M | 字典序结构：找 pivot → 换后继 → 反转后缀 |

## 最容易出错的地方

- **0088 正着合并**：会覆盖 nums1 前面还没处理的元素，必须从后往前。
- **0075 换到 hi 之后把 mid 也 +1**：换来的元素没检查过，会漏。本章第一大坑。
- **0080 漏了 `write < k` 判断**：`write - k` 会变成负下标，Python 不报错但静默出错。
- **0189 忘了 `k %= n`**：k 可以大于数组长度。
- **0031 的方向**：从右往左找第一个 `nums[i] < nums[i+1]`（pivot），再从右往左找第一个
  大于 `nums[i]` 的数交换，最后反转 `i+1` 之后的后缀。它**不是对撞指针题**，
  核心是排列的字典序结构。

## 与相邻家族的区别

- **Level 01 对撞**：两端相向、靠有序性排除候选；本家族同向、靠 `write <= read` 保证安全。
- **Sliding Window**：也是同向两个指针，但窗口两端由**同一个约束**驱动（窗口要合法），
  而本家族的 `write` 只是输出位置，不参与判断。对比见根 [README.md](../README.md)。
