# 13-greedy 重构审计报告

## 原始文件保留
迁移前 105 个文件（不含 `.DS_Store`）。SHA-256 逐个比对：
- **103 个逐字节未变**
- **2 个有意变更**（都是修 bug，见下）

## 修复的两个真实 bug（都在原有代码里）

### ① `jump-game/LC-0045 - Jump Game II` —— **死循环**
```python
farthest = max(farthest, nums[i])        # ✗ 少加了 i
farthest = max(farthest, i + nums[i])    # ✓
```
`nums[i]` 是「能跳多远」，`i + nums[i]` 才是「能跳到哪个下标」。
写错之后 `r` 不保证前进，`[2,3,0,1,4]` 直接**无限循环**。

**这是本次重构中唯一一个会让检查流程卡死的 bug** ——
它也暴露了我的检查脚本的一个问题：macOS 没有 `timeout` 命令，
所以之前的全量运行会被它卡住。已改用 Python 的
`subprocess.run(timeout=...)`（`scratchpad/runall.py`）。

### ② `Jump Game II - Cluster/LC-0045` 的 `Solution_1` —— 解包错误
```python
curr_end, curr_far = 0        # ✗ ValueError: cannot unpack non-sequence int
curr_end = curr_far = 0       # ✓
```
这个 bug 不会让文件跑不起来（因为文件底部用的是 `Solution_3`），
但 `Solution_1` 一调用就报错。两处都已修正并加注释。

迁移前基线：**21 通过 / 1 卡死**。迁移后：**26 / 26 全部通过**。

## 解决的三组重复（都在用户的待办清单上）

### ① LC-0045 —— 两份合一
| | |
|---|---|
| 正式位置 | `01 - 跳跃…/02 - 最少跳跃与最远覆盖/01 - LC-0045 - Jump Game II`（instructions 指定） |
| 归档 | `06/03/变体 · LC-0045 - Jump Game II (Cluster 版，含 DP 与记忆化)` |
| 处理 | Cluster 版的三种解法（贪心 / 记忆化 / DP）**全部并入正式位置**；归档目录改名后不再匹配题目前缀 ⟹ 不进复习队列；**文件一个没删** |

### ② LC-3291 —— 三份合一
原来有三份：本专题 Cluster、12-DP、08-tries。
**正式位置选 08-tries**，理由很实在：那份有用户写的 `note.md`、一张讲解图、
以及 **4 条复习记录**（🔴🔴🔴🟡）；另两份 `practice` 都是空的。
**删富的留穷的会丢掉真实学习数据。**
- 12-DP 那份的实现已并入 08-tries（类名加 `_DP` 后缀），目录删除，改为索引 README。
- 本专题 Cluster 那份归档为 `06/03/变体 · …`。

### ③ LC-0134 Gas Station —— 从 18-monotonic 搬到这里
原来在 `18-monotonic/05 - 单调扫描与跨专题存档/03 - Greedy 跨专题来源存档/`，
那里的 README 当时就写明「若日后 greedy 专题要收这道题，应当整体搬过去」。
本专题 instructions 把它列在 `02/01` ⟹ **整体搬过来**，
`practice`（2 条）和 `note.md` 一起跟过来；18 那边的空目录已清理，README 已更新。

## 另外两组本次也顺手解决的重复

| LC | 处理 |
|---|---|
| **LC-0881** | 新建时发现 02-two-pointers 早就有 ⟹ 补充解法并入那份，本专题改索引 |
| **LC-0032** | 04-stack-queue（栈版，有 2 张图 + 1 条复习记录）为正式位置；12-DP 那份的 DP 实现已并入 04，目录归档为「变体 · …」 |

**全仓库 LC/LC 重复组：重构前 12 组 → 现在 1 组**（只剩 LC-0014，见下）。

## 仍未处理的 1 组（需要你的指令）
**LC-0014 Longest Common Prefix**：
`99-advanced (进阶专题)/divide-and-conquer (分治)/` 和
`08-tries/05 - 进阶变体与跨专题存档/02 - Common Prefix 的非 Trie 主流解法/` 各有一份。
**没有动**，因为 `99-advanced` 没有 instructions.md ——
本次只执行了 04–18 这 15 个专题的指令，动它超出给定范围。

## NC 处理
**4 个 NC 来源全部是孤儿**，按规则**升格**：

| 原 NC | 升格为 | practice | 备注 |
|---|---|---|---|
| NC - Merge Triplets to Form Target | LC-1899 | 0 | 另外补上了 metadata 里缺失的 leetcode 链接 |
| NC - Hand of Straights | LC-0846 | 0 | |
| NC - Partition Labels | LC-0763 | 0 | |
| NC - Valid Parenthesis String | LC-0678 | **1 条** | |

## 新增题目（7 道，均含 metadata.json + problem.pdf + problem_dark.pdf）
- **第一轮 5 道**：LC-1024、LC-0860、LC-0135、LC-1029、LC-2561
- **第二轮自主新增 3 道**：LC-0330、LC-0406、LC-0881
  （**LC-0881 后来发现 02-two-pointers 已有** ⟹ 并入那份，本专题改索引，所以实体只多了 2 道）

每道都带 2–3 种解法 + 随机对拍，且**每道都写了交换论证或等价说明**：
- LC-0860：1500 组对拍「优先 10+5 的贪心」vs「穷举所有找零分支」
- LC-1029：800 组三方对拍（差额排序 / 改主意视角 / DP）
- LC-0135：1000 组三方对拍（两遍扫描 / O(1) 一次扫描 / 反复松弛）
- LC-0330：400 组对拍「reach 翻倍」vs「逐个补最小缺口」
- LC-0406：300 组「随机造合法队列再打乱还原」
- LC-1024：800 组三方对拍（reach 数组 / 排序扫描 / 最短路 DP）

**执行中发现并修正的三处我自己的错误**（如实记录）：
LC-0860 的 `[5,5,5,5,20,20]` 期望值、LC-0330 的 `[2], n=3` 期望值、
以及两次「把注释插进多行列表字面量中间导致括号未闭合」的编辑失误。

## 校验结果
- 原始文件：105 个，**103 逐字节一致 + 2 个 bug 修复**
- README 相对链接：**死链 0**
- `solution.py` 运行：**26 / 26 通过**（迁移前 21/22，其中 1 个死循环）
- Level 1 / 2 / 3 编号连续
- 写入范围：本专题目录内，加上上面明确说明的四处跨专题去重
- 未执行 `git add` / `commit` / `push`；删除一律用 `trash`，**未使用 `rm -rf`**
