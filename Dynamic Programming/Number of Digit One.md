# Number of Digit One

cannot be a more obvious digit dp problem

Initially, I was missing that I needed that "ones" as part of state. I was doing something
more optimised but messed up in suffix counting.

```python
class Solution:
    def countDigitOne(self, n: int) -> int:
        digs = list(map(int, str(n)))

        @cache
        def f(pos, ones, prefix_match):
            if pos == len(digs):
                return ones

            ans = 0
            next_dig = 9 if not prefix_match else digs[pos]
            for d in range(next_dig + 1):
                n_prefix_match = prefix_match and d == next_dig
                ans += f(pos + 1, ones + (d == 1), n_prefix_match)

            return ans

        return f(0, 0, True)
```

The more optimised version

```python
from functools import cache

class Solution:
    def countDigitOne(self, n: int) -> int:
        digs = list(map(int, str(n)))

        @cache
        def f(pos, tight):
            if pos == len(digs):
                return 1, 0  # ways, ones

            limit = digs[pos] if tight else 9

            total_ways = 0
            total_ones = 0

            for d in range(limit + 1):
                next_tight = tight and d == digs[pos]

                ways, ones = f(pos + 1, next_tight)

                total_ways += ways
                total_ones += ones + (d == 1) * ways

            return total_ways, total_ones

        return f(0, True)[1]
```
