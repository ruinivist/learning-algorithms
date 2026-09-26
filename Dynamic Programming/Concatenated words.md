# Concatenated words

for a words list, find all words such they are combination of other words in the list.

## Solution

A solution along the lines of an interval dp is definitely possible, only thing to worry about
is the contraints.

I need to check this for each word so O(n), f(l,r) is O(wl^2) and then the contains check can
be hashed match of O(1)

_Do I need an interval dp?_
And you should ask this when you see one, because here I can also split by prefix so just f(l)
is enough. I split at some prefix which is in wordlist and then check f(suffix).

```python
class Solution:
    def findAllConcatenatedWordsInADict(self, words: list[str]) -> list[str]:
        word_set = set(words)

        ans = []
        for word in words:
            # for word, is suffix from i valid?
            # easier to just return the number of segments
            n = len(word)
            @cache
            def f(i):
                if i == n:
                    return 0

                # so that it's 0 on end or we recurse
                # a no match should not be taken
                splits = -math.inf

                for j in range(i + 1, n+1):
                    if word[i:j] in word_set:
                        splits = max(splits, 1 + f(j))
                return splits

            if f(0) > 1:
                ans.append(word)

            f.cache_clear()

        return ans
```
