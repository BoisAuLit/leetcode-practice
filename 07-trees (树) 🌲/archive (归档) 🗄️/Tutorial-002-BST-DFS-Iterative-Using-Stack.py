from TreeNode import TreeNode


class DFS_Iterative:
    # ! Left -> Root -> Right
    # ! Expecting "H D I B J E K A L F M C N G O"
    def inorder(self, root: TreeNode):
        stack = []
        curr = root
        result = []
        while stack or curr:
            while curr:
                stack.append(curr)
                curr = curr.left
            curr = stack.pop()
            print(curr.val, end=" ")
            result.append(curr.val)
            curr = curr.right
        return result

    # # ! Root -> Left -> Right
    # # ! Expecting "A B D H I E J K C F L M G N O"
    def preorder(self, root: TreeNode):
        if not root:
            return []
        result = []
        stack = [root]
        while stack:
            node = stack.pop()
            result.append(node.val)
            print(node.val, end=" ")
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        return result

    # # ! Left -> Right -> Root
    # # ! Expecting "H I D J K E B L M F N O G C A"
    def postorder(self, root: TreeNode):
        if not root:
            return []
        result = []
        stack = [root]
        while stack:
            node = stack.pop()
            result.append(node.val)
            # print(node.val, end=" ")
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        return result[::-1]


s = DFS_Iterative()

treeNode = TreeNode.from_list(
    ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]
)
print("Original tree:")
treeNode.printTree()

print("\nInorder Traversal:   ", end=" ")
s.inorder(treeNode)

print("\nPreorder Traversal:  ", end=" ")
s.preorder(treeNode)

print("\nPostorder Traversal: ", end=" ")
result = s.postorder(treeNode)
print(result)
