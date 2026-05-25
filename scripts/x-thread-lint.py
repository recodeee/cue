#!/usr/bin/env python3
"""x-thread-lint — validate an X (Twitter) thread before it goes to Postiz.

Enforces two upstream-X constraints that Postiz surfaces as nonRetryable failures:

  1. Max 280 chars per tweet (standard tier).
  2. Max ONE $TICKER cashtag per tweet.

Input shapes accepted:
  - Postiz JSON payload:   posts[0].value[].content
  - Markdown thread file:  tweets separated by lines starting with "## Tweet"
  - Plain text file:       tweets separated by a blank line + "---" line

Exit codes:
  0  — all tweets pass
  1  — at least one tweet fails a rule
  2  — usage / parse error

Run as:
  scripts/x-thread-lint.py drafts/foo.json
  scripts/x-thread-lint.py drafts/foo-thread.md
  scripts/x-thread-lint.py --max-chars 280 drafts/foo.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CASHTAG_RE = re.compile(r"\$[A-Z]{2,10}\b")


def tweets_from_postiz_json(path: Path) -> list[str]:
    data = json.loads(path.read_text())
    posts = data.get("posts") or []
    if not posts:
        raise ValueError("postiz JSON has no 'posts' array")
    return [v["content"] for v in posts[0].get("value", []) if v.get("content")]


def tweets_from_markdown(path: Path) -> list[str]:
    text = path.read_text()
    chunks = re.split(r"\n## Tweet [^\n]*\n", text)
    out = []
    for chunk in chunks[1:]:
        body = chunk.strip()
        if body.startswith("#"):
            continue
        if body:
            out.append(body)
    if not out:
        chunks = [c.strip() for c in re.split(r"\n---+\n", text) if c.strip()]
        out = chunks
    return out


def load_tweets(path: Path) -> list[str]:
    if path.suffix == ".json":
        return tweets_from_postiz_json(path)
    return tweets_from_markdown(path)


def lint(tweets: list[str], max_chars: int) -> int:
    failures = 0
    for i, body in enumerate(tweets, start=1):
        chars = len(body)
        cashtags = CASHTAG_RE.findall(body)
        too_long = chars > max_chars
        too_many_tags = len(cashtags) > 1
        status = "FAIL" if (too_long or too_many_tags) else "ok"
        flags = []
        if too_long:
            flags.append(f"chars={chars}>{max_chars}")
        if too_many_tags:
            flags.append(f"cashtags={cashtags}")
        suffix = f"  ← {', '.join(flags)}" if flags else ""
        print(f"  T{i:>2}: {chars:>3} chars | {len(cashtags)} cashtag(s) | {status}{suffix}")
        if too_long or too_many_tags:
            failures += 1
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", type=Path)
    ap.add_argument("--max-chars", type=int, default=280)
    args = ap.parse_args()

    if not args.path.exists():
        print(f"file not found: {args.path}", file=sys.stderr)
        return 2

    try:
        tweets = load_tweets(args.path)
    except (ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"parse error: {exc}", file=sys.stderr)
        return 2

    print(f"x-thread-lint  →  {args.path}  ({len(tweets)} tweets, max {args.max_chars} chars/tweet)")
    failures = lint(tweets, args.max_chars)
    if failures:
        print(f"\n{failures} tweet(s) failed — fix before sending to Postiz.", file=sys.stderr)
        return 1
    print("\nall tweets pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
