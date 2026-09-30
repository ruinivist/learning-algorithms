# Count unique chars in all substrings.

Basically for all substrings t of s, count += len(set(t))
but optimised.

## Solution ( misread )

We are at full lengths, so an (l,r) iteration is not possible ( I think that would've been
easy to do, you could just extend and keep on summing ).

A "contribution" approach probably makes sense, given a character, in how many substrings would
it be present as unique. If it's like i...j...k and I'm at j, then the min i and max k such that
there is no s(j) would be the range, make substrings from it.

But this is also part of larger susbtrings, which j would attribute for those?
Let's say "this" j attributes instead for all the previous, till the first next.

```text
elite
first e => elit
second e => elite
Note that the "e" that attributes MUST be part.
```

```python
class Solution:
    def uniqueLetterString(self, s: str) -> int:
        n = len(s)
        pos = defaultdict(list)
        for idx, ch in enumerate(s):
            pos[ch].append(idx)
        for ch in pos:
            pos[ch].append(n)

        ans = 0
        for ch, pos_ch in pos.items():
            for i in range(0, len(pos_ch) - 1):
                cur, till = pos_ch[i], pos_ch[i + 1]
                # 0...cur...till
                ans += (cur + 1) * (till - cur)

        return ans
```

## Solution

count unique is count of characters that apper ONLY once, so for ABA it's 1 as opposed to the
size of set(AB) = 2.

But then it'll be easy to modify as I just need to handle a "prev" handling in my solution.

```python
class Solution:
    def uniqueLetterString(self, s: str) -> int:
        n = len(s)
        pos = defaultdict(list)
        for idx, ch in enumerate(s):
            pos[ch].append(idx)
        for ch in pos:
            pos[ch] = [-1] + pos[ch] + [n]

        ans = 0
        for _, pos_ch in pos.items():
            for i in range(1, len(pos_ch) - 1):
                prev, cur, till = pos_ch[i - 1 : i + 2]
                # (prev...cur...till)
                ans += (cur - prev) * (till - cur)
            print(ans)

        return ans
```
