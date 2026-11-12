
cd '/Users/bohaoli/Desktop/tuto/tuto_leetcode/leetcode-practice/08-tries (字典树、前缀树)' && claude "$(cat <<'PROMPT'
请直接执行当前 Trie（字典树、前缀树）LeetCode 学习目录的系统性重构。

我的目标是准备 Silicon Valley FAANG / Big Tech Software Engineer、AI Engineer 算法面试和 Online Assessment（OA）。

请建立一套：
- 面试价值高
- 算法迁移性强
- 学习难度循序渐进
- 结构清晰、适合长期复习
- 覆盖重要 Trie 变体
- 尽可能减少机械记忆

的 Trie 学习体系。

你必须实际执行目录重构、题目迁移、新题生成、README 编写和最终验收。

不要只给出规划。

==================================================
一、核心学习目标
==================================================

我的脑容量和学习时间有限。

我不想为每一道 Trie 题目分别记忆一套算法。

请围绕少量可复用的核心模式组织题库：

1. TrieNode（字典树节点）
2. Insert（插入）
3. Search（完整单词查找）
4. StartsWith（前缀查找）
5. End-of-Word Marker（单词结束标记）
6. Trie + DFS（字典树与深度优先搜索）
7. Wildcard Matching（通配符匹配）
8. Prefix Pruning（前缀剪枝）
9. Trie + Backtracking（字典树与回溯）
10. Prefix Count（前缀计数）
11. Autocomplete（自动补全）
12. Trie + Dynamic Programming（字典树与动态规划）
13. Bitwise Trie（二进制字典树，可选进阶）

优先彻底掌握：

LC-208
LC-211
LC-212

这三道是本专题最重要的核心题目。

其他题目用于理解有迁移价值的应用和变体。

不能因为某题具有 Trie 标签，
就将它列为核心必背题。

==================================================
二、Level 1 -> Level N 目录规则
==================================================

采用以下基本结构：

Level 1：Trie 算法家族
Level 2：具体 Pattern
Level 3：LeetCode 题目

必要时可以增加 Level 4。

但不要为一个微小区别制造新的算法分类。

同级文件夹全部使用：

01 - ...
02 - ...
03 - ...

排序优先考虑：

1. 学习依赖关系
2. 面试代表性
3. 知识迁移性
4. 难度递进
5. 记忆成本
6. 算法之间的复用关系

不能简单按照 LeetCode 题号排序。

Level 3 文件夹命名：

01 - LC-0208 - Implement Trie (Prefix Tree)
02 - LC-0648 - Replace Words

每个 Level 2 下独立从 01 开始编号。

_resources、_neetcode、utils、_conflicts
等目录不参与算法分类编号。

如果一个 Level 2 只有一道题，
只有在它确实代表独立重要的 Pattern 时才保留。
允许合并不必要的单题分类。

==================================================
三、Level 1 / Level 2 / Level 3 目标结构
==================================================

第一轮推荐 5 个 Level 1。

--------------------------------------------------
LEVEL 1
01 - Trie 基础结构与前缀匹配
--------------------------------------------------

核心：
TrieNode
Insert
Search
StartsWith
Shortest Prefix Matching

Level 2：
01 - Trie 基础操作与最短前缀

Level 3：

01 - LC-0208 - Implement Trie (Prefix Tree)
02 - LC-0648 - Replace Words

教学重点：

LC-208：

最重要的基础模板。

实现：

Trie()
insert(word)
search(word)
startsWith(prefix)

建议使用：

class TrieNode:
    children
    is_end

必须解释：

- 为什么 Trie 的每一条边代表一个字符
- 为什么共享前缀能够共享节点
- 为什么 search 必须检查 is_end
- 为什么 startsWith 不要求 is_end
- 如何处理重复插入
- 时间复杂度如何依赖单词长度 L
- 空间复杂度如何依赖 Trie 的节点数量

不要只给出代码，还需要解释节点不变量。

LC-648：

Shortest Matching Prefix。

将词根插入 Trie。

对于句子中的每个单词，
从根节点沿字符查找。

一旦到达 is_end=True 的节点，
即可找到最短词根并停止。

重点解释：

为什么找到第一个完整词根就可以停止搜索。

这道题的目的：
复用 LC-208，不需要额外记忆新 Trie 结构。

==================================================
LEVEL 1
02 - Trie + DFS 与回溯搜索
==================================================

核心：
Wildcard Search
DFS Branching
Backtracking
Prefix Pruning

Level 2：
01 - 通配符查找与 Trie 分支搜索

Level 3：

01 - LC-0211 - Design Add and Search Words Data Structure

教学重点：

在标准 Trie 中加入：

'.' 可以匹配任意单个字符。

普通字符：
只需要沿对应 child 继续搜索。

通配符：
必须尝试当前节点的所有有效 children。

核心 DFS 状态：

(node, index)

必须解释：

- 为什么普通 search 只需要一条路径
- 为什么 '.' 需要探索多个分支
- 什么时候返回 True
- 什么时候返回 False
- 为什么仍然需要 is_end 判断
- 搜索复杂度与通配符分支数的关系

不要错误地声称带通配符的搜索始终为 O(L)。

这道题代表：
Trie + DFS Branching。

--------------------------------------------------

Level 2：
02 - Grid Backtracking 与 Trie 剪枝

Level 3：

01 - LC-0212 - Word Search II

教学重点：

Trie + DFS + Backtracking。

先把 words 插入 Trie。

随后从 Board 的格子出发进行 DFS。

每次只沿 Trie 中存在的字符路径继续。

必须解释：

- 为什么直接对每个 word 分别搜索可能很慢
- 为什么 Trie 可以共享不同 words 的前缀
- 为什么不存在对应 child 时可以立即剪枝
- 如何防止同一条路径重复使用一个 Board Cell
- 什么时候恢复 Board 或 visited 状态
- 如何避免重复返回相同单词
- 如何正确处理 is_end / word 标记

可以根据实现选择是否删除已找到的单词，
但必须保证 Trie 剪枝与节点删除正确。

重点理解：

Trie 管理候选单词前缀。
DFS 管理 Board 上的空间搜索。

两者职责不同。

这道题是 P0 进阶核心题，
应在熟练掌握 LC-208 和 LC-211 后练习。

==================================================
LEVEL 1
03 - Trie 前缀统计与搜索应用
==================================================

核心：
Autocomplete
Prefix Aggregation
Prefix Count
Hierarchical Prefix Matching

Level 2：
01 - 自动补全与前缀聚合

Level 3：

01 - LC-1268 - Search Suggestions System
02 - LC-2416 - Sum of Prefix Scores of Strings

教学重点：

LC-1268：

给定搜索前缀，
返回字典序最小的最多 3 个商品名称。

可以使用：

Sorting + Binary Search

或者：

Trie + Prefix Suggestions。

本专题优先解释 Trie 解法，
但必须注明 Trie 并不是唯一或必需解法。

如果使用 Trie：
可以在每个 Prefix Node 维护至多三个最小的候选词。

必须解释：
- 为什么只需保留前三个
- 如何维护字典序
- 如何处理不存在的前缀
- 如何避免不必要的完整子树遍历

在 README 中简要比较 Trie 与 Binary Search 方案。

LC-2416：

Prefix Scores。

每个 TrieNode 除了 children，
还可以保存 prefix_count。

插入每个单词时，
经过对应节点就增加计数。

查询一个单词的分数时，
沿它的每个前缀节点累计 count。

重点解释：

- 为什么每个节点的 count 代表共享该前缀的单词数量
- 为什么不能只统计完整单词的出现次数
- 为什么重复单词也需要正确计数
- 查询和插入的复杂度如何取决于单词长度

这是最值得学习的 Trie Augmentation
（在字典树节点上维护附加信息）案例之一。

--------------------------------------------------

Level 2：
02 - 层级路径与前缀过滤

Level 3：

01 - LC-1233 - Remove Sub-Folders from the Filesystem

教学重点：

检测父目录与子目录关系。

例如：

/a
/a/b

后者是前者的子目录。

但是：

/a
/ab

不能认为 /ab 是 /a 的子目录。

必须正确处理 "/" 的路径边界。

本题可以通过：
Sorting + Prefix Checking

高效解决。

也可以使用 Trie。

本专题可以介绍 Trie 方案，
但必须解释更简单的排序方案。

标记 P1 或 P2，
不需要强制记忆 Trie 版本。

==================================================
LEVEL 1
04 - Trie + DP 与字符串划分
==================================================

核心：
Trie Prefix Matching
Dynamic Programming
String Segmentation

Level 2：
01 - Trie 加速字符串划分

Level 3：

01 - LC-3291 - Minimum Number of Valid Strings to Form Target I

教学重点：

题目中的 Valid String
是 words 中任意单词的非空前缀。

目标：
使用尽可能少的 Valid Strings 拼接 target。

核心状态：

dp[i] = 组成 target 前 i 个字符的最少段数

建立 Trie 存储 words。

从 target 的某个位置 i 出发，
沿 Trie 尝试匹配后续字符。

对于每个匹配成功的非空前缀，
更新对应的 DP 状态。

必须解释：

- 为什么 DP 状态表示前 i 个字符
- 为什么能够使用 Trie 查找合法片段
- 为什么可以提前终止不匹配的前缀搜索
- 如何处理不能组成 target 的情况
- 如何避免错误的下标边界
- 为什么 Trie 是匹配加速结构，而 DP 是优化决策结构

需要根据当前正式题目约束验证算法复杂度。

不要在未经证明的情况下声称其为线性时间。

本题标记 P2 进阶。
主要用于了解 Trie 与 DP 的组合。

如果此题的已有解法采用其他正确技巧，
必须保留原有 solution.py。

==================================================
LEVEL 1
05 - 进阶变体与跨专题存档
==================================================

目的：

保留已有学习成果，
同时认识 Trie 相关的重要扩展方向。

不强制要求将本分类全部题目背诵。

--------------------------------------------------

Level 2：
01 - Bitwise Trie 与最大 XOR

Level 3：

01 - LC-0421 - Maximum XOR of Two Numbers in an Array

教学重点：

把 Trie 中的字符边替换为：

bit 0
bit 1

从最高有效位到最低位插入整数。

查询某个数字时，
优先尝试与当前 bit 相反的分支，
从而尽可能使 XOR 对应位等于 1。

必须解释：

- 什么是 XOR
- 为什么优先相反 bit
- 为什么要从高位开始
- 为什么 TrieNode 可以只有两个 children
- 时间复杂度如何与位宽有关

这是 Binary Trie 的经典代表题。

但它属于 Bit Manipulation + Trie 的组合。

本专题标记 P2，可选学习。
不要求将 Bitwise Trie 作为 FAANG 准备的核心必背模板。

--------------------------------------------------

Level 2：
02 - Common Prefix 的非 Trie 主流解法

Level 3：

01 - LC-0014 - Longest Common Prefix
02 - LC-3043 - Find the Length of the Longest Common Prefix

教学重点：

LC-14：

普通 String Prefix Comparison 即可解决。

可以横向或纵向比较字符，
也可以使用排序。

Trie 不是必需的。

该题本身是基础字符串题，
但不是必须使用 Trie 的题。

LC-3043：

求两个整数数组之间的最长公共数字前缀。

可使用 Hash Set 存储数字前缀。
Trie 也是可行思路。

必须区分：
String Trie 和 Digit Trie。

请保留原有 solution.py，
不能因为分类调整而替换已有解法。

这组题标记 P2（针对 Trie 专题）。
它们在其他专题可能具有更高优先级。

--------------------------------------------------

Level 2：
03 - 多模式匹配与区间合并

Level 3：

01 - LC-0616 - Add Bold Tag in String

教学重点：

识别字符串中所有需要加粗的匹配区间。

当匹配区间重叠或相邻时，
必须合并。

可以使用：
- String Matching
- Interval Marking / Merging
- Trie Matching

但不强制使用 Trie。

必须保留已有图解：

asset-003 - 0616 - A - Add Bold Tag in String - 史诗级教科书.jpeg

这一题主要体现：

Multi-pattern Matching + Interval Processing。

标记 P2。

==================================================
四、现有题目审计与正式化
==================================================

当前 tree 中存在 9 个题目来源文件夹：

LC-0014
LC-1268
LC-3043
NC - Design Add and Search Word Data Structure
NC - Implement Trie (Prefix Tree)
LC-0616
LC-1233
LC-3291
NC - Word Search II

首先需要验证这 9 个题目来源。

其中三个 NC-only 来源：

NC - Implement Trie (Prefix Tree)
NC - Design Add and Search Word Data Structure
NC - Word Search II

分别对应：

LC-0208
LC-0211
LC-0212

请逐一检查题面与原始代码。

如果确实对应：

1. 建立正式 LC Level 3 文件夹。
2. 通过仓库原有生成工具创建标准 LC 文件。
3. 将原 NC 来源完整移动到 _neetcode/。
4. 保留 NC solution.py。
5. 保留 NC metadata 和 PDF。
6. 保留所有图片、SVG 和其他附件。
7. 在 README 中说明原 NC 版本与 LC 版本是否存在实现差异。

特别保护：

NC - Design Add and Search Word Data Structure：

asset-02 - DFS 解法图解.svg
asset-02 - Explanation.jpeg

NC - Word Search II：

asset-03 - explanation.jpg

不能因为正式化而丢掉这些学习资料。

同一道题只占据一个正式 Level 3。

==================================================
五、明确建议新增的题目
==================================================

第一轮新增不同题目：

LC-0648 - Replace Words
LC-2416 - Sum of Prefix Scores of Strings
LC-0421 - Maximum XOR of Two Numbers in an Array

其中：

LC-648 和 LC-2416 是推荐的主要新增题目。

LC-421 是 P2 扩展，
不需要作为核心必背。

另外需要将已有三个 NC-only 题：
208、211、212
整理成正式 LC 目录。

对于所有新建或正式化的 LC 题目，
调用仓库已有 LeetCode 生成能力，创建：

metadata.json
problem.pdf
problem_dark.pdf
solution.py

请复用现有工作流。

如果某题已经有完整 LC 标准文件，
不要重新生成或覆盖。

如果生成工具失败：
- 保留成功生成的文件。
- 说明失败原因。
- 不要创建空 PDF。
- 不要伪造题目 metadata。
- 不要覆盖已有 Python 解法。

==================================================
六、Claude Code 第二轮独立审核
==================================================

以上是 ChatGPT 第一轮推荐。

请独立检查 Trie 知识体系是否存在重要遗漏。

参考：

NeetCode 150
NeetCode 250
Blind 75
Grind 75 / Grind 169
LeetCode Top Interview 150
其他可靠的算法面试资料

如果网络访问可用，
请验证正式题号、题名、约束及主流解法。

不要编造 FAANG 企业真实出题频次。

重点检查以下知识：

1. Basic Trie
2. Word Insertion
3. Exact Word Search
4. Prefix Search
5. End-of-Word Marker
6. Wildcard Matching
7. DFS Branching
8. Backtracking + Trie
9. Prefix Pruning
10. Trie-based Autocomplete
11. Prefix Counting
12. Trie Node Augmentation
13. Prefix Replacement
14. Trie + DP
15. Multiple Pattern Matching
16. Hierarchical Prefix Filtering
17. Binary Trie

独立审核以下候选：

LC-0677 - Map Sum Pairs
LC-1804 - Implement Trie II (Prefix Tree)
LC-0745 - Prefix and Suffix Search
LC-1032 - Stream of Characters
LC-0720 - Longest Word in Dictionary
LC-0676 - Implement Magic Dictionary
LC-1707 - Maximum XOR With an Element From Array

这些只是候选，不要求全部加入。

特别注意：

LC-677：
Trie 节点可以维护 Prefix Sum，
但与 LC-2416 的前缀统计有明显联系。

LC-1804：
在 Trie 中增加单词计数、前缀计数及删除操作。
适合巩固动态 Trie 数据结构。

LC-745、1032：
可能涉及更特殊的 Trie 设计或字符串处理技巧。

LC-1707：
Bitwise Trie + Offline Query，
不应在尚未掌握 LC-421 时强行学习。

你应评估每道候选是否具有：
- 足够高的面试价值
- 独立的可迁移 Pattern
- 合理的学习成本
- 与现有核心题的明显区别

最多独立新增 4 道。

如果发现更多候选，
优先选最重要的 4 道，
其他记录在 README 的 Future Candidates。

不要为了增加题目数量而添加冷门技巧题。

特别不要把整个字符串算法领域
（KMP、Suffix Array、Aho-Corasick 等）
全部纳入 Trie 目录。

它们可能相关，但属于不同算法家族。

如果独立审核没有发现值得新增的题目，
允许不添加。

也允许基于明确的教学理由新增 Level 1 或 Level 2，
但禁止无意义的分类碎片化。

==================================================
七、现有资源与工具安全整理
==================================================

当前存在：

docs (资料)/
  Trie.png

utils/
  TrieUtils.py

建议：

将纯理论资料移动到：

_resources/
  docs/
    Trie.png

但不要盲目移动 utils/TrieUtils.py。

首先检查：

- 所有 solution.py
- 所有 tutorial 或 note 文件
- Python import
- 相对路径依赖
- 是否有 Symbolic Link

如果现有代码依赖 utils/TrieUtils.py，
优先保持 utils 位置不变。

如果确定移动不会破坏依赖，
可以安全整理。

不得随意修改原始工具代码。

特别检查：

LC-0014：
asset-001 - 0014 - meta.json

这个文件名称与 metadata.json 相似，
但不代表它是重复垃圾。

请检查内容，保留原始文件，
不能未经确认就删除或覆盖。

LC-3291：
asset-explanation.jpg
note.md

LC-1233：
原有 JPEG 图解。

LC-0616：
原有 JPEG 图解。

LC-3043、LC-1268：
全部标准文件及额外附件。

迁移时必须完整保留。

==================================================
八、Git 安全与文件保护
==================================================

当前 Git 仓库存在大量未提交修改与未跟踪文件。

因此必须严格保护已有内容。

执行前：

1. pwd
2. tree
3. git status --short
4. 递归扫描当前目录
5. 保存现有文件路径清单
6. 记录普通文件的 SHA-256
7. 识别 Symbolic Links
8. 检查可能的重名冲突
9. 检查原有题目与解法是否对应
10. 建立旧路径到新路径的完整迁移映射

严禁：

git reset
git clean
git restore .
git checkout -- .
rm -rf
强制覆盖
删除未跟踪文件
覆盖原有 solution.py
删除已有笔记或图解
修改其他算法专题

本次不要自动：

git add
git commit
git push

只允许修改当前：

08-tries (字典树、前缀树)

目录内部的文件。

可以只读扫描其他专题，
用于检查跨专题题目。

如果文件存在冲突：

- 不得丢弃任意版本。
- 不得默认新文件更正确。
- 必须保留原始代码和新版本。
- 可以使用 _conflicts/ 保存不同版本。
- 在最终报告说明冲突。

已跟踪文件和未跟踪文件必须同样保护。

不要通过符号链接修改当前目录之外的文件。

若题目生成工作流必须写入仓库其他位置，
先寻找可以将输出直接限定在本目录的方案。

无法安全限制时，
停止该生成步骤并记录原因，
不要冒险覆盖其他专题。

整体流程尽量满足 Idempotence（幂等）：

重复执行不应出现：
- 重复编号
- 重复题目
- 重复 NC 来源
- 文件覆盖
- 丢失资料

==================================================
九、README 学习文档
==================================================

必须创建：

A. 当前 Trie 根目录 README.md
B. 每个 Level 1 的 README.md
C. 对复杂 Pattern 创建必要的简短说明

根目录 README 内容：

1. Trie 完整知识地图
2. 五个 Level 1 的教学目标
3. 所有 Level 2 / Level 3 题目
4. P0 / P1 / P2 优先级
5. TrieNode 数据结构
6. 核心 Python 模板
7. Trie + DFS 模板
8. Prefix Count 模板
9. Trie + DP 思路
10. 主要复杂度分析
11. 跨专题索引
12. 第二轮独立审核结果
13. 推荐学习顺序
14. 不需要额外记忆的特殊技巧

特别建立 Trie Pattern Recognition Guide。

例如：

Q1：
是否需要大量查询完整单词是否存在？
-> Hash Set 或 Trie，按查询需求选择。

Q2：
是否频繁查询任意字符串前缀？
-> Trie。

Q3：
是否允许某个字符匹配多种可能？
-> Trie + DFS。

Q4：
是否在 Grid 中同时查找很多单词？
-> Trie + Backtracking。

Q5：
是否需要统计多少单词经过某个前缀？
-> Prefix Count Trie。

Q6：
是否需要自动补全？
-> Trie 或 Sorting + Binary Search。

Q7：
是否需要将一个字符串划分为多个字典前缀？
-> Trie + DP。

Q8：
是否需要通过按位选择最大化 XOR？
-> Bitwise Trie（进阶）。

必须说明 Trie 不是所有字符串问题的最优解法。

对于可使用更简单的：
Hash Set
Sorting
Binary Search
String Scanning
的方法，
应该明确列出。

==================================================
十、核心 Python 模板
==================================================

README 至少提供：

Template 1：
Basic Trie

class TrieNode
insert
search
startsWith

Template 2：
Trie + DFS Wildcard Search

Template 3：
Trie + Backtracking with Prefix Pruning

Template 4：
Trie with Prefix Count

其他变体只讲关键改动，
不要求每一种应用都重新记忆完整 Trie 实现。

特别解释：

Basic Trie：
children + is_end

Wildcard Trie：
增加 DFS Branching

Word Search II：
增加 Board DFS + Prefix Pruning

Prefix Count：
增加 count 字段

Autocomplete：
增加候选结果或字典序遍历

Bitwise Trie：
children 从字符映射变成 0/1 分支

这些都是在少量核心结构之上的变化。

==================================================
十一、理论说明风格
==================================================

请使用：

中文主导 + 英文专业术语。

例如：

Trie（字典树）
Prefix Tree（前缀树）
TrieNode（字典树节点）
Prefix Pruning（前缀剪枝）
Wildcard Search（通配符搜索）
Backtracking（回溯）
Prefix Aggregation（前缀信息聚合）
End-of-Word Marker（单词结束标记）

每种 Pattern 采用：

1. 1–3 个决定性观察
2. Node Invariant（节点不变量）
3. 核心状态
4. 简短正确性证明
5. Python 模板
6. 时间与空间复杂度
7. 代表题目
8. 与其他 Pattern 的区别

特别回答：

- 为什么 Trie 可以共享前缀？
- 为什么 prefix 存在不代表 word 存在？
- 为什么 DFS 中不存在某个 child 就可以剪枝？
- 为什么 Word Search II 使用 Trie 比逐词暴力搜索更有优势？
- 什么情况下 Trie 反而没有 Hash Set 或 Sorting 简单？
- Trie 节点数量与输入字符总数是什么关系？
- 为什么 Trie 的空间复杂度不能简单说成 O(1)？
- 为什么 Trie + DP 不意味着 DP 被 Trie 取代？

避免冗长、重复和空泛解释。

==================================================
十二、P0 / P1 / P2 优先级
==================================================

P0：
核心必练，必须熟练理解与实现。

P1：
重要变体，掌握核心思想和可迁移技巧。

P2：
低优先级、跨专题或特殊进阶。

P0：

LC-0208 - Implement Trie (Prefix Tree)
LC-0211 - Design Add and Search Words Data Structure
LC-0212 - Word Search II

P1：

LC-0648 - Replace Words
LC-1268 - Search Suggestions System
LC-2416 - Sum of Prefix Scores of Strings

P2：

LC-1233 - Remove Sub-Folders from the Filesystem
LC-3291 - Minimum Number of Valid Strings to Form Target I
LC-0421 - Maximum XOR of Two Numbers in an Array
LC-0014 - Longest Common Prefix
LC-3043 - Find the Length of the Longest Common Prefix
LC-0616 - Add Bold Tag in String

允许根据独立审核适度调整。

但必须解释调整理由。

P0 只设置真正最重要的代表题，
不要为了题目数量把所有题都设为 P0。

README 应包含：

P0：
最小核心必刷路线。

P0 + P1：
标准 Trie 面试准备路线。

P2：
进阶学习与低优先级存档。

==================================================
十三、题目数量与验收
==================================================

根据当前 tree：

原有题目来源文件夹：9 个。

其中：
3 道只有 NC 来源：
208、211、212。

现有不同题目：9 道。

第一轮新增：
648、2416、421。

如果都成功创建：

第一轮预计共有 12 道不同题目。

预期 Level 1 分布：

01：2 道
02：2 道
03：3 道
04：1 道
05：4 道

合计：12 道。

注意：

NC-only 题正式化为 LC，
不是新增不同题目。

如果第二轮新增真正有价值的题，
数量可以合理增加。

如果跨专题题采用索引而非实体目录，
最终实体数量可以不同。

不得为了凑数量制造假文件。

最终必须验证：

1. 所有原始题目均有新位置。
2. 所有原始文件全部保留。
3. 三个 NC-only 题正式化正确。
4. LC 编号与英文题目名称匹配。
5. Trie 分类与实际解法一致。
6. Level 1 / Level 2 / Level 3 编号连续。
7. 所有新题的标准文件完整。
8. 所有额外图片、SVG 和 note 保留。
9. TrieUtils.py 的引用没有被破坏。
10. README 相对路径全部有效。
11. 没有不必要的重复主目录。
12. 旧文件 SHA-256 校验通过。
13. 当前专题外没有任何写入或删除。
14. Git 原有未提交修改没有丢失。
15. 所有失败步骤均有明确记录。

==================================================
十四、实际执行顺序
==================================================

请直接执行：

1. 审计当前目录和 Git 状态。
2. 建立原始文件清单和哈希。
3. 识别 utils 的代码依赖。
4. 验证当前九道题的题号和内容。
5. 检查跨专题重复题目（只读）。
6. 建立 Level 1 / Level 2 结构。
7. 设计并执行安全迁移。
8. 为所有 Level 3 正确编号。
9. 正式整理 LC-208、211、212。
10. 保留完整 NC 来源资料。
11. 新增 LC-648、2416、421。
12. 检查旧题是否缺少标准文件。
13. 独立进行第二轮题库审核。
14. 补充少量高价值遗漏题目。
15. 如有必要，调整分类与排序。
16. 整理 docs 和其他学习资料。
17. 检查 TrieUtils.py 是否正常。
18. 创建根目录和各 Level 1 README。
19. 生成 Pattern Recognition Guide。
20. 验证目录编号连续性。
21. 验证题目文件完整性。
22. 对比迁移前后原始文件哈希。
23. 检查跨专题索引和相对路径。
24. 安全清理已经确认空置的旧目录。
25. 运行最终 tree。
26. 检查最终 Git 状态。
27. 输出完整验收报告。

最终报告需要包含：

- 最终完整 tree
- Level 1 / Level 2 分类
- 所有旧题迁移结果
- NC-only 题正式化结果
- 第一轮新增题目
- 第二轮独立新增题目
- 没有新增的候选及理由
- P0 / P1 / P2 数量
- 跨专题索引
- 原始文件哈希验证
- TrieUtils.py 检查结果
- Git 变更摘要
- 任何失败或未完成的事项
- 最终推荐学习顺序

不要仅仅提供目录规划。

请在全部安全限制内直接执行实际重构。
PROMPT
)"
