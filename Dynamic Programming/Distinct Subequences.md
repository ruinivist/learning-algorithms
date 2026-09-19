# Distinct Subsequences ( Count )

Count of subsequences of s which equal to t

You can define this either on prefix or suffix, I'll use suffix.
$f(i,j) = \text{ways to match on suffix from i and suffix from j}$

Python is so nice that the transitions are just in code.

```python
from functools import cache


class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        sn, tn = len(s), len(t)

        @cache
        def f(si, ti):
            # if the target has ended it's a 1
            if ti == tn:
                return 1
            # optim: if source does not have enough chards, stop
            # early
            if sn - si < tn - ti:
                return 0

            # skip this one
            ans = f(si + 1, ti)
            # take this one if you can
            if s[si] == t[ti]:
                ans += f(si + 1, ti + 1)

            return ans

        return f(0, 0)

```

I initially did as the stop condition on source

```python
# if target has not ended but source has it's a 0
if si == sn:
    return 0
```

but this as an optim prunes more states
