# Review ranking PoC

Run from this directory:

```sh
uv run --env-file .env main.py fetch
uv run main.py rank
uv run main.py rank --top 20
uv run main.py rank --topic "Dynamic Programming"
uv run main.py check
```

For a new checkout, copy `.env.example` to `.env` and set `LEETCODE_SESSION`.
Fetching gets each annotated problem's full available history and replaces
`submissions.json` only after every page succeeds. Ranking works offline and writes `ranking.md`;
without a cache, automatic scores default to zero. Fetch again after adding new
problem notes.

Notes use YAML front matter with `leetcode_url` and an optional integer `rating`.
Omit `rating` for zero. The note's top-level folder supplies its topic.

Priority is `a + rating`, with higher scores first:

```text
a = 6 * min(age / interval, 1) + 4 * recent_struggle
```

Only finalized submissions dated **1 January 2026 or later**, through today,
count. Dates use UTC; pending submissions are excluded. Older records
may remain in the cache but do not affect any score or report count.

- `age`: days since the last acceptance, or the latest attempt if never accepted.
- `recent_struggle`: the weighted average of each practice day's fraction of
  failed submissions. Each day contributes once, with its weight halving every
  90 days; a day with many retries cannot outweigh several practice days.
- `interval`: starts at 14 days. Each subsequent accepted day at least 14 days
  after the previous accepted day adds `14 * weight` days, capped at 90 days.
  Success weights also halve every 90 days, so older successes offer less credit.

No eligible history means `a = 0`. Calendar days approximate practice sessions;
these weights are a starting heuristic rather than a measured prediction of recall.

The source, setup instructions, and uv lockfile are tracked in Git. Credentials,
personal submission history, generated rankings, and local Python caches are ignored.
