"""Fetch LeetCode history and rank algorithm notes for review.
Used by this local uv project's fetch, rank, and check commands.
"""

import argparse
import json
import os
import re
import tempfile
import time
from collections import defaultdict
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlsplit
from urllib.request import Request, urlopen

import yaml

# ---------- Settings ----------

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CACHE = HERE / "submissions.json"
REPORT = HERE / "ranking.md"
HISTORY_START = date(2026, 1, 1)
PAGE_SIZE = 20


# ---------- Submission history ----------


def write_atomic(path, content):
    with tempfile.NamedTemporaryFile(
        mode="w", dir=HERE, encoding="utf-8", delete=False
    ) as file:
        temporary = Path(file.name)
        try:
            file.write(content)
            file.close()
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)


def fetch():
    """Collect all submission pages for each problem note before replacing the cache.
    Used by fetch; credentials and submitted code are never cached.
    """
    session = os.environ.get("LEETCODE_SESSION")
    if not session:
        raise ValueError(
            "Missing LEETCODE_SESSION; use uv run --env-file .env main.py fetch."
        )
    slugs = sorted({note["slug"] for note in notes()})
    if not slugs:
        raise ValueError("No problem notes found.")
    query = """query history($slug: String!, $offset: Int!, $limit: Int!, $lastKey: String) {
      questionSubmissionList(questionSlug: $slug, offset: $offset, limit: $limit, lastKey: $lastKey) {
        hasNext lastKey submissions { id timestamp statusDisplay }
      }
    }"""
    submissions = {}
    for index, slug in enumerate(slugs, 1):
        offset, lastkey = 0, None
        while True:
            params = urlencode(
                {
                    "query": query,
                    "variables": json.dumps(
                        {
                            "slug": slug,
                            "offset": offset,
                            "limit": PAGE_SIZE,
                            "lastKey": lastkey,
                        }
                    ),
                }
            )
            request = Request(
                "https://leetcode.com/graphql/?" + params,
                headers={
                    "Cookie": "LEETCODE_SESSION=" + session,
                    "User-Agent": "Mozilla/5.0",
                    "Referer": f"https://leetcode.com/problems/{slug}/submissions/",
                    "Accept": "application/json",
                },
            )
            for attempt in range(3):
                try:
                    with urlopen(request, timeout=30) as response:
                        response_data = json.load(response)
                    break
                except HTTPError as error:
                    if error.code not in {403, 429, 500, 502, 503, 504} or attempt == 2:
                        raise
                    retry_after = error.headers.get("Retry-After", "")
                    delay = (
                        int(retry_after)
                        if retry_after.isdigit()
                        else 2 ** (attempt + 1)
                    )
                    if delay > 60:
                        raise
                    print(
                        f"HTTP {error.code}; retrying the same page in {delay}s",
                        flush=True,
                    )
                    time.sleep(delay)
            if response_data.get("errors"):
                raise ValueError("LeetCode: " + response_data["errors"][0]["message"])
            page = response_data["data"]["questionSubmissionList"]
            if not isinstance(page, dict):
                raise TypeError(f"No authenticated submission history for {slug}.")
            records, has_next = page.get("submissions"), page.get("hasNext")
            if not isinstance(records, list) or type(has_next) is not bool:
                raise ValueError(
                    "Unexpected LeetCode response; existing cache preserved."
                )
            previous_count = len(submissions)
            for record in records:
                submission_id = str(record["id"])
                timestamp, status = int(record["timestamp"]), record["statusDisplay"]
                if timestamp <= 0 or not isinstance(status, str):
                    raise ValueError(
                        "Invalid submission record; existing cache preserved."
                    )
                submissions[submission_id] = {
                    "id": submission_id,
                    "slug": slug,
                    "timestamp": timestamp,
                    "status": status,
                    "pending": status in {"Pending", "Judging", "Waiting"},
                }
            if not has_next:
                break
            if len(submissions) == previous_count:
                raise ValueError(
                    "Pagination made no progress; existing cache preserved."
                )
            offset += len(records)
            lastkey = page.get("lastKey")
            time.sleep(0.5)
        print(
            f"[{index}/{len(slugs)}] {slug}: {offset + len(records)} submissions ({len(submissions)} total)",
            flush=True,
        )
        time.sleep(0.5)
    data = {
        "fetched_at": datetime.now(UTC).isoformat(),
        "problem_slugs": slugs,
        "submissions": list(submissions.values()),
    }
    write_atomic(CACHE, json.dumps(data, indent=2) + "\n")
    print(f"Saved {len(submissions)} submissions to {CACHE.name}")


# ---------- Notes and scoring ----------


def notes():
    for folder in sorted(ROOT.iterdir()):
        if not folder.is_dir() or folder.name.startswith(".") or folder == HERE:
            continue
        for path in sorted(folder.rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            if not text.startswith("---\n"):
                continue
            header, separator, body = text[4:].partition("\n---\n")
            if not separator:
                raise ValueError(
                    f"{path.relative_to(ROOT)}: front matter has no closing delimiter."
                )
            metadata = yaml.safe_load(header)
            if not isinstance(metadata, dict):
                raise TypeError(
                    f"{path.relative_to(ROOT)}: front matter must be a mapping."
                )
            if "leetcode_url" not in metadata:
                continue
            url = metadata["leetcode_url"]
            rating = metadata.get("rating")
            rating = 0 if rating is None else rating
            if type(rating) is not int:
                raise ValueError(
                    f"{path.relative_to(ROOT)}: rating must be an integer."
                )
            parsed = urlsplit(url) if isinstance(url, str) else None
            match = (
                re.fullmatch(r"/problems/([a-z0-9-]+)/?", parsed.path)
                if parsed
                else None
            )
            if not match or parsed.scheme != "https" or parsed.netloc != "leetcode.com":
                raise ValueError(
                    f"{path.relative_to(ROOT)}: invalid canonical leetcode_url."
                )
            title = next(
                (line[2:] for line in body.splitlines() if line.startswith("# ")),
                path.stem,
            )
            yield {
                "title": title,
                "topic": folder.name,
                "path": path.relative_to(ROOT).as_posix(),
                "url": url,
                "slug": match[1],
                "b": rating,
            }


def score(history, today):
    """Calculate review urgency from finalized practice since January 2026.
    Used by ranking and the small offline self-check.
    """
    sessions = defaultdict(list)
    for record in history:
        day = datetime.fromtimestamp(record["timestamp"], UTC).date()
        if not record.get("pending", False) and HISTORY_START <= day <= today:
            sessions[day].append(record["status"])
    accepted_days = sorted(
        day for day, statuses in sessions.items() if "Accepted" in statuses
    )
    submissions = sum(len(statuses) for statuses in sessions.values())
    failures = sum(
        status != "Accepted" for statuses in sessions.values() for status in statuses
    )
    last_accepted = max(accepted_days) if accepted_days else None
    a, age, interval, struggle = 0.0, None, 14.0, 0.0
    if sessions:
        age = (today - (last_accepted or max(sessions))).days
        weights = {day: 0.5 ** ((today - day).days / 90) for day in sessions}
        struggle = sum(
            weights[day]
            * sum(status != "Accepted" for status in statuses)
            / len(statuses)
            for day, statuses in sessions.items()
        ) / sum(weights.values())
        spaced_successes = sum(
            weights[current]
            for previous, current in zip(accepted_days, accepted_days[1:])
            if (current - previous).days >= 14
        )
        interval = min(90, 14 * (1 + spaced_successes))
        # ponytail: calendar days approximate sessions; use explicit recall results if available.
        a = 6 * min(age / interval, 1) + 4 * struggle
    return {
        "a": a,
        "submissions": submissions,
        "failed": failures,
        "accepted_days": len(accepted_days),
        "last_accepted": last_accepted.isoformat() if last_accepted else "—",
        "age": age,
        "interval": interval,
        "struggle": struggle,
    }


# ---------- Ranking report ----------


def rank(top=None, topic=None):
    cached = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else None
    histories = defaultdict(list)
    for record in cached["submissions"] if cached else []:
        histories[record["slug"]].append(record)
    today = datetime.now(UTC).date()
    rows = []
    for note in notes():
        if topic is not None and note["topic"] != topic:
            continue
        note.update(score(histories[note["slug"]], today))
        note["total"] = note["a"] + note["b"]
        rows.append(note)
    if not rows:
        raise ValueError(
            "No problem notes matched; --topic must match the folder name exactly."
        )
    rows.sort(key=lambda row: (-row["total"], -row["b"], row["path"]))
    if top is not None:
        rows = rows[:top]
    fetched_at = cached["fetched_at"] if cached else "unavailable — a defaults to 0"
    report = [
        "# Problems to review",
        "",
        f"Scored on {today} (UTC). History fetched: {fetched_at}.",
        "",
        "Priority = a + rating. Missing ratings/history default to 0.",
        f"Only finalized submissions from {HISTORY_START} through {today} count (UTC).",
        "a = 6 × min(age / interval, 1) + 4 × recent struggle.",
        "Age is days since last acceptance (latest attempt if never accepted).",
        "A practice session is one calendar day. Recent struggle averages each day's failure fraction",
        "with weights halving every 90 days. Interval starts at 14 days, adds 14 × the decayed weight",
        "of each subsequent successful day at least 14 days after the previous successful day, and caps at 90 days.",
        "Older successes and failures contribute less. No eligible history means a = 0.",
        "",
        "| Rank | Problem | Topic | Total | a | b | Submissions | Failed | Accepted days | Last accepted | Age (days) | Interval (days) | Struggle |",
        "| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: |",
    ]
    print(f"History fetched: {fetched_at}\n")
    print(f"{'#':>3} {'Total':>6} {'a':>6} {'b':>4}  Problem [topic]")
    for index, row in enumerate(rows, 1):
        title = row["title"].replace("|", "\\|").replace("[", "\\[").replace("]", "\\]")
        problem = f"[{title}](../{quote(row['path'])}) · [LC]({row['url']})"
        age = row["age"] if row["age"] is not None else "—"
        report.append(
            f"| {index} | {problem} | {row['topic']} | {row['total']:.2f} | {row['a']:.2f} | {row['b']} "
            f"| {row['submissions']} | {row['failed']} | {row['accepted_days']} | {row['last_accepted']} | {age} "
            f"| {row['interval']:.2f} | {row['struggle']:.2f} |"
        )
        print(
            f"{index:>3} {row['total']:>6.2f} {row['a']:>6.2f} {row['b']:>4}  {row['title']} [{row['topic']}]"
        )
    write_atomic(REPORT, "\n".join(report) + "\n")
    print(f"\nSaved {len(rows)} ranked notes to {REPORT.name}")


# ---------- Command line ----------


def check():
    today = date(2026, 10, 2)

    def attempt(days_ago=0, status="Accepted"):
        date = today - timedelta(days=days_ago)
        return {
            "timestamp": int(
                datetime.combine(date, datetime.min.time(), UTC).timestamp()
            ),
            "status": status,
        }

    fresh = [attempt()]
    assert score([], today)["a"] == 0
    assert score(fresh + fresh, today)["a"] == score(fresh, today)["a"]
    assert (
        score(fresh + [attempt(status="Wrong Answer")], today)["a"]
        > score(fresh, today)["a"]
    )
    assert score([attempt(180)], today)["a"] > score(fresh, today)["a"]
    assert (
        score([attempt(30), attempt(7)], today)["a"] < score([attempt(7)], today)["a"]
    )
    assert score([attempt(10), attempt(status="Wrong Answer")], today)["age"] == 10
    assert score([{**attempt(), "pending": True}], today)["a"] == 0
    print("Scoring self-check passed.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser(
        "fetch", help="Fetch all available submission history using LEETCODE_SESSION."
    )
    ranking = commands.add_parser(
        "rank", help="Rank notes from the local history cache."
    )
    ranking.add_argument("--top", type=int, help="Show only the highest N priorities.")
    ranking.add_argument("--topic", help="Exact top-level folder name.")
    commands.add_parser("check", help="Run the small offline scoring self-check.")
    args = parser.parse_args()
    if args.command == "rank" and args.top is not None and args.top <= 0:
        parser.error("--top must be positive")
    try:
        if args.command == "fetch":
            fetch()
        elif args.command == "rank":
            rank(args.top, args.topic)
        else:
            check()
    except HTTPError as error:
        parser.exit(
            1,
            f"LeetCode returned HTTP {error.code}; check your session/access. Existing cache preserved.\n",
        )
    except (
        OSError,
        URLError,
        ValueError,
        KeyError,
        TypeError,
        yaml.YAMLError,
    ) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
