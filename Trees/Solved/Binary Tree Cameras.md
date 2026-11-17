# Binary Tree Cameras

A node covers all at 1 hop. What is min number of nodes needed to cover it all?
No restrictions on placement.

## The dp solution

```python
class Solution:
    def minCameraCover(self, root: TreeNode | None) -> int:
        def f(root):
            # retvals are (cam at u, no cam at u but covered, no cam and not covered )
            if not root:
                # placing a cam is invalid state
                # not placing a cam is free
                return (inf, 0, 0)

            l0, l1, l2 = f(root.left)
            r0, r1, r2 = f(root.right)

            # place cam
            # don't care about the placements, just let the dp handle it
            a0 = 1 + min(l0, l1, l2) + min(r0, r1, r2)

            # not place cam but THIS is covered
            # cam MUST be at ONE child and toher must be covered
            a1 = min(l0 + min(r0, r1), r0 + min(l0, l1))

            # not covered at all, childen must be covered
            a2 = l1 + r1

            return a0, a1, a2

        ret = f(root)
        return min(ret[0], ret[1])
```

## Greedy sol

> TODO, but I don't think it really brings much to the table here
