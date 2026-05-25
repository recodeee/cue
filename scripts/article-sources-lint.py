#!/usr/bin/env python3
"""article-sources-lint — verify {#key} in-body refs match `sources:` frontmatter.

Exit codes:
  0  — all sources resolved, no orphan refs, no unused sources (warnings only)
  1  — orphan reference found (in-body {#key} not declared in frontmatter sources:)
  2  — usage / parse error

Run as:
  scripts/article-sources-lint.py drafts/foo.md
  scripts/article-sources-lint.py --strict drafts/foo.md   # also fail on unused sources
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
REF_RE = re.compile(r"\{#([a-z0-9][a-z0-9._-]*)\}")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm_raw = m.group(1)
    body = text[m.end():]

    sources: dict[str, str] = {}
    in_sources = False
    indent = None
    for line in fm_raw.splitlines():
        stripped = line.rstrip()
        if not stripped:
            continue
        if stripped == "sources:" or stripped.startswith("sources:"):
            in_sources = True
            indent = None
            continue
        if in_sources:
            if not line.startswith(" "):
                in_sources = False
                continue
            if indent is None:
                indent = len(line) - len(line.lstrip())
            if len(line) - len(line.lstrip()) < indent:
                in_sources = False
                continue
            entry = line.strip()
            if ":" in entry:
                key, _, value = entry.partition(":")
                key = key.strip()
                if re.match(r"^[a-z0-9][a-z0-9._-]*$", key):
                    sources[key] = value.strip().strip('"').strip("'")
    return {"sources": sources}, body


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", type=Path)
    ap.add_argument("--strict", action="store_true", help="fail on unused sources too")
    args = ap.parse_args()

    if not args.path.exists():
        print(f"file not found: {args.path}", file=sys.stderr)
        return 2

    text = args.path.read_text()
    fm, body = parse_frontmatter(text)
    sources = fm.get("sources", {})

    refs_in_body = REF_RE.findall(body)
    unique_refs = sorted(set(refs_in_body))

    declared = set(sources.keys())
    used = set(unique_refs)

    orphans = used - declared
    unused = declared - used

    print(f"article-sources-lint  →  {args.path}")
    print(f"  declared in frontmatter sources: {len(declared)}")
    print(f"  cited in body {{#key}}:           {len(used)}  ({len(refs_in_body)} total refs)")

    fail = False

    if orphans:
        fail = True
        print(f"\nORPHAN refs (in body but not declared in sources:):", file=sys.stderr)
        for key in sorted(orphans):
            count = refs_in_body.count(key)
            print(f"  ✗ {{#{key}}}  ({count} mention(s))", file=sys.stderr)

    if unused:
        print(f"\nUnused sources (declared but not cited):")
        for key in sorted(unused):
            print(f"  · {key}")
        if args.strict:
            fail = True
            print(f"\n--strict: failing on unused sources.", file=sys.stderr)

    if not fail:
        print(f"\nall sources resolved.")
        return 0

    print(f"\nsources linter FAILED — fix before publish.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
