# 12-dynamic-programming 重构审计报告

## 原始文件保留
迁移前 261 个文件（不含 `.DS_Store`）。SHA-256 逐个比对：
- **259 个逐字节未变**
- **2 个有意变更**：
  - `LC-1048 Longest String Chain/solution.py` —— 修掉一行孤立的 `&`（见下）
  - `LC-0494 Target Sum/solution.py` —— 追加了三级演进解法（见下）

## 修复的已有问题
**LC-1048 原本跑不起来**：文件里有一行孤立的 `&`（手误留下的字符）
⟹ 整个文件 `SyntaxError`。已删除那一行并注明原因，**没有改动任何解法代码**。

迁移前基线：59 通过 / 1 失败。迁移后：**73 / 73 全部通过**。

## LC-0494 的跨专题合并
处理 10-backtracking 时我在那里新建了 LC-0494（作为「回溯 vs DP 的边界」示例），
随后全仓库查重发现**本专题的 0-1 背包目录早就有这道题**。
已按「一道题只能有一个实体目录」处理：
- 把「01 背包 → 记忆化 → 朴素回溯」三级演进解法和随机对拍**并入本专题这份 solution.py**
  （用户原有实现一字未改，保留在前面）；
- 删除 10-backtracking 的重复目录，那里的 `05/01` 改为索引 README。

## NC 处理
**12 个 NC 来源全部是孤儿**（仓库里没有对应 LC 目录），按规则**升格**：

| 原 NC | 升格为 | practice |
|---|---|---|
| NC - Climbing Stairs | LC-0070 | 0 |
| NC - House Robber | LC-0198 | 0 |
| NC - House Robber II | LC-0213 | 0 |
| NC - Min Cost Climbing Stairs | LC-0746 | 0 |
| NC - Maximum Product Subarray | LC-0152 | 0 |
| NC - Partition Equal Subset Sum | LC-0416 | 0 |
| NC - Longest Increasing Subsequence | LC-0300 | 0 |
| NC - Decode Ways | LC-0091 | 0 |
| NC - Longest Common Subsequence | LC-1143 | 0 |
| NC - Distinct Subsequences | LC-0115 | **4 条** |
| NC - Edit Distance | LC-0072 | **1 条** |
| NC - Burst Balloons | LC-0312 | 0 |

**没有 LC / NC 重复，因此没有删除任何目录。**

## 新增题目（13 道，均含 metadata.json + problem.pdf + problem_dark.pdf）

**第一轮 12 道**：LC-0120、LC-0122、LC-0123、LC-0474、LC-1049、LC-0516、LC-0673、
LC-0044、LC-0174、LC-0354、LC-1547、LC-0879

**第二轮自主新增 1 道**：LC-1312

每道都带 2–3 种解法 + 随机对拍。几个值得一提的：
- LC-0044：**3000 组**随机对拍（DP / 贪心双指针 / 记忆化三方一致）
- LC-0174：和「二分答案 + 正向验证」对拍，同时说明了**为什么正推不行**
- LC-0354：600 组专压「同宽不同高」的陷阱
- LC-0673：1000 组小值域，专压「同长度多条路径」
- LC-1312：短串用**真插字符的 BFS** 验证「n − LPS」这个结论
- LC-1547：和「枚举所有切割顺序」的全排列暴力对拍

**执行中发现并修正的两处我自己的错误**（如实记录）：
- LC-0174 我写的期望值 4 是错的，三个解法一致给出 3（手算确认 3 正确）
- LC-1547 我写的期望值 14 是错的，正确是 19（两种切法都是 10 + 9）

## 第一轮候选里**没有**新建的 3 道（已在别处）
| LC | 实体目录在哪 | 原因 |
|---|---|---|
| LC-0647 / LC-0005 回文子串 | 02-two-pointers | 中心扩展是 O(1) 空间的更优解；本专题的 LC-0516 已覆盖「回文 + 区间 DP」 |
| LC-0337 House Robber III | 07-trees | 它是**树形** DP，归在树专题更准确 |

## 校验结果
- 原始文件：261 个，**259 逐字节一致 + 2 个已说明的有意变更**
- README 相对链接：**死链 0**
- `solution.py` 运行：**73 / 73 通过**（迁移前 59/60）
- Level 1 / 2 / 3 编号连续
- 写入范围：全部在 `12-dynamic-programming (动态规划)/` 之内
  （唯一例外是上面说明的 LC-0494 跨专题去重）
- 未执行 `git add` / `commit` / `push`；未使用 `rm -rf`
