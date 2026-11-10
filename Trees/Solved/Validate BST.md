# Validate BST

There are three ways we can solve this, refer to the 3 necessary and sufficient conditions in [notes](../Trees.mdx)

Way 1: bottom up to get lmax and rmins

```python

class Solution:
    def isValidBST(self, root):
        def dfs(node):
            if not node:
                return (True, inf, -inf)

            left_ok, left_min, left_max = dfs(node.left)
            right_ok, right_min, right_max = dfs(node.right)

            if not left_ok or not right_ok or (left_max < node.val < right_min):
                return (False, 0, 0)

            return (
                True,
                min(left_min, node.val),
                max(right_max, node.val)
            )

        return dfs(root)[0]
```

Way 2: inorder traversal

Keep track of a previous and just check if the inorder traversal is good.

```python
class Solution:
    def isValidBST(self, root: TreeNode | None) -> bool:
        prev = -inf
        ok = True
        def f(root):
            nonlocal prev, ok
            if not root:
                return

            f(root.left)

            if prev >= root.val:
                ok = False
                return

            prev = root.val

            f(root.right)

        f(root)
        return ok
```

Way 3: Parent enforced bounds

The idea is a bit non-trivial but impl really shines here

```python
class Solution:
    def isValidBST(self, root: TreeNode | None) -> bool:
        def f(root, l, r) -> bool:
            if not root:
                return True

            if not l < root.val < r:
                return False

            return f(root.left, l, root.val) and f(root.right, root.val, r)

        return f(root, -inf, inf)
```
