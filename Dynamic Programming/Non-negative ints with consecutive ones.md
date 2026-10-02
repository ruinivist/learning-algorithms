---
leetcode_url: https://leetcode.com/problems/non-negative-integers-without-consecutive-ones/
---

# Non-negative ints with consecutive ones

Count of ints in [0,n] such that binary rep has no consuecitve 1s.

## Solution

n is really large in this, so I feel like there is just some clever pattenr to observe.
A naive dp way is to solve like digit dp, except in binary.

Well, actually this is indeed correct, I missed that this in "digits" would just be 32.

```python
class Solution:
    def findIntegers(self, n: int) -> int:
        # bin gives a string with 0b prefix so remove that
        s = bin(n)[2:]

        @cache
        def f(i, prev, match):
            if i == len(s):
                return 1

            digit = int(s[i])
            limit = digit if match else 1

            ans = 0
            for x in range(limit + 1):
                if prev == 1 and x == 1:
                    continue

                n_match = match and (x == digit)
                ans += f(i + 1, x, n_match)

            return ans

        return f(0, 0, True)
```

An alternative is to make it into linear dp on binary strings, notice that it's fibonacci
numbers and then get the needed one in log time, via some matrix exponentiation equivalent.
But that's too much magic.
