---
description: Lock Edit/Write to a specific directory for the rest of the session. Prevents accidental edits outside the chosen scope.
---

# /freeze — restrict edits to one directory

Activates the `freeze-edit-scope` hook. Any `Edit` / `Write` / `MultiEdit`
tool call targeting a file outside the chosen directory is blocked.

## Usage

`/freeze <absolute-or-relative-path>`

If the user didn't pass a path, ask them via `AskUserQuestion` ("Which directory
should I restrict edits to?") and have them type the path.

## Activate

```bash
# Replace $DIR with the directory to lock to. Resolve to absolute.
DIR="$(cd "$DIR" && pwd -P)"
mkdir -p ~/.config/cue
printf '%s' "$DIR" > ~/.config/cue/freeze-dir
echo "cue: edits frozen to $DIR. To unlock: /unfreeze"
```

## Behavior

- `Edit`/`Write`/`MultiEdit` outside the directory → hard-blocked with stderr message.
- `Read`, `Bash`, `Grep`, `Glob` are unaffected.
- `Edit` of a file inside the directory → allowed.

## Deactivate

`/unfreeze` — or `rm ~/.config/cue/freeze-dir`.

## When to use

- Debugging one module — stop the agent "fixing" unrelated code.
- Doing a focused refactor that should be self-contained.
- Reviewing/cleaning a vendor directory without touching anything else.

Pair with `/careful` to also block destructive bash commands (`/guard` does both).
