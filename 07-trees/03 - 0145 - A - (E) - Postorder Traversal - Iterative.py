class Solution:
    def postorderTraversal(self, root):
        result = []
        stack = []
        curr = root
        while curr or stack:
            if curr:
                result.append(curr.val)
                stack.append(curr)
                curr = curr.right
            else:
                curr = stack.pop()
                curr = curr.left
        return result[::-1]
