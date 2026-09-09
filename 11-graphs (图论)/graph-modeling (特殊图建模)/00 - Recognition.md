# Recognition — Special Graph Modeling（先把题建模成图 / 树，再套模板）

题目信号
- 输入不是图，但关系可以当成图：等式 a/b = k（带权有向边）、嵌套列表（树）、字符串结构

题目
- 0399 Evaluate Division — 变量 = 节点，a/b = k ⇒ a→b 权 k，b→a 权 1/k；查询 = DFS 沿路累乘（带权并查集版在 `archive/004`）
- 0339 Nested List Weight Sum — DFS 带 depth / BFS 分层
- 0364 Nested List Weight Sum II — 两遍分层 BFS（先求最大深度）
