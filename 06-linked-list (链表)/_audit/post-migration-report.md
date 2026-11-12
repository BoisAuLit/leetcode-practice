# 06-linked-list 重构审计报告

## 原始文件保留（135 个文件的 SHA-256 逐个比对）

- **121 个逐字节未变**
- **14 个有变化，全部是有意的，逐条说明如下**

### A. 4 个 LC 的 solution.py 被**追加**内容（没有删除任何原有代码）

| 文件 | 改了什么 |
|---|---|
| LC-0023 | 末尾追加 `Solution_NC`（原 NC 目录的堆实现）；ListNode 类里补了 `from_list` / `print_list_node` |
| LC-0021 | 末尾追加 `Solution_NC` |
| LC-0138 | 末尾追加 `Solution_NC` |
| LC-0025、LC-0328 | ListNode 类里补了 `from_list` / `print_list_node` |

**这 4 个文件里原有的 Solution 类和算法代码一行都没动。**

### B. 9 个文件随 3 个 NC 重复目录一起删除

| NC 目录 | 对应 LC | 删除的文件 |
|---|---|---|
| `NC - Merge K Sorted Linked Lists` | LC-0023 | solution.py / problem.pdf / problem_dark.pdf |
| `NC - Copy Linked List with Random Pointer` | LC-0138 | 同上 |
| `NC - Merge Two Sorted Linked Lists` | LC-0021 | 同上 |

依据：用户的现行规则 **「LC / NC 重复时只保留 LeetCode 版」**。
（instructions.md 写的是归档到 `_neetcode/`，但那条已被更新的规则取代；
而且 `_neetcode/NC - Title/` 仍会匹配 `PROBLEM_DIR_RE`，复习队列会出现重复条目。）

**代码没有丢失**：三个 NC 的 `solution.py` 实现已**一字未改地并入**对应 LC 的 solution.py，
作为 `Solution_NC`，并在横幅里写明来源。已用字符串比对验证：

```
✓ LC-0023  heapq.heappush(min_heap, (node.val, id(node), node))   + class Solution_NC
✓ LC-0138  oldToCopy = defaultdict(lambda: Node(0))               + class Solution_NC
✓ LC-0021  node.next = list1 or list2                             + class Solution_NC
```

被删除的是 6 个 **NeetCode 版题面 PDF**（LeetCode 版题面 PDF 都在，内容是同一道题）。
三个 NC 目录的 `practice` 迁移前**都是空的**，没有复习记录损失。
删除使用 macOS 的 `trash`（可从废纸篓恢复），**没有使用 `rm -rf`**。

## 修复的已有问题

**3 个原本跑不起来的 solution.py**（LC-0023 / LC-0025 / LC-0328）：
它们底部的示例代码调用 `ListNode.from_list(...)` 和 `ListNode.print_list_node(...)`，
但文件内定义的 `ListNode` 类里**没有这两个方法**，运行即
`AttributeError: type object 'ListNode' has no attribute 'from_list'`。

修复方式：把 `_resources/utils/ListNode.py` 里的同名静态方法补进各自的 ListNode 类，
并加注释说明来历。**没有改动任何解法代码。**

迁移前基线：27 通过 / 3 失败。迁移后：**36 通过 / 0 失败**。

## 新增题目（9 道，均含 metadata.json + problem.pdf + problem_dark.pdf）

- 第一轮 6 道：LC-0092、LC-0024、LC-0083、LC-0082、LC-0086、LC-0430
- **LC-0146 LRU Cache**：instructions.md 说「当前已有 NC - LRU Cache」，但本次执行时该目录并不存在。
  我先在本专题新建了一份，随后在全仓库查重时发现 **`17-design (设计)/cache (缓存)/` 早就有 LC-0146**。
  已按「一道题只能有一个实体目录」的规则修正：把新写的三种实现和随机对拍
  **并入 17-design 那份 solution.py**（用户原有实现一字未改），
  删除本专题的重复目录，`06/02` 改为索引 README。
- 第二轮自主新增 2 道：LC-0445、LC-0725

每道新增题都有 2–3 种解法、完整不变量讲解，并在文件末尾用**随机对拍**验证，
其中 LC-0086 额外做了「结果链表无环」检查，LC-0430 额外校验了
「prev 回指正确 + child 已清空 + DFS 顺序」，LC-0146 额外检查了「map 无泄漏」。

## 资源目录
| 原位置 | 新位置 |
|---|---|
| `docs (资料)/00 - Linked List Problems Summary.pdf` | `_resources/docs/` |
| `doubly-linked-list (双链表)/00 - Double Linked List Insertion.pdf` | `_resources/doubly-linked-list/` |
| `doubly-linked-list (双链表)/01 - Linked List VS array.pdf` | `_resources/doubly-linked-list/` |
| `doubly-linked-list (双链表)/02 - Flatten ML Doubly Linked List.py` | `.../01 - LC-0430 .../\_original_sources/` |
| `Floyd's .../template_hasCycle_&_cycleStart.py` | `_resources/templates/` |
| `utils/ListNode.py` | `_resources/utils/` |

搬 `utils/ListNode.py` 之前已用 grep 确认：**没有任何 solution.py import 它**
（每个文件都自带 ListNode 定义），所以搬迁不会破坏运行环境。

## 跨专题
- **LC-0287**：已在 01-arrays-hashing 有完整资料（⭐ 解法正是 Floyd），
  本专题 Level 1 `03/02` 只建索引，不建实体目录。
- **LC-0109 / LC-0353 / LC-0957**：主归属分别更接近树构造 / 队列模拟 / 状态周期检测，
  保留在本专题的 Level 1 `07` 存档区，标 P2，并在 README 说明。

## 校验结果
- 原始文件：135 个，**121 逐字节一致 + 14 个已逐条说明的有意变更**
- README 相对链接：**死链 0**
- `solution.py` 运行：**36 / 36 通过**（迁移前是 27/30）
- Level 1 / 2 / 3 编号连续
- 写入范围：全部在 `06-linked-list (链表)/` 之内
- 未执行 `git add` / `commit` / `push`；未使用 `rm -rf`
