# tools/ — 复习调度与错题建档

## 每天的固定流程（约 15–45 分钟）

```bash
python3 tools/review_due.py today          # ① 看今天到期的复习；不足 3 题会自动从"未排期"里跨分类补足
# ② 对每一题：闭卷重写 → 跑文件头里的守卫反例 → 对照原解
python3 tools/review_due.py done "Gas Station" g     # ③ 记结果：g=🟢 闭卷流畅  y=🟡 有印象但慢  r=🔴 卡壳
# ④ 出了 bug → 打开 MISTAKES.md，归入已有模式（复发 +1）或新建模式；把守卫反例补进文件头
git add -A && git commit -m "review $(date +%F)"      # ⑤ 每天一提交，git log 就是打卡表
```

做新题时：写完 → `python3 tools/review_due.py init <文件> "<信号→模式一句话>"` → 补卡点/守卫 → 明天会自动进入复习。

## 文件头长什么样

```python
"""
📌 信号→模式: 两个序列各一个指针 → 双序列 DP（LCS 家族）
📅 首次: 2026-09-04 | 卡点: M1 边界层右列漏 break | 守卫: ("ba","c","cbx")->False
🔁 复习: 2026-09-05 🟡 | 2026-09-08 🟢 | 下次: 2026-09-15
"""
```

- **信号→模式**：看到题目里的什么词/结构，应该触发哪个模板——这是"十秒识别"的训练目标，复习时先盖住代码只看这一行。
- **卡点**：写 `M1`、`M9` 这类 MISTAKES.md 里的模式编号，或一句话。
- **守卫**：一个最小反例 `输入 -> 期望`，重写后 10 秒验证有没有再踩同一个坑。
- **复习**：脚本自动维护，不用手改。节奏 1 → 3 → 7 → 14 → 30 天；🔴 重置为 1 天，🟡 间隔不变，30 天后再 🟢 即毕业。

## 其他命令

```bash
python3 tools/review_due.py today -n 5     # 今天想多做几题
python3 tools/review_due.py stats          # 各分类进度
python3 tools/review_due.py list due|unscheduled|scheduled|graduated|all
python3 tools/add_headers_once.py --dry-run   # 一次性批量加头（幂等）；--undo 精确移除未使用过的头
```

## 说明

- `signals_manifest.txt` 是全仓库 134 题的"信号→模式"总索引，也可以当速查表翻。
- 批量加头时"首次"日期取自 git 首次提交日期；因为以前是攒着提交的，这个日期偏晚，不影响调度，介意可手动改。
- 只处理有复习头的文件；`$$-垃圾-可忽略`、`tools/`、`__pycache__` 一律忽略。
