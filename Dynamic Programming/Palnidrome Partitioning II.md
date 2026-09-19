# Palindrome Partitioning II

You can just keep on extending ranges and minimising over the cuts, a fast
palindrome check is needed but that you can pre-process.

It's overall a simple problem, just remeber to handle that cuts are 1 less
than the number of partitions, so need to handle for that. Easiest way for that
is to count number of partitions and then just subtract 1.

```python
from functools import cache


class Solution:
    def minCut(self, s: str) -> int:
        n = len(s)
        pal = [[0] * n for _ in range(n)]
        for l in range(1, n + 1):
            for i in range(n - l + 1):
                j = i + l - 1
                if l == 1:
                    pal[i][j] = 1
                    continue
                # s(i) and s(j) should match
                # and the i+1...j-1 should be palindrom
                inner = l == 2 or pal[i + 1][j - 1]
                pal[i][j] = inner and s[i] == s[j]

        # min cuts for making the suffix from i a palin
        @cache
        def f(i):
            nonlocal pal, n
            if i == n:
                # must have been some cut at n-1 to get here
                return 0
            ans = n
            # ans = min: for j where i..j is palin => 1 + f(j+1)
            for j in range(i, n):
                if pal[i][j]:
                    ans = min(ans, 1 + f(j + 1))

            return ans

        return f(0)-1
```
