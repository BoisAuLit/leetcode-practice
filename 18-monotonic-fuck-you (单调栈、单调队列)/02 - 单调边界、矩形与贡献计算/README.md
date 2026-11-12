# Level 1 · 02 单调边界、矩形与贡献计算

## 核心定义
对每个元素，求它作为**区间极值**时能统治的最大范围 `(left, right)`，
再把这个范围换算成面积、子数组个数或区间和。
这是单调栈从「找邻居」升级到「算价值」的一步，也是本专题性价比最高的一节。

## 决定性观察
1. **换枚举方向**：不要枚举区间再求极值（O(n²)），要枚举「每个元素当极值时覆盖哪些区间」。
2. 覆盖范围由两个边界夹出来：`left` = 左边第一个更小的，`right` = 右边第一个更小的，
   都是**开区间**端点。
3. 换算公式（必须分清用哪一个）：
   - 面积（LC-0084/0085）：`height * (right - left - 1)`
   - 子数组个数（LC-0907/2104）：`(i - left) * (right - i)` —— 起点 × 终点，两边独立相乘
   - 区间和（LC-1856）：`prefix[right] - prefix[left + 1]`

## Loop Invariant
单调**不减**的索引栈；栈里每个下标的左边界就是它在栈中的前一个元素。

## Push / Pop 规则
Pop 条件 `arr[stack[-1]] > cur`（**严格大于**）；末尾放一个 `-inf` / `0` 哨兵把栈清空。
弹出 j 时：`right = i`（当前下标），`left = 弹完之后的新栈顶`。

## 重复元素的 Tie Breaking（这一节最容易错的地方）
两边都用严格比较 ⟹ `[1,1]` 里两个 1 都认领整段 `[1,1]` ⟹ **重复计数**。
必须一边严格、一边非严格。本专题统一采用：

```
求 min 的贡献：left = Previous Strictly Smaller，right = Next Smaller **or Equal**
求 max 的贡献：left = Previous Strictly Greater，right = Next Greater **or Equal**
```

落到代码上就是：**严格大于才弹**（相等的留在栈里）。
直观解释：一串相等的元素中，只有**最左边那个**有权认领整串。

必验用例：`[1,1] → 3`、`[2,2,2] → 12`（LC-0907）。

## 典型模板
见根 README 的 Template 3（矩形）和 Template 4（贡献计数）。

## 题目

| # | 题 | 优先级 | 这道题独有的东西 |
|---|---|---|---|
| 01/01 | LC-0084 Largest Rectangle in Histogram | P0 | 边界法的原型；宽度 `right-left-1` 要减 1；哨兵简化收尾 |
| 01/02 | LC-0085 Maximal Rectangle | P2 | 唯一新东西是 **Matrix → 每行一个 Histogram**；遇 0 清零而不是减一 |
| 02/01 | LC-0907 Sum of Subarray Minimums | P1 | 贡献计数原型；**要对 1e9+7 取模** |
| 02/02 | LC-2104 Sum of Subarray Ranges | P1 | Σmax − Σmin 两套镜像边界；**不取模**；n≤1000 所以 O(n²) 也能过 |
| 02/03 | LC-1856 Max Subarray Min-Product | P2 | 宽度换成前缀和之差；**依赖元素全为正**；先比大小最后才取模 |

## 常见错误
- 宽度忘了减 1（`right - left` 而不是 `right - left - 1`）。
- 两边都用严格比较 → 重复元素重复计数。
- LC-0907 忘记取模；LC-2104 多此一举去取模。
- LC-1856 边算边取模再比大小 → 选错最大值。
- LC-0085 遇 '0' 写成 `heights[c] -= 1`。

## 复习时的 Pattern Recognition
> 「所有子数组的 min/max 之和」「最大矩形」「以某元素为最小值的最优区间」
> → 先求 Previous/Next Smaller 边界，再套换算公式。
