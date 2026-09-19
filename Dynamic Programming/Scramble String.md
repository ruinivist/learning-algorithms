# Scramble String

the problem statement itself makes it an obvious recursion, imagine a tree like
this

```
                    great
                   /     \
                 gr       eat
                /  \     /   \
               g    r   e     at
                             /  \
                            a    t
```

Instead you just try to convert string a to b by applying the break at some index
and swap operation.

Define $f(a, b) = \text{can I convert a to b by scrambling?}$

Then you can for each position, do the break and recurse into both states, swapped or
non-swapped. The only remaining challenge is the states, since I can't just put the
entire string in args.

Well, one of the condition to be scrambled is that length MUST match, so what I can do
is just use the starting indexes and the len making $(i_1,i_2,len)$ as my state.

```python
from functools import cache

class Solution:
    def isScramble(self, s1: str, s2: str) -> bool:
        @cache
        def f(i1, i2, l):
            if l == 1:
                return s1[i1] == s2[i2]

            for j in range(l-1):
                # no swap case
                # [i1...i1+j] and [i2...i2+j]
                a = f(i1,i2,j+1) and f(i1+j+1,i2+j+1,l-j-1)
                # swap case
                # [i1...i1+j] compared to [i2+l-j-1]
                b = f(i1,i2+l-j-1,j+1) and f(i1+j+1,i2,l-j-1)

                if a or b:
                    return True
            return False

        return f(0,0,len(s1))
```
