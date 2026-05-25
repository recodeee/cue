---
description: Enable cue's careful mode — stricter block on softly-destructive commands (rm -rf non-build, DROP/TRUNCATE, git force-push, kubectl/docker delete).
---

# /careful — destructive-command guard (opt-in)

cue's `bash-quality-preflight` hook always blocks the unconditionally-bad
commands (`rm -rf /`, fork bombs, `dd` to `/dev/sd*`, force-push to main).
`/careful` engages the **stricter** set covering the wider "ask twice" zone.

## Activate

```bash
mkdir -p ~/.config/cue
touch ~/.config/cue/careful-mode
echo "cue: careful mode active. To turn off: rm ~/.config/cue/careful-mode"
```

## What it now blocks (in addition to the always-on rules)

| Pattern | Example | Why |
|---|---|---|
| `rm -rf` of any non-build path | `rm -rf src/`, `rm -rf ~/Documents/...` | Recursive delete outside `node_modules\|dist\|.next\|.cache\|build\|target\|coverage` |
| `DROP TABLE` / `DROP DATABASE` | `DROP TABLE users` | Permanent schema/data loss |
| `TRUNCATE table_name` | `TRUNCATE orders` | Deletes all rows |
| `git push --force` / `-f` (any branch) | `git push -f origin feat/x` | Rewrites remote history |
| `git reset --hard` | `git reset --hard HEAD~3` | Discards uncommitted work |
| `git checkout .` / `git restore .` | `git checkout .` | Discards uncommitted work |
| `kubectl delete <anything>` | `kubectl delete pod app-7d9` | Cluster blast radius |
| `docker rm -f` / `docker system prune` | `docker system prune -a` | Container/image loss |

Block reason is printed to stderr; the model picks something else or asks the user.

## Deactivate

```bash
rm ~/.config/cue/careful-mode
```

## When to use

- Touching production / shared infra
- Working in a repo with uncommitted changes you care about
- Debugging — when you don't want the agent to "helpfully" reset the tree
- Pair it with `/freeze <dir>` to also lock edits to one folder (`/guard` does both)
