#!/usr/bin/env bash
# SessionStart hook — warns if Codex-CLI or plugin cache is stale/missing.
# Rationale: Hydra 2.0 depends on Codex for Cross-Provider-Review (Mies+, Stranger, Sentinel).
# Silent degradation to Claude-only kills the core value prop.
set -euo pipefail

if ! command -v codex >/dev/null 2>&1; then
  echo "⚠  Codex-CLI not installed. Hydra 2.0 Cross-Provider-Review will fall back to Claude-only." >&2
  echo "   Install via: npm install -g @openai/codex-cli   (or platform equivalent)" >&2
  exit 0
fi

PLUGIN_CACHE="${HOME}/.claude/plugins/cache/openai-codex/codex"
if [[ ! -d "$PLUGIN_CACHE" ]]; then
  echo "⚠  Codex Claude Code plugin cache missing at $PLUGIN_CACHE" >&2
  echo "   Run: claude plugins install openai-codex" >&2
  exit 0
fi

LATEST="$(find "$PLUGIN_CACHE" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | sort -Vr | head -n 1)"
if [[ -z "$LATEST" ]]; then
  echo "⚠  Codex plugin cache at $PLUGIN_CACHE is empty." >&2
  exit 0
fi

# macOS: stat -f %m ; Linux: stat -c %Y — support both
if mtime="$(stat -f %m "$LATEST" 2>/dev/null)"; then :
elif mtime="$(stat -c %Y "$LATEST" 2>/dev/null)"; then :
else
  exit 0  # can't determine mtime — silent rather than noisy false positive
fi

AGE_DAYS=$(( ($(date +%s) - mtime) / 86400 ))
if (( AGE_DAYS > 30 )); then
  echo "⚠  Codex plugin cache is ${AGE_DAYS}d old (>30d). Consider refreshing." >&2
fi
