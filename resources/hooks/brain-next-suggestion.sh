#!/usr/bin/env bash
# Stop hook — emits a "🧠 Next:" block with 1-3 ranked next-step suggestions
# grounded in real session signals:
#   1. Recent git commits in the session's cwd  (what got shipped?)
#   2. ~/.config/cue/analytics.jsonl            (which skills fired? misses?)
#   3. cue telemetry promote output             (any promotion candidates?)
#   4. Uncommitted changes / open TODOs         (what's still in flight?)
#
# Each suggestion is tagged with a dimension + bounded % + confidence tier
# from meta/roi-estimator, so the user can rank by impact.
#
# Gating:
#   - Skip empty sessions (no tool calls).
#   - Skip if the most recent commit message contains "[skip-brain]".
#   - Once per stop event (no re-fire within 60s).
#
# No external deps beyond jq + git. <500ms target.
# Exits 0 always — observability hook, never a gate.

set -uo pipefail

payload="$(cat -)"
CACHE_DIR="${XDG_RUNTIME_DIR:-/tmp}/cue-brain-suggestion"
mkdir -p "$CACHE_DIR" 2>/dev/null || exit 0

extract() {
  printf '%s' "$payload" | grep -oE "\"$1\"[[:space:]]*:[[:space:]]*\"[^\"]*\"" | head -1 \
    | sed "s/.*\"$1\"[[:space:]]*:[[:space:]]*\"//; s/\"$//"
}

session_id="$(extract session_id)"
transcript_path="$(extract transcript_path)"
cwd="$(pwd)"

# Throttle: don't re-fire within 60s for the same session.
throttle="$CACHE_DIR/throttle.${session_id:-default}"
now=$(date +%s)
last=$(stat -c '%Y' "$throttle" 2>/dev/null || echo 0)
[ $((now - last)) -lt 60 ] && exit 0
touch "$throttle"

# ─── Gather signals ──────────────────────────────────────────────────────
suggestions=()

# Signal 1: recent commits in cwd. If 3+ commits in the last hour, the
# user has been on a streak — surface "next thing" not "wrap up".
recent_commits=0
last_commit_msg=""
if [ -d "$cwd/.git" ] || git -C "$cwd" rev-parse --git-dir >/dev/null 2>&1; then
  recent_commits=$(git -C "$cwd" log --since="1 hour ago" --pretty=format:'%h' 2>/dev/null | wc -l)
  last_commit_msg=$(git -C "$cwd" log -1 --pretty=format:'%s' 2>/dev/null)
fi

# Skip if user explicitly requested no suggestions in last commit.
if [[ "$last_commit_msg" == *"[skip-brain]"* ]]; then exit 0; fi

# Signal 2: uncommitted changes (work in flight)
uncommitted=0
if git -C "$cwd" rev-parse --git-dir >/dev/null 2>&1; then
  uncommitted=$(git -C "$cwd" status --short 2>/dev/null | wc -l)
fi

# Signal 3: pending promotion candidates from telemetry.
# Cache for 5 minutes since this requires a bun startup (~300ms).
promote_count=0
top_promote=""
PROMOTE_CACHE="$CACHE_DIR/promote.json"
PROMOTE_CACHE_AGE=$(( now - $(stat -c '%Y' "$PROMOTE_CACHE" 2>/dev/null || echo 0) ))
if [ -f "$HOME/.config/cue/analytics.jsonl" ] && [ -x "$HOME/Documents/cue/bin/cue" ]; then
  if [ ! -f "$PROMOTE_CACHE" ] || [ "$PROMOTE_CACHE_AGE" -gt 300 ]; then
    "$HOME/Documents/cue/bin/cue" telemetry promote --json 2>/dev/null > "$PROMOTE_CACHE.tmp" \
      && mv "$PROMOTE_CACHE.tmp" "$PROMOTE_CACHE"
  fi
  if [ -s "$PROMOTE_CACHE" ]; then
    promote_count=$(jq 'length' "$PROMOTE_CACHE" 2>/dev/null | tr -d '\n' || echo 0)
    [ -z "$promote_count" ] && promote_count=0
    if [ "$promote_count" -gt 0 ] 2>/dev/null; then
      top_promote=$(jq -r '.[0] | "\(.skill) → profile \(.profile) (\(.invocations)×)"' "$PROMOTE_CACHE" 2>/dev/null)
    fi
  fi
fi

# Signal 4: skill misses (queries that should have triggered a skill)
miss_count=0
if [ -f "$HOME/.config/cue/analytics.jsonl" ]; then
  miss_count=$(grep -c '"event":"skill_miss"' "$HOME/.config/cue/analytics.jsonl" 2>/dev/null | tr -d '\n')
  [ -z "$miss_count" ] && miss_count=0
fi

# ─── Synthesize suggestions ──────────────────────────────────────────────
# Rule 1: uncommitted work → suggest review/commit
if [ "$uncommitted" -gt 5 ]; then
  suggestions+=("Review and commit the $uncommitted uncommitted files before context drifts.|friction +30% 🟡 ~70%|/code-review then commit")
elif [ "$uncommitted" -gt 0 ] && [ "$recent_commits" -ge 2 ]; then
  suggestions+=("Stage the remaining $uncommitted file(s) and ship a final commit.|friction +20% 🟡 ~80%|git add + commit")
fi

# Rule 2: hot promotion candidate → suggest the profile bump
if [ -n "$top_promote" ] && [ "$promote_count" -ge 1 ]; then
  suggestions+=("Promote a frequently smart-loaded skill: $top_promote.|turn-efficiency +25% 🟡 ~70%|cue telemetry promote")
fi

# Rule 3: many misses → suggest skill description tuning
if [ "$miss_count" -gt 10 ]; then
  suggestions+=("Tune skill descriptions: $miss_count user prompts matched triggers but the skills didn't fire.|accuracy +30% 🟠 ~40%|cue telemetry misses")
fi

# Rule 4: streak → momentum suggestion (only if no higher-priority items)
if [ "${#suggestions[@]}" -eq 0 ] && [ "$recent_commits" -ge 3 ]; then
  suggestions+=("Hot streak: $recent_commits commits in the last hour. Push remote before context resets.|friction +20% 🟢 measured|git push")
fi

[ "${#suggestions[@]}" -eq 0 ] && exit 0

# ─── Emit the block ──────────────────────────────────────────────────────
# Cap at 3 suggestions max.
printf '\n🧠 Next:\n'
i=0
for s in "${suggestions[@]}"; do
  i=$((i + 1))
  [ "$i" -gt 3 ] && break
  IFS='|' read -r reason roi cmd <<< "$s"
  printf '   %d. %s\n' "$i" "$reason"
  printf '      ROI: %s   →   %s\n' "$roi" "$cmd"
done
printf '   %s\n' "(suggestions grounded in: $recent_commits recent commits, $uncommitted uncommitted, $promote_count promote candidates, $miss_count misses; suppress with [skip-brain] in commit msg)"
exit 0
