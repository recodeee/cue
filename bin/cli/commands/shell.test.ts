import { describe, expect, test, beforeEach, afterEach } from "bun:test";
import { mkdtemp, readFile, rm, mkdir, stat } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";

import { runInstall, runUninstall } from "./shell";

let fakeHome: string;
beforeEach(async () => {
  fakeHome = await mkdtemp(join(tmpdir(), "cue-shell-"));
  await mkdir(join(fakeHome, ".local", "bin"), { recursive: true });
});
afterEach(async () => { await rm(fakeHome, { recursive: true, force: true }); });

describe("shell install", () => {
  test("writes claude and codex shims with correct content", async () => {
    const rc = await runInstall({
      homeDir: fakeHome,
      pathDirs: [join(fakeHome, ".local", "bin"), "/usr/bin"],
      realClaude: "/usr/bin/claude",
      realCodex: "/usr/bin/codex",
    });
    expect(rc).toBe(0);

    const claudeShim = await readFile(join(fakeHome, ".local", "bin", "claude"), "utf8");
    expect(claudeShim).toContain("exec cue launch claude");
    const codexShim = await readFile(join(fakeHome, ".local", "bin", "codex"), "utf8");
    expect(codexShim).toContain("exec cue launch codex");

    const st = await stat(join(fakeHome, ".local", "bin", "claude"));
    expect((st.mode & 0o111) !== 0).toBe(true); // executable
  });

  test("refuses to install when ~/.local/bin is not before real binary on PATH", async () => {
    const rc = await runInstall({
      homeDir: fakeHome,
      pathDirs: ["/usr/bin", join(fakeHome, ".local", "bin")], // wrong order
      realClaude: "/usr/bin/claude",
      realCodex: "/usr/bin/codex",
    });
    expect(rc).toBe(1);
  });

  test("uninstall removes shims, leaves bin dir", async () => {
    await runInstall({
      homeDir: fakeHome,
      pathDirs: [join(fakeHome, ".local", "bin"), "/usr/bin"],
      realClaude: "/usr/bin/claude",
      realCodex: "/usr/bin/codex",
    });
    const rc = await runUninstall({ homeDir: fakeHome });
    expect(rc).toBe(0);
    await expect(stat(join(fakeHome, ".local", "bin", "claude"))).rejects.toThrow();
  });
});
