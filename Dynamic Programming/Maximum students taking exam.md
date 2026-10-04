# Maximum students taking exam

8x8 grid. "." = seat, "#" = blocked. A student can cheat from left, right,
top left and top right. Max number of students you can set without any cheating.

## Solution

Now this is a good problem because otherwise the idea of doing masking per row is not something
I encounter very often.

Note that f(row, mask) = count if we get to this row and place mask students only depends on the prev row.
So that state compression is also possible if you write an iterative version.

Once the state is decided the rest is easy to implement. You just iterate over the possible previous valid masks
and max over.

```python
class Solution:
    def maxStudents(self, g: list[list[str]]) -> int:
        n, m = len(g), len(g[0])

        @cache
        def f(i, mask):
            if i == -1:
                return 0

            # if the mask itself is invalid, -inf instead of a 0
            for j in range(m):
                setm = mask >> j & 1 == 1
                if setm and g[i][j] == "#":
                    return -inf
                if j > 0:
                    setmleft = mask >> (j - 1) & 1 == 1
                    if setm and setmleft:
                        return -inf

            need_unset = []
            for j in range(m):
                setm = mask >> j & 1 == 1
                if setm:
                    need_unset += [j - 1, j + 1]
            need_unset = list(set(x for x in need_unset if 0 <= x < m))
            need_unset_mask = sum(1 << i for i in need_unset)
            # pmask is 1 where students are
            # need unset mask is 1 where we don't want students to be
            # then if you AND and it still comes out > 0, it means some
            # position matched in both places as a need unset matched with
            # a student there and it is hence invalid

            ans = 0
            for pmask in range(1 << m):
                if pmask & need_unset_mask > 0:
                    continue
                ans = max(ans, f(i - 1, pmask))

            return mask.bit_count() + ans

        return max(f(n - 1, mask) for mask in range(1 << m))
```

Above is what I wrote, though with some more of masking magic, you can get to this.

```python
class Solution:
    def maxStudents(self, g: list[list[str]]) -> int:
        n, m = len(g), len(g[0])

        @cache
        def f(i, mask):
            if i == -1:
                return 0

            # broken seats
            for j in range(m):
                if (mask >> j) & 1 and g[i][j] == "#":
                    return -float("inf")

            # horizontal cheating
            if mask & (mask << 1):
                return -float("inf")

            ans = 0

            for pmask in range(1 << m):
                # diagonal cheating
                if pmask & (mask << 1):
                    continue
                if pmask & (mask >> 1):
                    continue

                ans = max(ans, f(i - 1, pmask))

            return mask.bit_count() + ans

        return max(f(n - 1, mask) for mask in range(1 << m))
```
