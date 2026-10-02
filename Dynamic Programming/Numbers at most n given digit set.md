# Numbers at most n given digit set

Set of digits given, no 0 in them. Can repeat.
Count number of digits made from that set such that they are <= n.

## Solution

as obvious of a digit dp problem as it can be.

```python
class Solution:
    def atMostNGivenDigitSet(self, digs: list[str], n: int) -> int:
        lte = list(map(int, str(n)))
        digs = list(map(int, digs))

        @cache
        def f(i, match, lz):
            if i == len(lte):
                return 1 if not lz else 0  # cannot be all 0

            ans = 0
            lim = len(digs) if not match else bisect_right(digs, lte[i])
            for j in range(lim):
                d = digs[j]
                nmatch = match and d == lte[i]
                ans += f(i + 1, nmatch, False)

            # or we continue the current leading zero
            # since no 0 in set, match is always false here
            if lz:
                ans += f(i + 1, False, True)

            return ans

        return f(0, True, True)

```

I missed the leading 0 handling initially.
