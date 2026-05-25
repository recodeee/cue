/**
 * Incremental materialization — hash-based skill change detection.
 */

import { createHash } from "node:crypto";
import { readFileSync, readdirSync, statSync, existsSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const MANIFEST_FILE = ".cue-manifest.json";

/**
 * Compute a sha256 hash of all files in a skill directory.
 */
export function computeSkillHash(skillDir: string): string {
  const hash = createHash("sha256");
  const files = collectFiles(skillDir).sort();
  for (const file of files) {
    hash.update(file); // include relative path in hash
    hash.update(readFileSync(join(skillDir, file)));
  }
  return hash.digest("hex");
}

/** Recursively collect relative file paths. */
function collectFiles(dir: string, prefix = ""): string[] {
  const out: string[] = [];
  let entries: string[];
  try { entries = readdirSync(dir); } catch { return out; }
  for (const entry of entries) {
    const full = join(dir, entry);
    const rel = prefix ? `${prefix}/${entry}` : entry;
    try {
      if (statSync(full).isDirectory()) {
        out.push(...collectFiles(full, rel));
      } else {
        out.push(rel);
      }
    } catch { /* skip unreadable */ }
  }
  return out;
}

/**
 * Load the manifest from a runtime directory.
 */
export function loadManifest(runtimeDir: string): Record<string, string> {
  const path = join(runtimeDir, MANIFEST_FILE);
  if (!existsSync(path)) return {};
  try {
    return JSON.parse(readFileSync(path, "utf8"));
  } catch { return {}; }
}

/**
 * Save the manifest to a runtime directory.
 */
export function saveManifest(runtimeDir: string, manifest: Record<string, string>): void {
  writeFileSync(join(runtimeDir, MANIFEST_FILE), JSON.stringify(manifest, null, 2));
}

/**
 * Find which skills changed between two manifests.
 */
export function findChangedSkills(
  current: Record<string, string>,
  previous: Record<string, string>,
): { added: string[]; removed: string[]; changed: string[] } {
  const added: string[] = [];
  const removed: string[] = [];
  const changed: string[] = [];

  for (const id of Object.keys(current)) {
    if (!(id in previous)) added.push(id);
    else if (current[id] !== previous[id]) changed.push(id);
  }
  for (const id of Object.keys(previous)) {
    if (!(id in current)) removed.push(id);
  }

  return { added, removed, changed };
}
