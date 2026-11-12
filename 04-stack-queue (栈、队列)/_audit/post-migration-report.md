# 04-stack-queue 重构审计报告

## 原始文件保留
迁移前 89 个文件（不含 `.DS_Store`）。SHA-256 逐个比对：

**89 / 89 全部逐字节未变** —— 没有任何 `solution.py`、`note.md`、图片或 PDF 被覆盖或改写。
（`metadata.json` 的 `path` 字段由 `tools/update_path.sh` 按设计更新，不算内容变更；
本次校验把它们按「文件仍在」核对，结果同样全部在位。）

特别保护的资料：

| 文件 | 现在的位置 |
|---|---|
| `asset-explanation-claude.png`、`asset-explanation.jpeg` | `01/01/03 - LC-0032 - Longest Valid Parentheses/` |
| `note.md` | `03/02/01 - LC-0227 - Basic Calculator II/` |
| `note.md` | `03/03/01 - LC-0394 - Decode String/` |

## NC / LC 重复题
instructions.md 提到的 `NC - Evaluate Reverse Polish Notation` 和 `NC - Min Stack`
**在本次执行时已经不存在**（更早一轮的 NC 清理已经按「只保留 LeetCode 版」处理掉了）。
现存的 LC-0150 和 LC-0155 就是保留下来的 LeetCode 版本，资料完整。
因此本次没有需要新建 `_neetcode/` 的情形 —— 这也符合仓库现行规则：
**LC / NC 重复时只保留 LeetCode 版**。

## 跨专题去重
| 题 | 处理 |
|---|---|
| LC-0286 Walls and Gates | 11-graphs 的版本更完整（79 行 + 完整讲解 vs 31 行），两边 `practice` 均为空。本专题的副本**无损归档**到 `_cross_topic_archive/0286 - Walls and Gates (04 旧版本，正式目录在 11-graphs)`，目录名刻意不匹配 `LC-xxxx - ` 前缀，避免复习队列重复。文件一个没删。 |
| LC-0032 | 12-dynamic-programming 另有一份副本（不同的附件、DP 解法）。本专题这份有复习记录（1 条 🔴）且 instructions 指定本专题讲 Stack 版，故保留为主目录；两份的最终归并留待 12 专题重构时一并处理。 |
| 单调栈 / 单调队列全部题目 | 按仓库铁律归 18-monotonic，本专题 Level 1 `02` / `05` 只建索引 README，不建题目文件夹。 |
| LC-0994 / LC-0752 | 11-graphs 已有 ★ 签名题目录，只建索引。 |

## 新增题目（5 道，均含 metadata.json + problem.pdf + problem_dark.pdf）
- 第一轮：LC-0735、LC-0946、LC-0232
- 第二轮自主新增：LC-1544、LC-0649

第一轮推荐的 12 道里，另外 9 道（0496、0739、0503、0901、0084、0907、0853、0402、0862）
**全部属于单调栈 / 单调队列**，按铁律归 18-monotonic，已在那里实际创建或已存在，
本专题通过 Level 1 `02` / `05` 的索引 README 纳入学习路线。

## 校验结果
- 原始文件：**89 / 89 保留**
- README 相对链接：38 条，**死链 0**
- `solution.py` 运行：**26 / 26 通过**（含归档那份；每个新增题目都带随机对拍）
- Level 1 / 2 / 3 编号连续，无缺号
- 写入范围：全部在 `04-stack-queue (栈、队列)/` 之内
- 未执行 `git add` / `commit` / `push`；未使用 `rm -rf`

## 发现并修正的问题
- LC-0649 的暴力对照实现最初把「本轮发言后才被禁」的议员错误地留到了下一轮，
  导致和正解不一致。已修正为**轮末统一结算**，三个解法现已完全一致（随机对拍 300 组）。
