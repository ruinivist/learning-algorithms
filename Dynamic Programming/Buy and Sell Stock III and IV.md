# Buy and Sell Stock III and IV

I think it only makes sense to look at IV first and then III as a compressed
version of the states, otherwise it "looks" like a state machine which it is, I mean
any dp is a state machine, but seems to be "different" when written loosely with
just the 5 state vars.

So I have a timeseries of prices, I can buy and sell upto $k$ times.

_you must sell before you buy, you can only buy 1 unit_
the first gives it the state machine transitions, the second prevents a collapse to global
optima for single purchase.

Solving the actual problem case first, notice the "atmost" as well first.
Let $t$ be which transaction we are on, we can only move forward when we sell. So I would
need both a buy and a sell state.

```python
class Solution:
    def maxProfit(self, k: int, prices: list[int]) -> int:
        # profit on SUFFIX
        @cache
        def f(t, act, day):
            # t -> transction count
            # act -> action to do next
            # day -> index in prices
            if day == len(prices):
                return 0

            # don't do anything
            ans = f(t, act, day + 1)

            if act == "buy" and t + 1 < k:
                ans = max(ans, f(t + 1, "sell", day + 1) - prices[day])
            if act == "sell":
                ans = max(ans, f(t, "buy", day + 1) + prices[day])

            return ans

        return f(0, "buy", 0)
```

You can do some state pruning and write it iteratively but essentially this is the solution.

## What if I can buy MORE than 1 unit?

So this is possible buy -> buy -> sell -> sell.

Note that the "act" can essentially be this "cound of stocks held", this is then 0 or 1 in
the case above, but would be a number in my variation case.

```python
class Solution:
    def maxProfit(self, k: int, prices: list[int]) -> int:
        n = len(prices)

        @cache
        def f(t, held, day):
            # t    -> number of transactions/buys started
            # held -> number of stocks currently held
            # day  -> current day

            if day == n:
                # Every buy must eventually be sold
                return 0 if held == 0 else -math.inf

            # do nothing
            ans = f(t, held, day + 1)

            # BUY
            # Start another transaction even if we're already holding stocks.
            if t < k:
                ans = max(
                    ans,
                    f(t + 1, held + 1, day + 1) - prices[day]
                )

            # SELL
            # Can sell if at least one transaction is currently open.
            if held > 0:
                ans = max(
                    ans,
                    f(t, held - 1, day + 1) + prices[day]
                )

            return ans

        return f(0, 0, 0)
```

## Buy and Sell Stocks III

This just unfolds those loops ( note that in my case, I go the next day as well, here
technically you can do all 4 transaction on the same day but then the result is just 0.

```python
class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        buy1 = -math.inf
        sell1 = 0
        buy2 = -math.inf
        sell2 = 0

        for price in prices:
            buy1 = max(buy1, -price)
            sell1 = max(sell1, buy1 + price)

            buy2 = max(buy2, sell1 - price)
            sell2 = max(sell2, buy2 + price)

        return sell2
```
