# 18-monotonic 重构审计报告

## 原始文件保留
迁移前 48 个文件（不含 .DS_Store）。逐个 SHA-256 比对结果：

- **47 个内容逐字节未变**（含全部 PDF、图解、note.md、questions_about_monotonic.md、
  以及所有原始 solution.py）。
- **1 个有意变更**：`LC-2104 - Sum of Subarray Ranges/solution.py`。
  原文件只有一个**空的 `class Solution`**（没有函数体，本身是语法错误、无法运行），
  属于占位而非实现。原始内容已完整留档于
  [original-LC-2104-solution.py.txt](<original-LC-2104-solution.py.txt>)。
- `metadata.json` 的 `path` 字段由 `tools/update_path.sh` 按设计改写，不计入"内容变更"。

## 特别保护的资料（全部确认在位）
| 文件 | 现在的位置 |
|---|---|
| `questions_about_monotonic.md` | 专题根目录，**未作任何修改** |
| `asset-Scan 15.jpeg` | `05/01/01 - LC-0853 - Car Fleet/` |
| `asset-explanation-1.jpeg`、`asset-explanation-2-claude.jpg`、`note.md` | `02/01/01 - LC-0084 - Largest Rectangle in Histogram/` |
| `note.md`（Gas Station） | `05/03/01 - LC-0134 - Gas Station/` |
| `note.md`（Sliding Window Maximum） | `04/01/01 - LC-0239 - Sliding Window Maximum/` |

## NC → LC 正式化（保留 practice 复习记录，未使用 --force）
| 原目录 | 新目录 | id 变更 | practice |
|---|---|---|---|
| `NC - Largest Rectangle In Histogram` | `02/01/01 - LC-0084 - …` | `NC-largest-rectangle-in-histogram` → `LC-0084` | 保留 2 条 |
| `NC - Car Fleet` | `05/01/01 - LC-0853 - Car Fleet` | `NC-car-fleet` → `LC-0853` | 0 条 |
| `NC - Gas Station` | `05/03/01 - LC-0134 - Gas Station` | `NC-gas-station` → `LC-0134` | 保留 2 条 |

三者都**没有** NC/LC 重复（仓库里不存在对应的 LC 实体目录），因此是「升格」而不是「删除」。

## 新增题目（7 道，全部带 metadata.json + problem.pdf + problem_dark.pdf）
第一轮：LC-0503、LC-0901、LC-0907、LC-0085（LC-1438 / LC-0862 已在 03-sliding-window，只建索引）
第二轮：LC-0456、LC-1673、LC-1856

## 校验结果
- 原始文件保留：47/48 逐字节一致，1 个为上述有意补全
- README 相对链接：25 条，**死链 0**
- `solution.py` 运行：**17/17 通过**（每个新增题目都带随机对拍，覆盖重复元素边界）
- Level 1 / 2 / 3 编号：连续，无缺号
- 写入范围：全部在本专题目录内
- 未执行任何 `git add` / `commit` / `push`；未使用 `rm -rf`
