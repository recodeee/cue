/**
 * Locate the real `claude` binary on PATH, skipping cue's shim.
 *
 * cue installs ~/.local/bin/claude as a bash one-liner that calls `cue launch
 * claude`; shelling to that from within cue would recurse or trigger the picker.
 *
 * Lookup order:
 *   1. $CUE_REAL_CLAUDE (explicit override)
 *   2. $CLAUDE_CODE_EXECPATH (set by claude-code itself on subprocesses)
 *   3. Walk $PATH, skipping any small bash shim that contains `cue launch`.
 */

import { existsSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

export function findRealClaudeBin(): string | null {
  if (process.env.CUE_REAL_CLAUDE && existsSync(process.env.CUE_REAL_CLAUDE)) {
    return process.env.CUE_REAL_CLAUDE;
  }
  if (process.env.CLAUDE_CODE_EXECPATH && existsSync(process.env.CLAUDE_CODE_EXECPATH)) {
    return process.env.CLAUDE_CODE_EXECPATH;
  }
  const pathDirs = (process.env.PATH ?? "").split(":").filter(Boolean);
  for (const dir of pathDirs) {
    const candidate = join(dir, "claude");
    if (!existsSync(candidate)) continue;
    try {
      const stat = statSync(candidate);
      if (stat.size < 500) {
        const content = readFileSync(candidate, "utf8");
        if (/cue\s+launch/i.test(content)) continue;
      }
      return candidate;
    } catch {
      return candidate;
    }
  }
  return null;
}
