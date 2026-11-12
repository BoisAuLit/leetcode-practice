# Level 1 · 02 排列与重复元素去重 (Permutations)

## 核心定义
排列**关心顺序**，所以每个位置都可以从**全部**未使用的元素里挑 ——
这决定了它和组合类题的根本区别。

## 排列 vs 组合（一句话区别）

| | 组合（Level 1 `01`） | 排列（本章） |
|---|---|---|
| 关心顺序吗 | 不关心，`[1,2]` == `[2,1]` | 关心，`[1,2]` ≠ `[2,1]` |
| 怎么防重复选 | **`start` 参数** | **`used[]` 数组** |
| 循环范围 | `range(start, n)` | `range(0, n)` ← 每次都从头 |
| 答案个数 | C(n,k) / 2^n | n! |

**为什么排列不能用 `start`**：用了 `start` 就永远只能往后挑，
`[2,1]` 这种「后面的排在前面」的排列就被排除了。

## 模板
```python
def dfs(path):
    if len(path) == n:
        res.append(path[:]); return
    for i in range(n):
        if used[i]: continue
        if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
            continue                      # 去重，见下
        used[i] = True;  path.append(nums[i])
        dfs(path)
        path.pop();      used[i] = False  # 两个都要撤销
```

## LC-0047 的去重条件（本章唯一的难点）

```python
if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue
```

**前提：先排序**，让相同的值相邻。

三个条件的含义：
- `nums[i] == nums[i-1]`：当前值和前一个相同，可能产生重复排列。
- **`not used[i-1]`**：前一个**同值元素还没被用** ⟹ 说明我们正处在「同一层」，
  而前一个同值的分支已经在这一层试过了 ⟹ 跳过。
- 反过来，`used[i-1]` 为真时说明前一个同值元素在**当前路径上**（上一层用掉了），
  这时用当前这个是合法的 —— `[1,1]` 本身就是答案的一部分。

**写成 `used[i-1]`（不加 not）也能去重**，但那是「只保留逆序使用」的约定，
同样正确、效率略低。**关键是前后一致**，不要两种混用。

一句话记忆：
> **`not used[i-1]` ⟹ 同层去重；`used[i-1]` ⟹ 同路径允许重复。**

## 题目

| # | 题 | 优先级 | 关键点 |
|---|---|---|---|
| 01/01 | LC-0046 Permutations | **P0** | `used[]` + 每次从 0 开始；无重复值 |
| 01/02 | LC-0047 Permutations II | **P0** | 排序 + `not used[i-1]` 同层去重 |

## 另一种写法：交换法
```python
def dfs(i):
    if i == n: res.append(nums[:]); return
    for j in range(i, n):
        nums[i], nums[j] = nums[j], nums[i]
        dfs(i + 1)
        nums[i], nums[j] = nums[j], nums[i]   # 换回来
```
省掉 `used` 和 `path`，**但有重复元素时去重更难写**（交换会打乱排序）。
LC-0046 用它很漂亮，LC-0047 还是老实用 `used[]`。

## 复杂度
O(n! · n) 时间（n! 个排列，每个拷贝 O(n)），O(n) 递归栈。
**答案本身就有 n! 个**，所以这是下界。

## 常见错误
- 用了 `start` 参数 ⟹ 只能生成组合，不是排列。
- 撤销时只 `path.pop()` 忘了 `used[i] = False`。
- LC-0047 忘记先排序。
- LC-0047 的去重条件写成 `used[i-1]` 和 `not used[i-1]` 混用。
- `res.append(path)` 忘了拷贝。

## 复习时的 Pattern Recognition
> 「所有排列」「不同的顺序算不同方案」「全排列去重」
> → 用 `used[]`，不要用 `start`。有重复值就先排序 + `not used[i-1]`。
