# 05-binary-search 重构审计报告

## 原始文件保留
迁移前 105 个普通文件 + 1 个符号链接。SHA-256 逐个比对：

- **103 / 105 逐字节未变**
- **2 个有意变更**（都有留档，没有丢失任何逻辑）：
  1. `NC - Median of Two Sorted Arrays/solution.py` → `01 - LC-0004 - .../solution.py`
     加了标题注释与 `##### ! Solution 1` 横幅，类名 `Solution` → `Solution_1`，
     并追加了一个 O(m+n) 的对拍基准 `Solution_2`。
     **用户原有的 `findMedianSortedArrays` 方法体一字未改。**
  2. `LC-0162 - Find Peak Element/solution.py` —— 见下面「修复的已有问题」。
- `metadata.json` 的 `path` 字段由 `tools/update_path.sh` 按设计更新，不计入内容变更。

## 符号链接
```
_resources/templates/02 - 2616 - Min the Max Diff of Pairs.py
  -> /Users/bohaoli/.../leetcode-practice/greedy/003 - 2616 - A - (M) - Min the Max Diff of Pairs.py
```
**目标不存在（失效链接）** —— `greedy/` 目录在更早的重构中已改名为 `13-greedy (贪心)`。
按要求：使用 `mv` 整体搬迁，**没有解引用、没有跟随链接写入外部、没有自动修复**。
用 `ls -l` 确认搬迁后它仍然是一个 symlink 而不是普通文件。
要修复的话，正确目标应该是 13-greedy 下对应的 LC-2616 资料，但**本次不动**。

## 修复的已有问题（两处真实 bug）

### 1. LC-0367 的 metadata 链接指错题
```
before: https://leetcode.com/problems/minimize-the-maximum-difference-of-pairs/   ← 这是 LC-2616
after : https://leetcode.com/problems/valid-perfect-square/
```

### 2. LC-0162 的 solution.py 无法运行
原文件是一次自动合并的产物，文件头自己写着「⚠️ 自动合并失败 … 需要手工整理」。
里面有一段**残缺的驱动代码**：
```python
input_ =                      # 等号后面没有值
result = s.XXXXXXXXXXXXX(input_)   # 占位的方法名
```
导致整个文件 `SyntaxError`，根本跑不起来。另外文件里有**三个重名的 `class Solution`**，
其中第二段和第三段（标为 "BST" 和 "Linear Scan"）**内容完全相同**。

处理方式：
- 两段不同的实现保留为 `Solution_1`（二分）和 `Solution_2`（线性扫描），**函数体一字未改**；
- 内容完全相同的那两段合并为一个，避免无意义重复；
- 只删除了无法运行的占位驱动代码，补上可运行的随机对拍；
- **整理前的原文件已原样留档为 `solution.py.orig-broken.txt`**。

## NC / LC 重复题
instructions.md 列出的 4 组 NC/LC 重复
（Koko、Time Based Key-Value Store、Find Minimum in Rotated、Search in Rotated）
**在本次执行时已经不存在** —— 更早一轮的 NC 清理已按「只保留 LeetCode 版」处理完毕。
现存的 LC-0875 / LC-0981 / LC-0153 / LC-0033 就是保留下来的 LeetCode 版本。
因此本次**不需要**新建 `_neetcode/`，这也符合仓库现行规则。

唯一剩下的 `NC - Median of Two Sorted Arrays` 没有 LC 对应目录，
属于「孤儿 NC」，按规则**升格**为 `LC-0004 - Median of Two Sorted Arrays`
（`id` 由 `NC-median-of-two-sorted-arrays` 改为 `LC-0004`，`practice` 原为空，无记录损失）。

## 新增题目（10 道，均含 metadata.json + problem.pdf + problem_dark.pdf）
- 第一轮 7 道：LC-0074、LC-1011、LC-1482、LC-0410、LC-1283、LC-1552、LC-0658
- 第二轮自主新增 3 道：LC-0081、LC-0275、LC-0378

每道新增题的 `solution.py` 都包含 2–3 种解法、完整的不变量讲解，
并在文件末尾用**随机对拍**（对照暴力枚举或独立算法）验证正确性，
覆盖了重复元素、空输入、无解、边界等场景。

## 资源目录
`00-Theory/`（3 个文件）和 `templates (模板)/`（9 个文件，含 1 个符号链接）
整体搬到 `_resources/` 下，**内容全部未改**，Template 1/2/3 与两个 bisect 示例都在。

## 校验结果
- 原始文件：105 个普通文件，**103 逐字节一致 + 2 个已说明的有意整理**
- 符号链接：1 个，**保持未解引用**
- README 相对链接：**死链 0**
- `solution.py` 运行：**30 / 30 通过**（修复 LC-0162 之前是 29/30）
- Level 1 / 2 / 3 编号连续
- 写入范围：全部在 `05-binary-search (二分查找)/` 之内
- 未执行 `git add` / `commit` / `push`；未使用 `rm -rf`
