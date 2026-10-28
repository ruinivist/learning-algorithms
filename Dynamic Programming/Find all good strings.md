# Find all good strings

Count of strings between s1 and s2 such that they don't contain evil ( given as arg )

## Solutiobn

Digit dp, you can do the combined one where you include both matchHigh and a
matchLow but I rather prefer to do it separate and subtract.

Note that valid strings need to have size n so no leading handling is needed.

Well, I initially misread and missed that the arg evil is an arg, I assume it literally
meant evil and wrote this ( correct to change to arg, which is why the 3 remnants )

```python
class Solution:
    def findGoodStrings(self, n: int, s1: str, s2: str, evil: str) -> int:
        mod = int(1e9 + 7)
        # since I use cache, I put this as global to not cache the strings
        # themeselves
        s = s2

        # usual pos, match and the last 3 char window
        @cache
        def f(pos, match, l3):
            if pos == n:
                return 1

            ans = 0
            lim = ord(s[pos]) if match else ord("z")
            for ch in (chr(x) for x in range(ord("a"), lim + 1)):
                nl3 = (l3 + ch)[-len(evil) :]  # python handles out of bounds clamping
                if nl3 == evil:
                    continue
                nmatch = match and ord(ch) == lim
                ans += f(pos + 1, nmatch, nl3)
                ans %= mod

            return ans

        ans = f(0, True, "")

        f.cache_clear()
        s = s1
        ans -= f(0, True, "")
        # but we also excluded s, instead of doing an s-1, it's easier to just
        # check s1 again
        ans += 1 if evil not in s1 else 0

        ans = (ans % mod + mod) % mod
        return ans
```

Of course this won't float if the string evil is large, so we need to do better here.
