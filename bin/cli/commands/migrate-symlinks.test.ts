import { describe, expect, test, beforeEach, afterEach } from "bun:test";
import { mkdtemp, mkdir, symlink, readlink, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";

import { migrateSymlinks } from "./migrate-symlinks";

let root: string;
beforeEach(async () => { root = await mkdtemp(join(tmpdir(), "cue-mig-")); });
afterEach(async () => { await rm(root, { recursive: true, force: true }); });

describe("migrateSymlinks", () => {
  test("rewrites symlinks whose target starts with --from", async () => {
    const skills = join(root, ".codex", "skills");
    await mkdir(skills, { recursive: true });
    await symlink("/home/user/Documents/soul/skills/skills/x/y", join(skills, "y"));
    const summary = await migrateSymlinks({
      from: "/home/user/Documents/soul",
      to:   "/home/user/Documents/cue",
      roots: [skills],
      dryRun: false,
    });
    expect(summary.updated).toBe(1);
    const after = await readlink(join(skills, "y"));
    expect(after).toBe("/home/user/Documents/cue/skills/skills/x/y");
  });

  test("dryRun does not modify links", async () => {
    const skills = join(root, ".codex", "skills");
    await mkdir(skills, { recursive: true });
    const original = "/home/user/Documents/soul/skills/skills/x/y";
    await symlink(original, join(skills, "y"));
    const summary = await migrateSymlinks({
      from: "/home/user/Documents/soul",
      to:   "/home/user/Documents/cue",
      roots: [skills],
      dryRun: true,
    });
    expect(summary.wouldUpdate).toBe(1);
    expect(summary.updated).toBe(0);
    expect(await readlink(join(skills, "y"))).toBe(original);
  });

  test("ignores symlinks whose target does not match --from", async () => {
    const skills = join(root, ".codex", "skills");
    await mkdir(skills, { recursive: true });
    await symlink("/somewhere/else/x", join(skills, "y"));
    const summary = await migrateSymlinks({
      from: "/home/user/Documents/soul",
      to:   "/home/user/Documents/cue",
      roots: [skills],
      dryRun: false,
    });
    expect(summary.updated).toBe(0);
    expect(summary.skipped).toBe(1);
  });
});
