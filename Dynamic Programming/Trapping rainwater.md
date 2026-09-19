# Trapping rainwater

It is more closer to two pointers, in style, but we do keep accumulated state info
so fine ig.

The key idea is that you solve for $f(l,r)$,
if $height(l) < height(r)$ then the water in this column is bounded by the left max,
otherwise it's the right max.
You would want to move pointers such that you always move the smaller one since it
contributes nothing to the "holding of water", the level would be contrained by other cols.

```python
class Solution:
    def trap(self, h: list[int]) -> int:
        l_max, r_max = 0, 0
        l, r = 0, len(h) - 1

        ans = 0
        while l <= r:
            if h[l] < h[r]:
                l_max = max(l_max, h[l])
                ans += l_max - h[l]
                l += 1
            else:
                r_max = max(r_max, h[r])
                ans += r_max - h[r]
                r -= 1

        return ans
```

Rem

- think of the case where this col advances `l_max`, 0 water would be stored
