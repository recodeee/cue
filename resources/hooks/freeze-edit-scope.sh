#!/usr/bin/env bash
# PreToolUse:Write|Edit|MultiEdit — restrict edits to a directory (opt-in).
#
# Reads ~/.config/cue/freeze-dir. If present and non-empty, any Edit/Write
# targeting a file outside that path is blocked. Activated by /freeze.
#
# Exit 0 = allow, exit 2 = block.
set -euo pipefail

state_file="${HOME}/.config/cue/freeze-dir"
[[ -f "$state_file" ]] || exit 0
freeze_dir="$(tr -d '[:space:]' < "$state_file")"
[[ -z "$freeze_dir" ]] && exit 0

# Resolve freeze_dir to a real absolute path.
if [[ -d "$freeze_dir" ]]; then
  freeze_dir="$(cd "$freeze_dir" && pwd -P)"
fi

payload="$(cat -)"
target="$(printf '%s' "$payload" | python3 -c 'import sys,json
try: d=json.load(sys.stdin); print(d.get("tool_input",{}).get("file_path",""))
except Exception: pass' 2>/dev/null)"
[[ -z "$target" ]] && exit 0

# Resolve target to absolute (without requiring it to exist).
if [[ "$target" != /* ]]; then
  target="$(pwd)/$target"
fi
target_dir="$(dirname "$target")"
target_base="$(basename "$target")"
if [[ -d "$target_dir" ]]; then
  target="$(cd "$target_dir" && pwd -P)/$target_base"
fi
target="$(printf '%s' "$target" | sed 's|/\+|/|g;s|/$||')"

case "$target/" in
  "$freeze_dir/"*) exit 0 ;;
esac

>&2 echo "cue:freeze blocked: edits are locked to '$freeze_dir'."
>&2 echo "Target was: $target"
>&2 echo "To unlock: rm $state_file  (or run /unfreeze)"
exit 2
