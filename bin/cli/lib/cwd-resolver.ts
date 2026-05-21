/**
 * cwd-resolver — given a working directory, find the profile cue should use.
 *
 * Resolution precedence (stop at first hit):
 *   1. `opts.override` (matches the --cue-profile CLI flag)
 *   2. `.cue-profile` file walking up from cwd; stops at git repo root or homeDir
 *   3. `<configDir>/repo-defaults.json` keyed by git repo root absolute path
 *   4. `<configDir>/default-profile` (single-line file)
 *   5. none — caller should open the picker
 *
 * Pure: only reads files under cwd and configDir. Never writes.
 */

import { readFile, stat } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";

export type ResolveResult =
  | { source: "flag"; profile: string }
  | { source: "pin-file"; profile: string; pinPath: string }
  | { source: "repo-default"; profile: string }
  | { source: "global-default"; profile: string }
  | { source: "none" };

export interface ResolveOptions {
  cwd: string;
  homeDir: string;
  configDir: string;
  override?: string | null;
}

async function exists(path: string): Promise<boolean> {
  try { await stat(path); return true; } catch { return false; }
}

async function findUpward(startDir: string, fileName: string, stopAt: string): Promise<string | null> {
  let dir = resolve(startDir);
  const stop = resolve(stopAt);
  while (true) {
    const candidate = join(dir, fileName);
    if (await exists(candidate)) return candidate;
    if (dir === stop) return null;
    const parent = dirname(dir);
    if (parent === dir) return null;
    dir = parent;
  }
}

async function findGitRoot(startDir: string, stopAt: string): Promise<string | null> {
  let dir = resolve(startDir);
  const stop = resolve(stopAt);
  while (true) {
    if (await exists(join(dir, ".git"))) return dir;
    if (dir === stop) return null;
    const parent = dirname(dir);
    if (parent === dir) return null;
    dir = parent;
  }
}

export async function resolveProfileForCwd(opts: ResolveOptions): Promise<ResolveResult> {
  if (opts.override) return { source: "flag", profile: opts.override };

  const pinPath = await findUpward(opts.cwd, ".cue-profile", opts.homeDir);
  if (pinPath) {
    const profile = (await readFile(pinPath, "utf8")).trim();
    if (profile) return { source: "pin-file", profile, pinPath };
  }

  const repoRoot = await findGitRoot(opts.cwd, opts.homeDir);
  if (repoRoot) {
    const repoDefaultsPath = join(opts.configDir, "repo-defaults.json");
    if (await exists(repoDefaultsPath)) {
      const map = JSON.parse(await readFile(repoDefaultsPath, "utf8")) as Record<string, string>;
      const profile = map[repoRoot];
      if (profile) return { source: "repo-default", profile };
    }
  }

  const defaultPath = join(opts.configDir, "default-profile");
  if (await exists(defaultPath)) {
    const profile = (await readFile(defaultPath, "utf8")).trim();
    if (profile) return { source: "global-default", profile };
  }

  return { source: "none" };
}
