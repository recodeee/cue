/**
 * Tests for multi-inherit profile support.
 */

import { afterEach, beforeEach, describe, expect, test } from "bun:test";
import { mkdir, mkdtemp, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";

import { loadProfile } from "./profile-loader";

let scratchRoot: string;
let priorEnv: string | undefined;

beforeEach(async () => {
  scratchRoot = await mkdtemp(join(tmpdir(), "cue-multi-inherit-"));
  priorEnv = process.env.CUE_PROFILES_DIR;
  process.env.CUE_PROFILES_DIR = scratchRoot;
});

afterEach(() => {
  if (priorEnv === undefined) delete process.env.CUE_PROFILES_DIR;
  else process.env.CUE_PROFILES_DIR = priorEnv;
});

async function writeProfile(name: string, body: string): Promise<void> {
  const dir = join(scratchRoot, name);
  await mkdir(dir, { recursive: true });
  await writeFile(join(dir, "profile.yaml"), body, "utf8");
}

describe("multi-inherit profiles", () => {
  test("array inherits merges skills from multiple parents", async () => {
    await writeProfile("base-a", `
name: base-a
description: "Base A"
skills:
  local: [skill-a]
rules: [rule-a]
persona: "I am A"
`);
    await writeProfile("base-b", `
name: base-b
description: "Base B"
skills:
  local: [skill-b]
rules: [rule-b]
persona: "I am B"
`);
    await writeProfile("child", `
name: child
description: "Child with multi-inherit"
inherits: [base-a, base-b]
skills:
  local: [skill-c]
`);

    const resolved = await loadProfile("child");
    const localIds = resolved.skills.local.map(s => s.id);
    expect(localIds).toContain("skill-a");
    expect(localIds).toContain("skill-b");
    expect(localIds).toContain("skill-c");
  });

  test("persona is last-wins from parents, child overrides all", async () => {
    await writeProfile("base-a", `
name: base-a
description: "Base A"
persona: "I am A"
`);
    await writeProfile("base-b", `
name: base-b
description: "Base B"
persona: "I am B"
`);
    await writeProfile("child", `
name: child
description: "Child"
inherits: [base-a, base-b]
persona: "I am Child"
`);

    const resolved = await loadProfile("child");
    expect(resolved.persona).toBe("I am Child");
  });

  test("persona last-wins from parents when child has none", async () => {
    await writeProfile("base-a", `
name: base-a
description: "Base A"
persona: "I am A"
`);
    await writeProfile("base-b", `
name: base-b
description: "Base B"
persona: "I am B"
`);
    await writeProfile("child", `
name: child
description: "Child"
inherits: [base-a, base-b]
`);

    const resolved = await loadProfile("child");
    // Last parent's persona wins (base-b is last in the chain before child)
    expect(resolved.persona).toBe("I am B");
  });

  test("rules/hooks/commands are unioned", async () => {
    await writeProfile("base-a", `
name: base-a
description: "Base A"
rules: [rule-a, shared-rule]
hooks: [hook-a]
`);
    await writeProfile("base-b", `
name: base-b
description: "Base B"
rules: [rule-b, shared-rule]
hooks: [hook-b]
`);
    await writeProfile("child", `
name: child
description: "Child"
inherits: [base-a, base-b]
commands: [cmd-c]
`);

    const resolved = await loadProfile("child");
    expect(resolved.rules).toContain("rule-a");
    expect(resolved.rules).toContain("rule-b");
    expect(resolved.rules).toContain("shared-rule");
    // Deduped
    expect(resolved.rules.filter(r => r === "shared-rule").length).toBe(1);
    expect(resolved.hooks).toContain("hook-a");
    expect(resolved.hooks).toContain("hook-b");
    expect(resolved.commands).toContain("cmd-c");
  });

  test("MCPs are deduped by id", async () => {
    await writeProfile("base-a", `
name: base-a
description: "Base A"
mcps: [gbrain, mcp-a]
`);
    await writeProfile("base-b", `
name: base-b
description: "Base B"
mcps: [gbrain, mcp-b]
`);
    await writeProfile("child", `
name: child
description: "Child"
inherits: [base-a, base-b]
`);

    const resolved = await loadProfile("child");
    const mcpIds = resolved.mcps.map(m => m.id);
    expect(mcpIds).toContain("gbrain");
    expect(mcpIds).toContain("mcp-a");
    expect(mcpIds).toContain("mcp-b");
    expect(mcpIds.filter(id => id === "gbrain").length).toBe(1);
  });

  test("single string inherits still works", async () => {
    await writeProfile("parent", `
name: parent
description: "Parent"
skills:
  local: [skill-p]
`);
    await writeProfile("child", `
name: child
description: "Child"
inherits: parent
skills:
  local: [skill-c]
`);

    const resolved = await loadProfile("child");
    const localIds = resolved.skills.local.map(s => s.id);
    expect(localIds).toContain("skill-p");
    expect(localIds).toContain("skill-c");
  });
});
