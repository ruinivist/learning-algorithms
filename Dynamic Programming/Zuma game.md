# Zuma game

Zuma game is matching consecutive balls of the same color, 3 or more to delete them.
You have some on your hand and can insert anywhere. Min number of moves to win or -1
if not possible.

## Solution

the contraints are a dead giveaway, though initially I was thinking along the lines of an
interval dp. I asked chatgpt if I can be better here and know it for sure without looking
at constraints and it said my guess was not unreasonable so I'll take it.

We have 5 colors, and board and hands are strings.
To define state, I do need the board as it's positioned but hands can just be a Counter.
Then I just place it at any position, get a new board and that's it. It's more of a
recursion + cache + a little bit of set optimisation instead of a proper subset dp for this
problem.

_what does `groupby` do?_

```python
arr = [1, 1, 1, 2, 2, 3, 3, 3, 4]

1 -> [1, 1, 1]
2 -> [2, 2]
3 -> [3, 3, 3]
4 -> [4]

so an iteration is like
for elem (1), iterator over ( [1,1,1] )

note that you cant do len(iterator), instead do len(list(iterator)) to materialise it
```

As a pruning optimisation, it makes sense to only insert at the start of a same color group.

But a case exists where this leads to chainr reaction that deletes part of a long chain too fast
that should otherwise be done later.
board = "RRWWRRBBRR" and hand = "WB"
by breaking any of the W or B at the first step, you are left with stranged Rs of len 2.

These two pruning steps are essential.

```python
import math
from functools import cache
from itertools import groupby


class Solution:
    def findMinStep(self, board: str, hand: str) -> int:
        def clean(s: str) -> str:
            """Repeatedly remove consecutive groups of 3 or more balls."""
            # this can ofc be written better but no need to worry
            # of correctness in such an impl
            while True:
                norm = "".join(
                    "".join(group_l)
                    for _, group in groupby(s)
                    if len(group_l := list(group)) <= 2
                )
                if len(norm) == len(s):
                    return norm
                s = norm

        @cache
        def f(b: str, h: str) -> float:
            if not b:
                return 0
            if not h:
                return math.inf

            ans = math.inf

            for j, col in enumerate(h):
                # don't try same color
                if j > 0 and h[j] == h[j - 1]:
                    continue

                next_h = h[:j] + h[j + 1 :]

                for i in range(len(b) + 1):
                    # as a pruning step, we ONLY want to insert
                    # at the start of a same color group
                    pick = False
                    if i < len(b) and b[i] == col:
                        pick = True

                    # IMP: it's not best to ALWAYS match to the
                    # current group, we also need to insert between
                    # two identical balls of same color to prevent
                    # an early collapse of some long branch
                    if 0 < i < len(b) and b[i-1] == b[i]:
                        pick = True

                    if pick:
                        nb = clean(b[:i] + col + b[i:])
                        ans = min(ans, 1 + f(nb, next_h))

            return ans

        # sort so that identical Counters are the same cache key
        ans = f(board, "".join(sorted(hand)))
        return -1 if ans == math.inf else ans
```
