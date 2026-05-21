import { describe, expect, test, beforeEach, afterEach } from "bun:test";
import { mkdtemp, mkdir, writeFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";

import { resolveProfileForCwd } from "./cwd-resolver";

let root: string;
beforeEach(async () => {
  root = await mkdtemp(join(tmpdir(), "cue-resolver-"));
});
afterEach(async () => {
  await rm(root, { recursive: true, force: true });
});

describe("resolveProfileForCwd", () => {
  test("returns null when nothing pinned and no defaults set", async () => {
    const out = await resolveProfileForCwd({
      cwd: root,
      homeDir: root,
      configDir: join(root, ".config", "cue"),
    });
    expect(out).toEqual({ source: "none" });
  });

  test("reads .cue-profile in cwd", async () => {
    await writeFile(join(root, ".cue-profile"), "frontend\n");
    const out = await resolveProfileForCwd({
      cwd: root,
      homeDir: root,
      configDir: join(root, ".config", "cue"),
    });
    expect(out).toEqual({ source: "pin-file", profile: "frontend", pinPath: join(root, ".cue-profile") });
  });

  test("walks up to find .cue-profile", async () => {
    await writeFile(join(root, ".cue-profile"), "backend\n");
    const child = join(root, "a", "b", "c");
    await mkdir(child, { recursive: true });
    const out = await resolveProfileForCwd({
      cwd: child,
      homeDir: root,
      configDir: join(root, ".config", "cue"),
    });
    expect(out).toEqual({ source: "pin-file", profile: "backend", pinPath: join(root, ".cue-profile") });
  });

  test("stops walking at homeDir", async () => {
    await writeFile(join(root, ".cue-profile"), "should-not-find");
    const home = join(root, "home");
    const child = join(home, "user");
    await mkdir(child, { recursive: true });
    const out = await resolveProfileForCwd({
      cwd: child,
      homeDir: home,
      configDir: join(home, ".config", "cue"),
    });
    expect(out.source).toBe("none");
  });

  test("falls back to repo-defaults.json keyed by git repo root", async () => {
    const repo = join(root, "repo");
    await mkdir(join(repo, ".git"), { recursive: true });
    await mkdir(join(root, ".config", "cue"), { recursive: true });
    await writeFile(
      join(root, ".config", "cue", "repo-defaults.json"),
      JSON.stringify({ [repo]: "research" }),
    );
    const out = await resolveProfileForCwd({
      cwd: repo,
      homeDir: root,
      configDir: join(root, ".config", "cue"),
    });
    expect(out).toEqual({ source: "repo-default", profile: "research" });
  });

  test("falls back to default-profile file", async () => {
    await mkdir(join(root, ".config", "cue"), { recursive: true });
    await writeFile(join(root, ".config", "cue", "default-profile"), "core\n");
    const out = await resolveProfileForCwd({
      cwd: root,
      homeDir: root,
      configDir: join(root, ".config", "cue"),
    });
    expect(out).toEqual({ source: "global-default", profile: "core" });
  });

  test("--cue-profile flag (passed via override) wins over everything", async () => {
    await writeFile(join(root, ".cue-profile"), "frontend");
    const out = await resolveProfileForCwd({
      cwd: root,
      homeDir: root,
      configDir: join(root, ".config", "cue"),
      override: "backend",
    });
    expect(out).toEqual({ source: "flag", profile: "backend" });
  });
});
