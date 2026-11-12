# 08-tries 重构审计报告

## 原始文件保留
迁移前 47 个文件（不含 `.DS_Store`）。SHA-256 逐个比对：
**47 / 47 全部逐字节未变** —— 没有任何 solution.py、PDF、图片被修改。
（`metadata.json` 的 `path` 由 `update_path.sh` 按设计更新，`id` 对 3 个 NC 做了升格，见下。）

## NC 处理
3 个 NC 来源**全部是孤儿**（仓库里没有对应 LC 目录），按规则**升格**：

| 原 NC | 升格为 | id 变更 | practice |
|---|---|---|---|
| NC - Implement Trie (Prefix Tree) | LC-0208 | `NC-implement-prefix-tree` → `LC-0208` | 0 条 |
| NC - Design Add and Search Word Data Structure | LC-0211 | `NC-design-word-search-data-structure` → `LC-0211` | 0 条 |
| NC - Word Search II | LC-0212 | `NC-search-for-word-ii` → `LC-0212` | 0 条 |

**没有 LC / NC 重复，因此没有删除任何目录。**

## 新增题目（5 道，均含 metadata.json + problem.pdf + problem_dark.pdf）
- 第一轮 3 道：LC-0648、LC-2416、LC-0421
- 第二轮自主新增 2 道：LC-1032、LC-0720

每道都带 2–3 种解法和随机对拍：
- LC-0648 验证「取的确实是最短词根」
- LC-2416 含重复单词的对拍
- LC-0421 三方对拍（Bitwise Trie / 逐位贪心 / 暴力）
- LC-1032 500 组 × 40 次 query 对拍
- LC-0720 验证「同长度取字典序最小」

## 未处理的 LC / LC 重复（已登记，待指令）
| LC | 位置 |
|---|---|
| LC-0014 | 本专题 + `99-advanced (进阶专题)/divide-and-conquer (分治)/` |
| LC-3291 | 本专题 + `12-dynamic-programming` + `13-greedy/jump-game/Jump Game II - Cluster` |

这两组是 **LC / LC** 重复（不是 NC/LC），属于用户之前交代「待明确指令再清理」的那批，
本次**没有删除任何一份**。

## 资源目录
`docs (资料)/Trie.png` → `_resources/docs/`；`utils/TrieUtils.py` → `_resources/utils/`。内容未改。

## 校验结果
- 原始文件：**47 / 47 逐字节一致**
- README 相对链接：**死链 0**
- `solution.py` 运行：**14 / 14 通过**（迁移前 9/9，新增 5 道全部通过）
- Level 1 / 2 / 3 编号连续
- 写入范围：全部在 `08-tries (字典树、前缀树)/` 之内
- 未执行 `git add` / `commit` / `push`；未使用 `rm -rf`
