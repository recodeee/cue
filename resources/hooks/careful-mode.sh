#!/usr/bin/env bash
# PreToolUse:Bash — stricter destructive-command guard (opt-in via /careful).
#
# bash-quality-preflight.sh already blocks the unconditionally-bad commands
# (rm -rf /, fork bombs, dd to /dev/sd, force-push to main). This hook adds
# the broader "ask twice" set — only active when the user has opted in via
# the /careful slash command (touches ~/.config/cue/careful-mode).
#
# Exit 0 = allow, exit 2 = block with stderr message.
set -euo pipefail

state_file="${HOME}/.config/cue/careful-mode"
[[ -f "$state_file" ]] || exit 0

payload="$(cat -)"
cmd="$(printf '%s' "$payload" | python3 -c 'import sys,json
try: d=json.load(sys.stdin); print(d.get("tool_input",{}).get("command",""))
except Exception: pass' 2>/dev/null)"
[[ -z "$cmd" ]] && exit 0

lower="$(printf '%s' "$cmd" | tr "[:upper:]" "[:lower:]")"

# rm -r / -rf / --recursive — allow only well-known safe targets.
if printf '%s' "$cmd" | grep -qE 'rm[[:space:]]+(-[a-zA-Z]*r[a-zA-Z]*|--recursive)'; then
  args="$(printf '%s' "$cmd" | sed -E 's/.*rm[[:space:]]+(-[a-zA-Z]+[[:space:]]+)*//;s/--recursive[[:space:]]*//')"
  safe=true
  for target in $args; do
    case "$target" in
      */node_modules|node_modules|*/.next|.next|*/dist|dist|*/__pycache__|__pycache__|*/.cache|.cache|*/build|build|*/.turbo|.turbo|*/coverage|coverage|*/target|target) ;;
      -*) ;;
      *) safe=false; break ;;
    esac
  done
  if [[ "$safe" != true ]]; then
    >&2 echo "cue:careful blocked: recursive delete of a non-build path."
    >&2 echo "Ask the user first or run a non-recursive rm. To disable: rm $state_file"
    exit 2
  fi
fi

# SQL data-loss patterns.
if printf '%s' "$lower" | grep -qE 'drop[[:space:]]+(table|database)'; then
  >&2 echo "cue:careful blocked: SQL DROP TABLE/DATABASE. Confirm with the user first."
  exit 2
fi
if printf '%s' "$lower" | grep -qE '\btruncate[[:space:]]+(table[[:space:]]+)?[a-z_]'; then
  >&2 echo "cue:careful blocked: SQL TRUNCATE deletes all rows. Confirm with the user first."
  exit 2
fi

# git push --force (any branch — bash-quality-preflight only covers main/master).
if printf '%s' "$cmd" | grep -qE 'git[[:space:]]+push[[:space:]]+.*(-f\b|--force\b|--force-with-lease\b)'; then
  >&2 echo "cue:careful blocked: git force-push. Other contributors may lose work."
  exit 2
fi

# git reset --hard (any ref).
if printf '%s' "$cmd" | grep -qE 'git[[:space:]]+reset[[:space:]]+--hard'; then
  >&2 echo "cue:careful blocked: git reset --hard discards uncommitted changes."
  exit 2
fi

# git checkout . / git restore .
if printf '%s' "$cmd" | grep -qE 'git[[:space:]]+(checkout|restore)[[:space:]]+\.'; then
  >&2 echo "cue:careful blocked: git checkout/restore '.' discards uncommitted changes."
  exit 2
fi

# kubectl delete (production blast radius).
if printf '%s' "$cmd" | grep -qE 'kubectl[[:space:]]+delete\b'; then
  >&2 echo "cue:careful blocked: kubectl delete removes cluster resources. Confirm with the user."
  exit 2
fi

# docker prune / docker rm -f
if printf '%s' "$cmd" | grep -qE 'docker[[:space:]]+(rm[[:space:]]+-f|system[[:space:]]+prune)'; then
  >&2 echo "cue:careful blocked: docker force-remove/prune deletes containers/images."
  exit 2
fi

exit 0
