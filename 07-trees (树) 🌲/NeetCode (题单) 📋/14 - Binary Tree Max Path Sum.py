from TreeNode import TreeNode

from typing import Optional

"""
于是对每个节点,有两个量:

① 拐弯路径(以本节点为最高点的完整路径)= 左↓ + 本节点 + 右↓。
这是一条完整的路径(可以左右都伸),所以它有资格更新全局答案 res。但它已经在这里拐弯了,没法再往上接到父亲(接上去就分叉/重复了)。

② 上传路径 = 本节点 + max(左↓, 右↓)(只能挑一边)。
这是"从本节点出发、一路向下、只走一个方向"的最优链。只有这种不拐弯的链,父亲才能接着它继续往上延伸。 所以 dfs 返回的是 ②。

关键点:dfs 返回 ② 给父亲用,但每到一个节点都顺手用 ① 更新答案。 因为答案的那条路径,它的最高点是某个具体节点——我们就在那个节点用 ① 把它记下来。图里答案 42 就是在节点 20 用 ① 记下的,而 20 只把 35(②)传给了父亲 -10。

为什么 max(leftMax, 0)?

dfs(child) 返回的是子树"最优向下链"。如果这个值是负的,说明往那边伸只会拖低总和 —— 那还不如不要这条分支。max(…, 0) 就是"这一边如果是负的,就当成 0(不走)"。节点值可以是负数,所以这一步很关键。(图里的例子恰好都是正的,看不出效果;但如果某个孩子返回 -5,这里就会用 0。)
"""

class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        res = [root.val]

        def dfs(root):
            if not root:
                return 0

            leftMax = max(dfs(root.left), 0)
            rightMax = max(dfs(root.right), 0)

            res[0] = max(res[0], root.val + leftMax + rightMax)
            return root.val + max(leftMax, rightMax)

        dfs(root)
        return res[0]
