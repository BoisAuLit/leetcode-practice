# Recognition — Enumerating / Validating Paths（返回所有路径 / 验证所有路径）

题目信号
- "return ALL paths from source to target" → 枚举 → **DFS + backtracking**
- "do all paths from s end at t" / "every path leads to" → 验证 → **DFS 3-state**（环 ⇒ False，叶子必须是 t）

模板
- 枚举（DAG）：`path.append → dfs → path.pop`；到达 target 时 copy 一份
- 数量是指数级的，不可能比 O(2^N·N) 更好

题目
- 0797 All Paths From Source to Target — DFS 记忆化 (A) / 回溯 (B 🚀) / BFS 带路径 (C) / TODO (D, E)
- 1059 All Paths from Source Lead to Destination — DFS WHITE/GRAY/BLACK (A, B)
