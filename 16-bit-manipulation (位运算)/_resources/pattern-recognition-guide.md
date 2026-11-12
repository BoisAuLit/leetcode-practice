# Bit Manipulation Pattern Recognition Guide（题型识别指南）

> 位运算题的识别很直接：**看题目在问「位」的什么**。
> 这些提示**不互斥** —— LC-0260 = Q3 + Q5，LC-0421 = Q3 + Trie。

---

## 决策树

### Q1：要数一个数里有几个 1？
→ **Popcount**。`x &= x - 1` 循环（O(popcount)）或 `bin(x).count('1')`。
📍 [LC-0191 Number of 1 Bits](<../01 - 二进制基础、位计数与位反转/01 - Popcount 与最低有效置位/01 - LC-0191 - Number of 1 Bits>)

### Q2：要算 `0..n` **每个数**的 1 的个数？
→ **Counting Bits DP**。`dp[i] = dp[i>>1] + (i&1)`，一遍 O(n)。
📍 [LC-0338 Counting Bits](<../01 - 二进制基础、位计数与位反转/01 - Popcount 与最低有效置位/03 - LC-0338 - Counting Bits>)

### Q3：有元素「成对出现」，要找出不成对的？
→ **XOR Cancellation（抵消）**。`x ^ x == 0`。
- **1 个**异常 ⟹ 一次全体 XOR 就够
- **2 个**异常 ⟹ 全体 XOR 得 `a^b`，**再用最低位 1 分组**
📍 [LC-0136](<../02 - XOR 不变量与二进制算术/01 - XOR 抵消与缺失元素/01 - LC-0136 - Single Number>)、
[LC-0268](<../02 - XOR 不变量与二进制算术/01 - XOR 抵消与缺失元素/02 - LC-0268 - Missing Number>)、
[LC-0260](<../02 - XOR 不变量与二进制算术/01 - XOR 抵消与缺失元素/03 - LC-0260 - Single Number III>)

### Q4：判断是不是 2 的幂？
→ **`x > 0 and x & (x - 1) == 0`**。⚠️ `x > 0` 不能省。
📍 [LC-0231 Power of Two](<../01 - 二进制基础、位计数与位反转/01 - Popcount 与最低有效置位/02 - LC-0231 - Power of Two>)

### Q5：需要「只保留最低位的 1」来做区分 / 分组？
→ **`x & (-x)`**（lowbit）。
⚠️ 和 `x & (x-1)`（**清掉**最低位 1）是两回事。
📍 LC-0260（区分位分组）

### Q6：要反转一个**固定宽度**的二进制数？
→ **Fixed-width Reverse**。循环**恰好 32 次**，不要用 `while n`
（前导零也是有效位）。
📍 [LC-0190 Reverse Bits](<../01 - 二进制基础、位计数与位反转/02 - 固定宽度位读取与反转/01 - LC-0190 - Reverse Bits>)

### Q7：不让用 `+` / `-` 做加法？
→ **XOR + AND 半加器**：`a^b` 是无进位和，`(a&b)<<1` 是进位，迭代到进位为 0。
⚠️ **Python 必须加 32 位 MASK，否则负数死循环。**
📍 [LC-0371 Sum of Two Integers](<../02 - XOR 不变量与二进制算术/02 - XOR 与 AND 形成二进制加法/01 - LC-0371 - Sum of Two Integers>)

### Q8：求一个**区间内所有整数**的 AND？
→ **公共高位前缀**：同时右移两端点直到相等，再左移回去。
⚠️ **AND 的规律不能迁移到 OR / XOR。**
📍 [LC-0201 Bitwise AND of Numbers Range](<../02 - XOR 不变量与二进制算术/03 - Range AND 与共同高位前缀/01 - LC-0201 - Bitwise AND of Numbers Range>)

### Q9：要枚举**所有子数组**的 OR / AND？
→ **Bitwise Aggregation**。关键观察：以每个右端点结尾的
「不同 OR 值」个数是 **O(32)**（因为 OR 单调递增且只有 32 位可变）
⟹ 用一个小集合滚动，总复杂度 O(32n)。
📍 [LC-0898 Bitwise ORs of Subarrays](<../03 - Bitwise Subarray 与位聚合/01 - 子数组 OR 状态与按位贡献/01 - LC-0898 - Bitwise ORs of Subarrays>)、
[LC-2411](<../03 - Bitwise Subarray 与位聚合/01 - 子数组 OR 状态与按位贡献/02 - LC-2411 - Smallest Subarrays With Maximum Bitwise OR>)

### Q10：要最大 Bitwise AND 的**最长子数组**？
→ 关键观察：**AND 只会让值变小** ⟹ 最大 AND 就是数组的**最大值本身**
⟹ 退化成「求最大值的最长连续段」。
📍 [LC-2419 Longest Subarray With Maximum Bitwise AND](<../03 - Bitwise Subarray 与位聚合/02 - 最大 Bitwise AND 与连续区间/01 - LC-2419 - Longest Subarray With Maximum Bitwise AND>)

### Q11：要把一个数**分解成 2 的幂**之和？
→ **Binary Decomposition**。逐位取出 `1 << i`。
📍 [LC-2438 Range Product Queries of Powers](<../04 - 二进制分解与原地编码/01 - Powers of Two 与范围乘积/01 - LC-2438 - Range Product Queries of Powers>)

### Q12：要**原地**改数组，但新值依赖旧值？
→ **In-place Encoding**：把新旧两个值塞进同一个数的高低位
（`x = old + new * K`，取旧值 `x % K`，取新值 `x // K`），
最后再统一除出来。
📍 [LC-1470 Shuffle the Array](<../04 - 二进制分解与原地编码/02 - In-place 编码与旧状态保护/01 - LC-1470 - Shuffle the Array>)、
[LC-1920 Build Array from Permutation](<../04 - 二进制分解与原地编码/02 - In-place 编码与旧状态保护/02 - LC-1920 - Build Array from Permutation>)

### Q13：要判断两个集合**是否相交**（元素种类 ≤ 32/64）？
→ **Bitmask 表示集合**，一次 `a & b == 0` 搞定（把 O(L) 压到 O(1)）。
📍 [LC-0318 Maximum Product of Word Lengths](<../04 - 二进制分解与原地编码/03 - Bitmask 表示集合/01 - LC-0318 - Maximum Product of Word Lengths>)

### Q14：要枚举一个集合的**所有子集**？
→ **Bitmask Enumeration**：`for mask in range(1 << n)`。
⚠️ 无法剪枝，`n <= 20` 才可行；要剪枝就用回溯。
📍 [LC-0078 Subsets](<../05 - 跨专题与低优先级存档/04 - 跨专题索引/02 - LC-0078 - Subsets (学习索引 · 实体在 10-backtracking)>) ↗️

### Q15：要在数组里找**最大的 XOR 对**？
→ **高位优先贪心** + Binary Trie 或逐位 Hash Set。
用 `a ^ b == c ⟺ a == c ^ b` 把配对变成一次查询。
📍 [LC-0421 Maximum XOR of Two Numbers](<../05 - 跨专题与低优先级存档/04 - 跨专题索引/01 - LC-0421 - Maximum XOR of Two Numbers in an Array (学习索引 · 实体在 08-tries)>) ↗️

### Q16：输入里有**负数**，或代码里有 `<<` 且会迭代？
→ ⚠️ **先想 Python 的无限位补码**。加 `MASK = 0xFFFFFFFF`。
这一条**每道位运算题都要问**。
📍 见 [位运算恒等式速查表 · 第九节](<./bit-tricks-cheat-sheet.md>)

---

## 三秒速判表

| 题干关键词 | Pattern |
|---|---|
| number of 1 bits / hamming weight | Popcount |
| for every i in 0..n, count bits | Counting Bits DP |
| appears twice except one / missing number | XOR Cancellation |
| exactly two elements appear once | XOR + **lowbit 分组** |
| power of two / power of four | `x & (x-1) == 0` |
| reverse bits (32-bit) | Fixed-width Reverse |
| without using + or - | XOR/AND 半加器 + **MASK** |
| bitwise AND of range [left, right] | **公共高位前缀** |
| all subarrays' OR / AND | Bitwise Aggregation（O(32) 状态） |
| longest subarray with max AND | **最大值的最长连续段** |
| sum of powers of two | Binary Decomposition |
| in-place, O(1) extra space, nums[i] = nums[nums[i]] | In-place Encoding |
| no common letters / disjoint sets | **Bitmask `a & b == 0`** |
| all subsets / all combinations (n ≤ 20) | Bitmask Enumeration |
| maximum XOR of two numbers | 高位贪心 + Trie / Hash Set |

---

## 读位运算题时的三问

1. **输入会是负数吗？代码里有 `<<` 吗？**
   → 有任一个 ⟹ Python 需要 `MASK = 0xFFFFFFFF`，否则可能死循环。
2. **宽度是题目给定的吗？**
   → 是（如「32 位无符号」）⟹ 循环**固定次数**，前导零也算有效位。
3. **我要的是「这一位」还是「这个数」？**
   → 很多题（LC-0201、LC-0898、LC-0421）的解法是**逐位独立考虑**，
     而不是整体考虑数值。**换到位的视角**往往是突破口。

---

## 本专题刻意不做的（Future Candidates）

按指令要求**不主动扩充**：
- ❌ **Gray Code 全套变体**
- ❌ **Advanced Bitmask DP**（状压 DP 全家族）
- ❌ **SOS DP**（Sum over Subsets）

这些要么学习成本远超迁移收益，要么属于竞赛范畴。
LC-0318 和 LC-0078 把「Bitmask 当集合」的概念打通就够了。
