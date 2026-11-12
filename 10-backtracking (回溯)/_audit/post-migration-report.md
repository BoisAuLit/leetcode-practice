# 10-backtracking 重构审计报告

## 原始文件保留
迁移前 68 个文件（不含 `.DS_Store`）。SHA-256 逐个比对：
- **67 个逐字节未变**
- **1 个有意修复**：`LC-0039 Combination Sum` 的 solution.py（见下）

## 修复的已有问题
**LC-0039 Combination Sum 原本跑不起来**：文件底部写的是
```python
result = s.combinationSum(input_)      # 少传了 target
```
⟹ `TypeError: combinationSum() missing 1 required positional argument: 'target'`。
已补上 `target = 9` 并注明原因，**没有改动任何解法代码**。

迁移前基线：14 通过 / 1 失败。迁移后：**20 / 20 全部通过**。

## NC 处理
**10 个 NC 来源全部是孤儿**（仓库里没有对应 LC 目录），按规则**升格**：

| 原 NC | 升格为 | id 变更 | practice |
|---|---|---|---|
| NC - Subsets | LC-0078 | `NC-subsets` | 0 |
| NC - Subsets II | LC-0090 | `NC-subsets-ii` | 0 |
| NC - Combination Sum | LC-0039 | `NC-combination-target-sum` | 0 |
| NC - Combination Sum II | LC-0040 | `NC-combination-target-sum-ii` | 0 |
| NC - Permutations | LC-0046 | `NC-permutations` | 0 |
| NC - Letter Combinations of a Phone Number | LC-0017 | `NC-combinations-of-a-phone-number` | **1 条** |
| NC - Generate Parentheses | LC-0022 | `NC-generate-parentheses` | **1 条** |
| NC - Palindrome Partitioning | LC-0131 | `NC-palindrome-partitioning` | 0 |
| NC - Word Search | LC-0079 | `NC-search-for-word` | 0 |
| NC - N-Queens | LC-0051 | `NC-n-queens` | 0 |

**没有 LC / NC 重复，因此没有删除任何目录。**

## 新增题目（5 道，均含 metadata.json + problem.pdf + problem_dark.pdf）
- **第一轮 2 道**：LC-0093、LC-0698
- **第二轮自主新增 3 道**：LC-0491、LC-0980、LC-0494
  （**LC-0494 后来发现 12-dynamic-programming 的 0-1 背包目录早就有这道题**，
   已按「一道题只能有一个实体目录」把三级演进解法并入那份 solution.py，
   本专题的 `05/01` 改为索引 README）

每道都带 2–3 种解法 + 随机对拍：
- LC-0093：2000 组随机数字串，专压**前导零**
- LC-0698：600 组三方对拍（剪枝回溯 / 状压 DP / 朴素回溯）
- LC-0491：1000 组小值域随机，验证「每层 set 去重 == 全枚举后去重」
- LC-0980：300 组随机网格，**额外校验原地标记完全回溯**（网格恢复原样）
- LC-0494：1000 组三方对拍（01 背包 / 记忆化 / 朴素回溯），含 0 和负 target

## 结构说明
为 LC-0494 **新开了 Level 1 `05 - 回溯与记忆化的边界`**。
理由：本专题前四章都是「必须列出所有方案 ⟹ 只能回溯」的题，
而「什么时候该停止回溯、改用 DP」是这个专题最该想清楚、却最容易被忽略的问题。
给它一个独立的 Level 1 而不是塞进别处，是为了让这条分界线在目录结构上就看得见。

## 校验结果
- 原始文件：68 个，**67 逐字节一致 + 1 个已说明的修复**
- README 相对链接：**死链 0**
- `solution.py` 运行：**20 / 20 通过**（迁移前 14/15）
- Level 1 / 2 / 3 编号连续
- 写入范围：全部在 `10-backtracking (回溯)/` 之内
- 未执行 `git add` / `commit` / `push`；未使用 `rm -rf`
