# Stickers to Spell Word

Make a subset with infinite possible duplicates and then if I can make a given string from
the character set I have, that's a valid choice. Smallest count of elems in subset.

## Problem

n is 50 here, but target is 15. It hints at either a bitmask dp involving target or some meet
in the middle like approach.

The approach goes like, for all masks, for all stickers, apply ticker to mask and push.
There is no need to worry about duplicate stickers since the inner loop running again will pick
it up the next time. A recursive is similar.

```python
class Solution:
    def minStickers(self, stickers: list[str], target: str) -> int:
        n = len(target)
        full = (1 << n) - 1
        counts = list(map(Counter, stickers))

        @cache
        def f(mask: int) -> int:
            if mask == full:
                return 0

            ans = inf

            for sticker in counts:
                chars = sticker.copy()
                new_mask = mask

                for i, ch in enumerate(target):
                    if not mask & (1 << i) and chars[ch]:
                        new_mask |= 1 << i
                        chars[ch] -= 1

                if new_mask != mask:
                    ans = min(ans, 1 + f(new_mask))

            return ans

        return -1 if (ans := f(0)) == inf else ans
```

## What if repetition was not allowed?

Had it been iterative the loop order for mask -> for sticker would switch to for sticker ->
for mask, so you process each sticker once per mask.`

```python
class Solution:
    def minStickers(self, stickers: list[str], target: str) -> int:
        n = len(target)
        full = (1 << n) - 1
        counts = list(map(Counter, stickers))

        @cache
        def f(i: int, mask: int) -> int:
            if mask == full:
                return 0

            if i == len(stickers):
                return inf

            # don't use sticker i
            ans = f(i + 1, mask)

            # use sticker i
            chars = counts[i].copy()
            new_mask = mask

            for j, ch in enumerate(target):
                if not mask & (1 << j) and chars[ch]:
                    new_mask |= 1 << j
                    chars[ch] -= 1

            if new_mask != mask:
                ans = min(ans, 1 + f(i + 1, new_mask))

            return ans

        ans = f(0, 0)
        return -1 if ans == inf else ans
```
