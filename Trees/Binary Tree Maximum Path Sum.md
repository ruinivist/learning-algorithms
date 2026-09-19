# Binary Tree Maximum Path Sum

it's the classic one where you optimise over a global and return needed stuff from
recursion

What I want to return is the max path starting from current node into the left subtree
and the right subtree.

Idea being that there MUST be some PEAK of the node, and if you then merge the paths
in left and right for that peak you have the solution. What I'm doing with this global
max is just iteration over that peak.

```python
class Solution:
    def maxPathSum(self, root: TreeNode | None) -> int:
        ans = -math.inf

        def f(root):
            nonlocal ans
            if not root:
                return 0
            # "peak" as this is always included so child paths
            # can be empty
            lpath = max(0, f(root.left))
            rpath = max(0, f(root.right))

            ans = max(ans, lpath + rpath + root.val)
            return root.val + max(lpath, rpath)

        f(root)

        return ans
```
