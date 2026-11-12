# Level 1 · 04 二分查找与数据结构设计 (Binary Search Design)

## 核心定义
二分不只是一个算法，也可以是**数据结构的查询原语**：
在一个按 key 分桶、桶内有序的结构上，用二分回答「不超过某个时间戳的最近一条记录」。

## 题目

### 01 - 按时间戳检索历史版本 → LC-0981 Time Based Key-Value Store（P0）

**结构**：`Hash Map<key, List[(timestamp, value)]>`，每个 key 的列表按 timestamp 升序。

**决定性观察**：
1. 题目保证 `set` 的 timestamp **严格递增**，所以直接 `append` 就是有序的，
   **不需要插入排序，也不需要每次重新排序**。这是本题能做到 O(log n) 查询的前提。
2. `get(key, t)` 要的是「timestamp **不超过** t 的最大那条」
   ⟹ `Upper Bound(t) - 1` ⟹ Python 里就是 `bisect_right(timestamps, t) - 1`。
3. 返回 `-1`（即 `bisect_right` 返回 0）表示**所有记录都比 t 晚**，按题意返回 `""`。

```python
from bisect import bisect_right

class TimeMap:
    def __init__(self):
        self.store = defaultdict(list)          # key -> [(ts, val), ...] 按 ts 升序
    def set(self, key, value, timestamp):
        self.store[key].append((timestamp, value))   # 题目保证 ts 递增
    def get(self, key, timestamp):
        arr = self.store.get(key)
        if not arr: return ""
        i = bisect_right(arr, (timestamp, chr(127))) - 1   # 找 <= timestamp 的最后一条
        return arr[i][1] if i >= 0 else ""
```

**为什么用二分而不是线性扫描**：
`set` 和 `get` 各可能被调用 2×10⁵ 次。线性扫描是 O(n) 每次查询，
总共 O(n²) ≈ 4×10¹⁰，必然超时；二分是 O(log n)，总共 O(n log n)。

**bisect 用在元组上的坑**：
`bisect_right(arr, (t, ...))` 会按元组字典序比较。
如果直接写 `(timestamp,)`，它会和 `(timestamp, value)` 比较，
`(t,) < (t, 'anything')` 恒成立，于是等于 t 的那条**不会**被包含进左半 —— 结果错。
两个安全写法：
- 单独维护一个 `timestamps` 列表，对它做 `bisect_right(timestamps, t)`（最清楚）；
- 或者用一个比任何 value 都大的哨兵，如上面的 `chr(127)`。

**三种情况要处理**：
| 情况 | 返回 |
|---|---|
| key 不存在 | `""` |
| key 存在但所有 timestamp 都 > t | `""`（`i == -1`） |
| 正常 | 最后一条 `<= t` 的 value |

## 为什么这道题值得 P0
它把**哈希分桶 + 有序列表 + 二分**三件事组合在一起，
是「二分作为查询原语」最典型的面试案例，而且 NeetCode 150 / Top Interview 150 都收录。

## 跨专题
更多「设计题」在 [17-design (设计)](<../../17-design (设计)/>)；
本题因为核心是二分查询，主归属留在本专题。
