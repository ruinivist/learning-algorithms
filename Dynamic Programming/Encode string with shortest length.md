# Encode string with shortest length

this is just run length encoding of a string.

given a string s, encode it as k[t] meaning that s = t repeated k times
O(n^3) is expected for the solution, n being the string length

**you can encode recursively** so 5[ab]10[xy] is possible

## Solution

The recursive encoding is what makes the problem challenging else you can just
brute force every length.

If you can imagine that you have a f(l,r) that can return the encoded string for
that substring; then the whole problem you can split as an interval dp, by trying
to split at every k.

What are the transitions then? The tricky part is how do you merge and it what do you
return from f.

I was initially thinking along these lines, that the dp should return a list of [(n1,rep1),...]
so that I can merge cases like (1,abc) and 3(abc) => last from left and first from right as
(4,abc) but that explodes my state a lot. This can work but then in the O(n) loop inside of
the interval, I would also need to match the last and first strings, another potential O(n).
I can do substring hashing but let's avoid that.

The trick to the problem is using k only as a concat boundary, you assume that the optimal
recursion path would not split across an encoding, since we try all paths that is valid. But then
we need to handle full string encodings.

This is what one more transition gets you. For each period p, if this period can cover the whole
string, use that. To answer this efficiently you need an lcp precomputed.
KMP/z-algo can do this as well but let's avoid that.
if len(lcp(s[l], s[l+p])) >= len of this range - p, then p is a valid period.

```python
from functools import cache


class Solution:
    def encode(self, s: str) -> str:
        n = len(s)

        # lcp[i][j] = longest common prefix of s[i:] and s[j:]
        lcp = [[0] * (n + 1) for _ in range(n + 1)]

        for i in range(n - 1, -1, -1):
            for j in range(n - 1, i, -1):
                if s[i] == s[j]:
                    lcp[i][j] = 1 + lcp[i + 1][j + 1]

        @cache
        def f(l, r):
            length = r - l + 1

            # leave raw
            best = s[l:r + 1]

            # split
            for k in range(l, r):
                cand = f(l, k) + f(k + 1, r)

                if len(cand) < len(best):
                    best = cand

            # repeat whole interval
            for p in range(1, length):
                if length % p != 0:
                    continue

                # period p means:
                # s[l:r-p+1] == s[l+p:r+1]
                if lcp[l][l + p] >= length - p:
                    count = length // p
                    cand = f"{count}[{f(l, l + p - 1)}]"

                    if len(cand) < len(best):
                        best = cand

            return best

        return f(0, n - 1)
```
