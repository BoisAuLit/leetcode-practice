# 07-trees 重构审计报告

## 原始文件保留（160 个文件的 SHA-256 逐个比对）

- **148 个逐字节未变**
- **12 个有变化，全部有意，逐条说明如下**

### A. 9 个 solution.py 被修改 —— 全部是**修复原本跑不起来的文件**

迁移前基线：**28 通过 / 8 失败**。8 个失败全是同一类原因：
文件底部的示例代码调用 `TreeNode.from_list(...)` / `printTree()`，
但文件里的 `TreeNode` 要么**根本没定义**（只有 `TreeNode_1`），
要么**缺这些方法**，运行即 `NameError` / `AttributeError`。

| 文件 | 原因 | 修复 |
|---|---|---|
| LC-0101、LC-0104 | 引用了不存在的 `TreeNode` | 插入取自 `utils/TreeNode.py` 的标准 TreeNode 类 |
| LC-0250、LC-0236、LC-0102、LC-0314 | `TreeNode` 缺 `from_list` | 把方法补进已有的类里 |
| LC-0863 | `TreeNode` 缺 `printTree` | 同上 |
| LC-0257 | **用户代码里的真实 typo**：`stack.append(node.left.val)` 压进去的是 int，下一轮 `node.val` 直接 AttributeError | 改成 `stack.append(node.left)`，并加注释说明（另注：该类名叫 `Inorder_Traversal`，但这种栈写法其实是 Preorder） |
| LC-0100 | 并入 NC 版独有的迭代栈解法（见下） | 追加 `Solution_NC_DFS_Iterative_Stack` + 一行 `TreeNode = TreeNode_1` 别名 |

**所有修复都只补定义 / 改那一行 typo，没有改动任何解法逻辑。**
迁移后：**49 / 49 全部通过**。

### B. 3 个文件随 NC 重复目录删除

`NC - Same Binary Tree`（solution.py + problem.pdf + problem_dark.pdf）。

依据：用户现行规则「LC / NC 重复时只保留 LeetCode 版」。
`LC-0100 - Same Tree` 已存在，两者 `practice` 均为空。

**代码没有丢失**：NC 版里有一个 LC 版**没有的迭代栈 DFS**
（用户自己在代码里标了 `✅ Preferred method`），已一字未改地并入 LC-0100。
并用随机对拍 500 组验证：递归版 / BFS 版 / 并入的迭代栈版三者结果完全一致。

删除使用 macOS `trash`（可恢复），**没有用 `rm -rf`**。

## NC 孤儿题的升格（9 个）

这 9 个 NC 目录在仓库里**没有对应的 LC 目录**，属于孤儿，按规则**升格**而非删除：
目录改名为正式 LC 编号，`metadata.id` 从 `NC-xxx` 改为 `LC-xxxx`，
**`practice` 复习记录原样保留**，solution.py / note.md 一个字节未改。

| 原 NC | 升格为 | practice |
|---|---|---|
| NC - Diameter of Binary Tree | LC-0543 | 0 条 |
| NC - Binary Tree Maximum Path Sum | LC-0124 | 0 条 |
| NC - Count Good Nodes in Binary Tree | LC-1448 | 0 条 |
| NC - Valid Binary Search Tree | LC-0098 | 0 条 |
| NC - Kth Smallest Integer in BST | LC-0230 | 0 条 |
| NC - Lowest Common Ancestor in BST | LC-0235 | 0 条 |
| NC - Construct Binary Tree from Preorder and Inorder | LC-0105 | 0 条 |
| NC - Serialize and Deserialize Binary Tree | LC-0297 | 0 条 |
| NC - Binary Tree Right Side View | LC-0199 | **保留 1 条** |
| NC - Subtree of Another Tree | LC-0572 | 0 条 |

（instructions.md 提到的另外 4 组 NC/LC 重复 —— Balanced / Invert / Max Depth /
Level Order —— 在本次执行时**已经不存在**，更早一轮的 NC 清理已经处理过了。）

## 新增题目（14 道，均含 metadata.json + problem.pdf + problem_dark.pdf）

- **第一轮 9 道**：LC-0437、LC-0114、LC-0173、LC-0450、LC-0337、LC-0113、LC-0103、LC-0700、LC-0129
- **第二轮自主新增 5 道**：LC-0117、LC-0701、LC-0938、LC-1026、LC-0662

每道新增题都有 2–3 种解法 + 完整的「dfs 返回什么」讲解，
并在文件末尾用**随机对拍**验证（对照暴力枚举或独立算法），其中：
- LC-0450 额外校验「删除后仍是合法 BST 且中序 == 排序后的全集」
- LC-0114 额外校验「展开后所有 left 都是 None」
- LC-0117 额外校验「next 链 == 标准 BFS 层序」
- LC-0437 覆盖负数与 target = 0
- LC-0662 覆盖编号归一化

## 资源目录
`docs (资料)` → `_resources/docs`；`tutorials (教程)`（4 份 BST/DFS/BFS 教程 + TreeNode.py）
→ `_resources/tutorials`；`utils` → `_resources/utils`。**内容全部未改。**

## 校验结果
- 原始文件：160 个，**148 逐字节一致 + 12 个已逐条说明的有意变更**
- README 相对链接：**死链 0**
- `solution.py` 运行：**49 / 49 通过**（迁移前 28/36）
- Level 1 / 2 / 3 编号连续
- 写入范围：全部在 `07-trees (树)/` 之内
- 未执行 `git add` / `commit` / `push`；未使用 `rm -rf`
