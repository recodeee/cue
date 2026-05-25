---
description: Maximum safety — activates /careful + /freeze in one command. Use for prod work or when debugging live systems.
---

# /guard — full safety mode

Runs `/careful` and `/freeze` together. The agent gets both:

- **Bash guard**: stricter destructive-command block (see `/careful`).
- **Edit guard**: locks Edit/Write to the chosen directory (see `/freeze`).

## Usage

`/guard <directory-to-lock-to>`

If no path was passed, ask the user via `AskUserQuestion`.

## Activate

```bash
# Resolve to absolute path.
DIR="$(cd "$DIR" && pwd -P)"
mkdir -p ~/.config/cue
touch ~/.config/cue/careful-mode
printf '%s' "$DIR" > ~/.config/cue/freeze-dir
echo "cue: guard active. Bash strict mode + edits locked to $DIR."
echo "To release: /unfreeze && rm ~/.config/cue/careful-mode"
```

## Deactivate

```bash
rm -f ~/.config/cue/careful-mode ~/.config/cue/freeze-dir
echo "cue: guard released."
```

## When to use

Touching production. Editing infra. Debugging on main. Pair-programming with the
agent on a stack you can't afford to break.
