/**
 * `soul migrate-symlinks` — rewrite external symlinks from soul/ to cue/.
 *
 * Walks the directories named in --roots (default: ~/.codex/skills,
 * ~/.claude-accounts/{any}/skills), inspects each symlink, and if the link's
 * target starts with --from, replaces the link with one whose target starts
 * with --to. Idempotent; dry-run by default.
 */

import { readdir, readlink, lstat, unlink, symlink } from "node:fs/promises";
import { join } from "node:path";
import { homedir } from "node:os";

export interface MigrateOptions {
  from: string;
  to: string;
  roots: string[];
  dryRun: boolean;
}

export interface MigrateSummary {
  scanned: number;
  updated: number;
  wouldUpdate: number;
  skipped: number;
  errors: { path: string; reason: string }[];
}

export async function migrateSymlinks(opts: MigrateOptions): Promise<MigrateSummary> {
  const summary: MigrateSummary = { scanned: 0, updated: 0, wouldUpdate: 0, skipped: 0, errors: [] };
  for (const root of opts.roots) await walk(root, opts, summary);
  return summary;
}

async function walk(dir: string, opts: MigrateOptions, s: MigrateSummary): Promise<void> {
  let entries: string[];
  try { entries = await readdir(dir); } catch { return; }
  for (const name of entries) {
    const path = join(dir, name);
    let st;
    try { st = await lstat(path); } catch (e) { s.errors.push({ path, reason: (e as Error).message }); continue; }
    if (st.isSymbolicLink()) {
      s.scanned++;
      const target = await readlink(path);
      if (target.startsWith(opts.from)) {
        const newTarget = opts.to + target.slice(opts.from.length);
        if (opts.dryRun) {
          s.wouldUpdate++;
          process.stdout.write(`would update: ${path} -> ${newTarget}\n`);
        } else {
          await unlink(path);
          await symlink(newTarget, path);
          s.updated++;
          process.stdout.write(`updated: ${path} -> ${newTarget}\n`);
        }
      } else {
        s.skipped++;
      }
    } else if (st.isDirectory()) {
      await walk(path, opts, s);
    }
  }
}

export async function run(args: string[]): Promise<number> {
  let from = "";
  let to = "";
  let dryRun = true;
  const roots: string[] = [];
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === "--from") from = args[++i] ?? "";
    else if (a === "--to") to = args[++i] ?? "";
    else if (a === "--apply") dryRun = false;
    else if (a === "--root") roots.push(args[++i] ?? "");
  }
  if (!from || !to) {
    process.stderr.write("usage: soul migrate-symlinks --from <path> --to <path> [--apply] [--root <dir>]+\n");
    return 1;
  }
  const defaultRoots = roots.length > 0 ? roots : [
    join(homedir(), ".codex", "skills"),
    join(homedir(), ".claude-accounts"),
  ];
  const summary = await migrateSymlinks({ from, to, roots: defaultRoots, dryRun });
  process.stdout.write(JSON.stringify(summary, null, 2) + "\n");
  return summary.errors.length > 0 ? 2 : 0;
}
