# Contribution Counting Cheat Sheet（贡献计数）

## 一句话
不要枚举「区间 → 它的极值」，要枚举「**元素 → 它统治了哪些区间**」。

## 公式

设 nums[i] 作为**最小值**时的统治范围是开区间 `(left, right)`：

```
起点可选 left+1 .. i      共 (i - left) 种
终点可选 i .. right-1     共 (right - i) 种
两边独立  ⇒  子数组个数 = (i - left) * (right - i)
```

| 目标 | 换算式 |
|---|---|
| 子数组个数 | `(i - left) * (right - i)` |
| Σ 子数组最小值 | `nums[i] * (i - left) * (right - i)` |
| 最大矩形面积 | `height * (right - left - 1)` |
| 区间和（元素为正） | `prefix[right] - prefix[left + 1]` |

注意**面积公式减 1，个数公式不减 1** —— 它们算的不是同一样东西：
面积要的是「中间有多少个格子」，个数要的是「左右各有多少种选法」。

## Tie Breaking（本仓库统一约定）

```
Σ min：left = Previous Strictly Smaller   right = Next Smaller **or Equal**
Σ max：left = Previous Strictly Greater   right = Next Greater **or Equal**
```

实现上只要记一句：**严格大于（求 min 时）才弹，相等的留在栈里**。
语义：一串相等的元素中，只有**最左边那个**有权认领整串。

反例：若两边都用严格比较，`[1,1]` 的两个 1 都会认领 `[1,1]`，答案从 3 变成 4。

## 一次扫描的标准实现

```python
total, stack = 0, []
for i in range(n + 1):
    cur = float('-inf') if i == n else arr[i]      # 末尾哨兵，清空栈
    while stack and arr[stack[-1]] > cur:          # 严格大于才弹
        j = stack.pop()
        left = stack[-1] if stack else -1          # 弹完后的新栈顶 = 左边界
        total += arr[j] * (j - left) * (i - j)     # 右边界就是 i
    stack.append(i)
```

## 取模（两题要求不同，别搞混）
- **LC-0907 要对 1e9+7 取模。**
- **LC-2104 不取模。**
- LC-1856 取模，但必须**先在未取模的数上比出最大值，最后才取模**。

## 用这个模板的题
LC-0907（Σmin）、LC-2104（Σmax − Σmin）、LC-1856（换成区间和）、
LC-0084 / LC-0085（换成面积）。
