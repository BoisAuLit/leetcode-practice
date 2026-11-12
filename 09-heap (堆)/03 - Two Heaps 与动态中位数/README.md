# Level 1 · 03 Two Heaps 与动态中位数

## 核心定义
一个堆只能给「最小」或「最大」。要拿**中间**的那个，就用**两个堆把数据切成两半**：
左半用最大堆（堆顶是左半最大），右半用最小堆（堆顶是右半最小），
中位数就夹在两个堆顶之间。

## 不变量（整章的地基）
```
small：最大堆（Python 里存负数），放较小的一半
large：最小堆，放较大的一半
① max(small) <= min(large)                  ← 分界正确
② len(small) == len(large) 或 len(small) == len(large) + 1   ← 大小平衡
中位数：总数奇 → small 顶；总数偶 → (small 顶 + large 顶) / 2
```

## 插入的标准两步
```python
heapq.heappush(small, -num)                     # 1. 先无脑进 small
heapq.heappush(large, -heapq.heappop(small))    # 2. 把 small 最大的让给 large（保证不变量①）
if len(large) > len(small):                     # 3. 再平衡大小（保证不变量②）
    heapq.heappush(small, -heapq.heappop(large))
```
这个「先过一遍对面再平衡」的写法，比「先比较再决定进哪边」更不容易写错。

## LC-0480 的新问题：**删除**

LC-0295 只加不删。窗口一滑动，就要**从堆里删掉一个任意元素** ——
而**堆只能删堆顶**。这就是 **Lazy Deletion（惰性删除）** 的用武之地：

```python
to_delete[x] += 1                      # 不真删，只记账
while heap and to_delete[heap[0]] > 0: # 等它浮到堆顶再真删
    to_delete[heap[0]] -= 1
    heapq.heappop(heap)
```

### 由此引出的两个必须处理的后果

**① `len(heap)` 不再等于有效元素数。**
堆里躺着一堆「已标记删除但还没浮上来」的元素。
所以平衡判断**必须用另外维护的 `small_size` / `large_size`**，不能用 `len()`。

**② 删除标记必须分边记（本仓库实测踩到的坑）。**
如果 `small` 和 `large` 里**都有同一个值**（重复元素正好跨越中位线），
用一张共享的 `to_delete` 表时，这一笔删除可能被**错误的那一边**在 prune 时消费掉，
于是计数器和堆内容彻底对不上。
**解决**：`del_small` 和 `del_large` 两张表，各自只消费自己的标记。

> 这个 bug 不会在小样例上暴露 —— 本专题的 solution.py 里用
> 「小值域（0–5）+ 大量重复」的 1000 组随机对拍才把它抓出来。

### 删除时还要先判边
```python
prune_small()
if small_size > 0 and num <= -small[0]:   # ★ 必须在打标记【之前】判断
    del_small[num] += 1; small_size -= 1
else:
    del_large[num] += 1; large_size -= 1
```
顺序反了的话，prune 可能先把它从堆顶弹走，后面就判错边了。

## 题目

| # | 题 | 优先级 | 新增的东西 |
|---|---|---|---|
| 01/01 | LC-0295 Find Median from Data Stream | **P0** | 双堆不变量 + 插入平衡 |
| 02/01 | LC-0480 Sliding Window Median | P2 | **Lazy Deletion** + 逻辑 size + 分边标记 |

## 复杂度
- LC-0295：`addNum` O(log n)，`findMedian` O(1)。
- LC-0480：**O(n log n)**（不是 O(n log k) —— 失效元素会在堆里滞留），空间 O(n)。

**另一条路**：`sortedcontainers.SortedList` 可以 O(log k) 插入/删除 + O(1) 取中位数，
总共 O(n log k)，代码短得多。但它不在标准库里，面试要说明依赖。

## 常见错误
- 只用一个堆想拿中位数（拿不到）。
- 插入时直接比较后决定进哪边，忘了之后还要平衡。
- LC-0480 用 `len(heap)` 做平衡判断。
- LC-0480 用共享的删除标记表。
- 偶数个元素时忘了取两个堆顶的**平均**（且要用浮点）。

## 复习时的 Pattern Recognition
> 「动态维护中位数」「流式数据的第 k 分位」「窗口中位数」
> → Two Heaps。要删除就加 **Lazy Deletion**，并记住它带来的两个后果。
