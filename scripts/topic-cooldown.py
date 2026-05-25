#!/usr/bin/env python3
"""topic-cooldown — refuse repeating the same primary keyword too soon.

Audience-burnout guard. Before writing a new article, scan the recent drafts
directory and compare the proposed primary keyword against keywords used in
the last N days. Warn/fail if the same one comes up too fast.

Match logic:
  - case-insensitive
  - simple string equality on `keywords.primary` slug-normalized
  - Hungarian diacritics stripped before compare (á→a, é→e, etc.) — same
    as the marva-blog-author slug algorithm

Exit codes:
  0  — no recent overlap, safe to write
  1  — overlap detected inside cooldown window
  2  — usage / parse error

Run as:
  scripts/topic-cooldown.py --primary "rare-earth halt"
  scripts/topic-cooldown.py --primary "AI compute price war" --cooldown-days 21
  scripts/topic-cooldown.py --primary "stablecoins" --drafts-dir ~/Documents/cue/drafts
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from datetime import datetime, timedelta, timezone
from pathlib import Path

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
DATE_KEY_RE = re.compile(r"^date:\s*(\d{4}-\d{2}-\d{2})", re.MULTILINE)
PRIMARY_KEY_RE = re.compile(r"^\s*primary:\s*\"?([^\"\n]+?)\"?\s*$", re.MULTILINE)
SECONDARY_RE = re.compile(r"^\s*secondary:\s*\[([^\]]*)\]", re.MULTILINE)


def normalize(s: str) -> str:
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def parse_draft(path: Path) -> dict | None:
    text = path.read_text()
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    fm = m.group(1)

    date_m = DATE_KEY_RE.search(fm)
    if not date_m:
        return None
    try:
        date = datetime.strptime(date_m.group(1), "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return None

    primary_m = PRIMARY_KEY_RE.search(fm)
    primary = normalize(primary_m.group(1)) if primary_m else None

    sec_m = SECONDARY_RE.search(fm)
    secondary = []
    if sec_m:
        for tok in sec_m.group(1).split(","):
            tok = tok.strip().strip("\"'")
            if tok:
                secondary.append(normalize(tok))

    return {"path": path, "date": date, "primary": primary, "secondary": secondary}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--primary", required=True, help="proposed primary keyword for the new article")
    ap.add_argument("--cooldown-days", type=int, default=14)
    ap.add_argument("--drafts-dir", type=Path, default=Path.home() / "Documents/cue/drafts")
    ap.add_argument("--warn-only", action="store_true", help="never fail (exit 0), just print warnings")
    args = ap.parse_args()

    proposed = normalize(args.primary)
    if not proposed:
        print(f"could not normalize: {args.primary!r}", file=sys.stderr)
        return 2

    cutoff = datetime.now(tz=timezone.utc) - timedelta(days=args.cooldown_days)

    if not args.drafts_dir.exists():
        print(f"drafts dir not found: {args.drafts_dir}", file=sys.stderr)
        return 2

    hits_primary = []
    hits_secondary = []
    for md in sorted(args.drafts_dir.glob("*.md")):
        draft = parse_draft(md)
        if not draft or draft["date"] < cutoff:
            continue
        if draft["primary"] == proposed:
            hits_primary.append(draft)
        elif proposed in draft.get("secondary", []):
            hits_secondary.append(draft)

    print(f"topic-cooldown  →  primary={proposed!r}  cooldown={args.cooldown_days}d")

    if not hits_primary and not hits_secondary:
        print(f"  no overlap inside window. safe to write.")
        return 0

    if hits_primary:
        print(f"\n  primary keyword RECENTLY used in {len(hits_primary)} draft(s):", file=sys.stderr)
        for h in hits_primary:
            age = (datetime.now(tz=timezone.utc) - h["date"]).days
            print(f"    ✗ {h['path'].name}  ({age}d ago)", file=sys.stderr)

    if hits_secondary:
        print(f"\n  secondary mentions in {len(hits_secondary)} draft(s) (lower severity):")
        for h in hits_secondary:
            age = (datetime.now(tz=timezone.utc) - h["date"]).days
            print(f"    · {h['path'].name}  ({age}d ago)")

    if args.warn_only:
        print(f"\n--warn-only: not failing.")
        return 0

    if hits_primary:
        print(f"\ntopic-cooldown FAILED — primary repeats inside {args.cooldown_days}d. Pick a fresh angle, increase --cooldown-days, or pass --warn-only.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
