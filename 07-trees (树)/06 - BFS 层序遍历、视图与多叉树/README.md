# Level 1 · 06 BFS 层序遍历、视图与多叉树

## 核心定义
队列的 FIFO 保证「第 d 层的节点全部排在第 d+1 层之前」，
所以 BFS 天然按层推进。本章全部题目共用**一个分层骨架**。

## 分层骨架（整章就这一段）
```python
q = deque([root])
while q:
    for _ in range(len(q)):      # ★ 进层时先固定住本层节点数
        node = q.popleft()
        ...                      # 每题不同的只有这里和「怎么收集本层结果」
        if node.left:  q.append(node.left)
        if node.right: q.append(node.right)
```

`len(q)` 必须在进入这一层时**先取出来**。
写成 `for _ in range(len(q))` 是因为循环体里会往 q 里加下一层的节点。

## 同一个骨架，四种收集方式

| 题 | 本层结果怎么收 |
|---|---|
| **LC-0102** Level Order | 全部收进一个列表 |
| **LC-0103** Zigzag | 交替 `level[::-1]`（**不要改入队顺序**） |
| **LC-0199** Right Side View | 只取本层**最后一个** |
| **LC-0429** N-ary | 把 `node.left/right` 换成 `for child in node.children` |

**LC-0103 最常见的错解**：交替改变入队顺序。
那会破坏下一层的父子对应关系。**遍历顺序不变，只改「怎么摆」。**

## 带坐标的遍历（两种不同的坐标）

| 题 | 坐标是什么 | 怎么用 |
|---|---|---|
| **LC-0314** Vertical Order | **列**：root=0，left=col-1，right=col+1 | 按列分桶，桶内按行序 |
| **LC-0662** Maximum Width | **堆式编号**：root=0，left=2i+1，right=2i+2 | 每层宽度 = 末编号 − 首编号 + 1 |

LC-0662 的编号会**指数增长**，深度 60 就超过 2^60。
Python 不溢出，但通用做法是**每层减去该层第一个节点的编号**做归一化 ——
既安全又能直接迁移到 C++/Java。

**LC-0314 vs LC-0987**：两题都按列分组，但 **987 要求同一行同一列的节点按值排序**，
314 只要求按遍历顺序。**排序规则不同，代码不能互相照抄。**

## 同层 Next Pointer：LC-0116 vs LC-0117（本章最有教学价值的一对）

| | LC-0116 | LC-0117 |
|---|---|---|
| 树形 | **完美二叉树** | 任意二叉树 |
| `node.left.next = node.right` | 永远成立 | **不一定**（可能没有右孩子） |
| 找下一层的邻居 | `node.next.left` 直接可用 | 要沿 next **一路往右找**第一个有孩子的 |
| O(1) 空间解法 | 两行连线即可 | 需要 **dummy + tail** |

LC-0117 的 O(1) 解法：**把上一层已经连好的 next 链当作链表来遍历**，
同时用一个 dummy 头 + tail 指针串出下一层：
```python
cur = root
while cur:
    dummy = Node(0); tail = dummy
    while cur:                                   # 沿当前层横着走
        if cur.left:  tail.next = cur.left;  tail = tail.next
        if cur.right: tail.next = cur.right; tail = tail.next
        cur = cur.next
    cur = dummy.next                             # 下沉到下一层
```

**复杂度必须说准**：BFS 队列版是 **O(w) 空间**，不是 O(1)。
只有上面这个「用上一层 next 当链表」的版本才是 O(1)。

## 题目

| # | 题 | 优先级 |
|---|---|---|
| 01/01 | LC-0102 Binary Tree Level Order Traversal | P0 |
| 01/02 | LC-0103 Zigzag Level Order Traversal | P1 |
| 01/03 | LC-0199 Binary Tree Right Side View | P0 |
| 02/01 | LC-0314 Vertical Order Traversal | P2（可能是 Premium） |
| 02/02 | LC-0662 Maximum Width of Binary Tree | P2 |
| 03/01 | LC-0429 N-ary Tree Level Order Traversal | P1 |
| 04/01 | LC-0116 Populating Next Right Pointers | P1 |
| 04/02 | LC-0117 Populating Next Right Pointers II | P1 |

## BFS vs DFS
- **BFS**：天然按层，适合「最短层数」「每层一个结果」「层宽」。
- **DFS**：也能拿到层序结果（按深度分桶，见 LC-0103 的 Solution_3），
  但做不到「边走边按层提前退出」。
- **LC-0199 右视图**两种都行：BFS 取每层最后一个，
  或 DFS 按「根 → 右 → 左」顺序、每个深度第一次到达的就是右视图节点。

## 常见错误
- 忘了用 `len(q)` 固定本层大小 ⟹ 层与层混在一起。
- LC-0103 通过改入队顺序来「反转」。
- LC-0662 不做编号归一化（在 C++/Java 里会溢出）。
- 把 LC-0117 的 BFS 队列版说成 O(1) 空间。
- LC-0314 直接套 LC-0987 的排序规则。

## 复习时的 Pattern Recognition
> 「按层输出」「每层第一个/最后一个」「层宽」「同层连指针」
> → 分层 BFS。**骨架永远一样，只改收集方式。**


---

## 2026-11-11 新增题目（对照大厂高频题单补的缺口）

| 题 | 位置 | 信号 → 模式 | 备注 |
|---|---|---|---|
| [LC-0987 Vertical Order Traversal of a Binary Tree](<./02 - 带坐标的层序遍历/03 - LC-0987 - Vertical Order Traversal of a Binary Tree>) | `06 - BFS 层序遍历、视图与多叉树/02 - 带坐标的层序遍历` | 和 LC-0314 唯一区别：同行同列按值排 ⟹ 桶内 sorted((row,val)) | 带坐标 BFS |

每道题的 `solution.py` 都带：全部主流解法（各自的复杂度与适用场景）、一个 ⭐️ Preferred、和一段对独立真值基线的随机对拍。
