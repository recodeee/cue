import { describe, expect, test, beforeEach, afterEach } from "bun:test";
import { mkdtempSync, rmSync, writeFileSync, mkdirSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

import { computeSkillHash, loadManifest, saveManifest, findChangedSkills } from "./incremental-materialize";

let tmp: string;

beforeEach(() => {
  tmp = mkdtempSync(join(tmpdir(), "cue-incr-"));
});
afterEach(() => {
  try { rmSync(tmp, { recursive: true, force: true }); } catch {}
});

describe("computeSkillHash", () => {
  test("returns consistent hash for same content", () => {
    const dir = join(tmp, "skill-a");
    mkdirSync(dir);
    writeFileSync(join(dir, "SKILL.md"), "# Test skill");
    const h1 = computeSkillHash(dir);
    const h2 = computeSkillHash(dir);
    expect(h1).toBe(h2);
    expect(h1).toHaveLength(64); // sha256 hex
  });

  test("different content produces different hash", () => {
    const dir1 = join(tmp, "skill-1");
    const dir2 = join(tmp, "skill-2");
    mkdirSync(dir1);
    mkdirSync(dir2);
    writeFileSync(join(dir1, "SKILL.md"), "# Skill A");
    writeFileSync(join(dir2, "SKILL.md"), "# Skill B");
    expect(computeSkillHash(dir1)).not.toBe(computeSkillHash(dir2));
  });

  test("includes nested files in hash", () => {
    const dir = join(tmp, "skill-nested");
    mkdirSync(dir);
    mkdirSync(join(dir, "sub"));
    writeFileSync(join(dir, "SKILL.md"), "# Main");
    const h1 = computeSkillHash(dir);
    writeFileSync(join(dir, "sub/extra.md"), "extra");
    const h2 = computeSkillHash(dir);
    expect(h1).not.toBe(h2);
  });

  test("empty dir returns a hash", () => {
    const dir = join(tmp, "empty");
    mkdirSync(dir);
    const h = computeSkillHash(dir);
    expect(h).toHaveLength(64);
  });
});

describe("loadManifest / saveManifest", () => {
  test("missing manifest returns empty object", () => {
    expect(loadManifest(tmp)).toEqual({});
  });

  test("round-trips correctly", () => {
    const manifest = { "review/code-review": "abc123", "meta/doctor": "def456" };
    saveManifest(tmp, manifest);
    expect(loadManifest(tmp)).toEqual(manifest);
  });
});

describe("findChangedSkills", () => {
  test("detects added skills", () => {
    const result = findChangedSkills(
      { "a": "h1", "b": "h2" },
      { "a": "h1" },
    );
    expect(result.added).toEqual(["b"]);
    expect(result.removed).toEqual([]);
    expect(result.changed).toEqual([]);
  });

  test("detects removed skills", () => {
    const result = findChangedSkills(
      { "a": "h1" },
      { "a": "h1", "b": "h2" },
    );
    expect(result.removed).toEqual(["b"]);
    expect(result.added).toEqual([]);
  });

  test("detects changed skills", () => {
    const result = findChangedSkills(
      { "a": "h1-new" },
      { "a": "h1-old" },
    );
    expect(result.changed).toEqual(["a"]);
    expect(result.added).toEqual([]);
    expect(result.removed).toEqual([]);
  });

  test("handles empty manifests", () => {
    expect(findChangedSkills({}, {})).toEqual({ added: [], removed: [], changed: [] });
  });

  test("complex diff", () => {
    const result = findChangedSkills(
      { "a": "1", "b": "2-new", "c": "3" },
      { "a": "1", "b": "2-old", "d": "4" },
    );
    expect(result.added).toEqual(["c"]);
    expect(result.removed).toEqual(["d"]);
    expect(result.changed).toEqual(["b"]);
  });
});
