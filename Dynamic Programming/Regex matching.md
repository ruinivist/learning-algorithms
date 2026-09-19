# Regex matching

If you take note of these things, the solution naturally follows

- string "" matches pattern "a\*" so your exit condition must be on "pattern" ending not string
- the "\*" is to be treated and handled EAGERLY as it's a character pair that we handle in that case

Here's the pseudocode, using **"suffix based"** memoised dp => we go from 0 to n and f(i,j) means suffixes starting from those
positions match

```python
from functools import cache

# suffix based => f(i,j) answers for the suffix
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        sn, pn = len(s), len(p)

        @cache
        def f(si, pi):
            # only pattern, to handle the edge case of string empty but not
            # pattern, emerging from the possible 0 match
            if pi == pn:
                return si == sn

            # first match extracted as common
            firstMatch = si < sn and (s[si] == p[pi] or p[pi] == ".")

            if pi < pn - 1 and p[pi + 1] == "*":
                # match 0
                match = f(si, pi + 2)
                # match atleast one more
                match = match or firstMatch and f(si + 1, pi)
                return match

            return firstMatch and f(si + 1, pi + 1)

        return f(0, 0)
```

a **prefix based** f can be solved as following though note the 2nd check we need due
getting the "\*" first and then looking back

```python
from functools import cache


class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        sn, pn = int(len(s)), int(len(p))

        @cache
        def f(si, pi):
            if pi == -1:
                return si == -1

            curMatch = si >= 0 and (s[si] == p[pi] or p[pi] == ".")

            if pi > 0 and p[pi] == "*":
                prevMatch = si >= 0 and (s[si] == p[pi - 1] or p[pi - 1] == ".")
                # match 0
                match = f(si, pi - 2)
                # match atleast one more
                match = match or prevMatch and f(si - 1, pi)
                return match

            return curMatch and f(si - 1, pi - 1)

        return f(sn - 1, pn - 1)
```

**Look for**

- the base condition
- suffix style
- taking firstMatch out
