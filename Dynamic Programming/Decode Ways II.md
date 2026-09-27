# Decode Ways II

You havea lossy encoding. A -> ord(A) = 1, also \* = any from 1 to 9 ( not 0 ).
Given the encoding, count number of possible original messages.

## Solution

I think it's just break at suffix and count number of ways at that end.
Should be a simple cached recursion.

```python
class Solution:
    def numDecodings(self, s: str) -> int:
        n = len(s)

        splits = [str(i) for i in range(1, 27)]
        mod = int(1e9 + 7)

        def startswith(t, pos):
            if pos + len(t) > len(s):
                return False
            return all(
                ch == s[pos + idx] or (s[pos + idx] == "*" and ch != "0")
                for idx, ch in enumerate(t)
            )

        @cache
        def f(pos):
            if pos == n:
                return 1

            # what all num sequences can I break at
            # 1...26 is one, * is another
            ans = 0
            for sp in splits:
                if startswith(sp, pos):
                    np = pos + len(sp)
                    ans += f(np)
                    ans %= mod

            return ans

        return f(0)
```

I really like python for how elegant it makes this, albeit slower ( which is fine for optimisation leading to cancer
should not be something you throw in everywhere )
