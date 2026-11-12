# 09-heap 重构审计报告

## 原始文件保留
迁移前 88 个文件（不含 `.DS_Store`）。SHA-256 逐个比对：

- **87 个逐字节未变**
- **1 个有意修改**：`NC - Design Twitter/solution.py`（升格为 LC-0355 后的同一文件）。
  原因见下面「修复的已有问题」。

> 说明：本次的基线快照是在**修完 LC-0378 重复问题之后**取的，
> 所以 LC-0378 的 solution.py 合并不体现在上面的对比里。它的详情单独记在下面。

## 修复的已有问题

### 1. LC-0355 Design Twitter 原本跑不起来
文件底部有一行：
```python
print(twitter.followedBy)
```
但类里只有 `self.following`，**没有 `followedBy` 属性** ⟹ 整个文件 `AttributeError`。
已把这一行注释掉并写明原因，**没有改动任何解法代码**。

迁移前基线：14 通过 / 1 失败。迁移后：**24 / 24 全部通过**。

### 2. LC-0378 的重复（本次重构过程中由我造成，已修复）
在更早处理 05-binary-search 时，我误判仓库里没有 LC-0378，
于是在那里新建了一份「值域二分 + 计数」的实现。
实际上 **09-heap 的 `top-k (Top K)/` 下早就有这道题**（用户写的堆解法）。

修复方式：
1. 把我写的「值域二分 + 阶梯计数」「多路归并堆」「暴力基准」三个解法
   **并入 09-heap 这道题的 solution.py**；
2. 用户原有的「全遍历 + 大小 k 的最大堆」实现**一字未改**，保留为 `Solution_0`；
3. **删除 05-binary-search 的那份重复目录**（用 `trash`），
   改成一个索引 README，说明实体目录在 09-heap。

现在全仓库只有一个 LC-0378 实体目录，复习队列不会重复。

## NC 处理
6 个 NC 来源**全部是孤儿**（仓库里没有对应 LC 目录），按规则**升格**：

| 原 NC | 升格为 | id 变更 | practice |
|---|---|---|---|
| NC - Last Stone Weight | LC-1046 | `NC-last-stone-weight` → `LC-1046` | 0 条 |
| NC - Kth Largest Element in a Stream | LC-0703 | `NC-kth-largest-integer-in-a-stream` → `LC-0703` | 0 条 |
| NC - Kth Largest Element in an Array | LC-0215 | `NC-kth-largest-element-in-an-array` → `LC-0215` | 0 条 |
| NC - K Closest Points to Origin | LC-0973 | `NC-k-closest-points-to-origin` → `LC-0973` | 0 条 |
| NC - Task Scheduler | LC-0621 | `NC-task-scheduling` → `LC-0621` | 0 条 |
| NC - Design Twitter | LC-0355 | `NC-design-twitter-feed` → `LC-0355` | **保留 2 条** |

**没有 LC / NC 重复，因此没有删除任何目录。**

## 新增题目（9 道，均含 metadata.json + problem.pdf + problem_dark.pdf）
- **第一轮 7 道**：LC-0692、LC-0373、LC-0502、LC-2542、LC-1834、LC-2402
  （LC-1353 本来也要新建，但全仓库查重发现 **13-greedy 早就有这道题**；
   已把新写的解法并入那份 solution.py，本专题改为索引 README）
- **第二轮自主新增 2 道**：LC-0480、LC-0632

每道都带 2–3 种解法 + 随机对拍。几个值得一提的验证：
- LC-0692：1000 组对拍验证三种写法的 **tie-breaking** 完全一致
- LC-0502 / LC-2542：和暴力枚举组合对拍，验证贪心正确
- LC-1834 / LC-1353 / LC-2402：和朴素模拟对拍 800–1000 组
- **LC-0480**：对拍过程中抓到一个真实 bug —— 当重复值跨越中位线时，
  共享一张 Lazy Deletion 标记表会让删除被**错误的那一边**消费掉，
  导致计数器和堆内容不一致。已改为 `del_small` / `del_large` **分边记标记**。
  这个 bug 在官方样例上不暴露，只有「小值域 + 大量重复」的随机用例能打出来。

## 资源目录
| 原位置 | 新位置 |
|---|---|
| `introduction (堆入门)/`（7 份） | `_resources/introduction/` |
| `top-k (Top K)/` 下的 11 份 PDF/PY 讲义 | `_resources/top-k-theory/` |
| `top-k (Top K)/kth-largest-smallest (第 K 大与第 K 小)/` | `_resources/top-k-theory/kth-largest-smallest/` |
| `utils/`（3 张图） | `_resources/utils/` |

内容全部未改。

## 校验结果
- 原始文件：88 个，**87 逐字节一致 + 1 个已说明的修复**
- README 相对链接：**死链 0**
- `solution.py` 运行：**24 / 24 通过**（迁移前 14/15）
- Level 1 / 2 / 3 编号连续
- 写入范围：本专题目录内（唯一的例外是上面说明的 LC-0378 跨专题去重，
  它删除的是**我自己本次误建**的那份，并在 05 留了索引 README）
- 未执行 `git add` / `commit` / `push`；未使用 `rm -rf`
