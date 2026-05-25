import { describe, expect, test } from "bun:test";
import { generateSkillStub, generateLazyManifest, isLazyEnabled } from "./lazy-skills";

describe("generateSkillStub", () => {
  test("generates stub with name and description", () => {
    const stub = generateSkillStub("review/code-review", "Thorough PR review");
    expect(stub).toContain("name: code-review");
    expect(stub).toContain("Thorough PR review");
    expect(stub).toContain("Full skill body available on demand");
  });

  test("handles simple id without slash", () => {
    const stub = generateSkillStub("linter", "Lint code");
    expect(stub).toContain("name: linter");
    expect(stub).toContain("# linter");
  });

  test("includes frontmatter description", () => {
    const stub = generateSkillStub("meta/doctor", "Diagnose issues");
    expect(stub).toContain('description: "Diagnose issues"');
  });
});

describe("generateLazyManifest", () => {
  test("generates manifest with skill list", () => {
    const manifest = generateLazyManifest([
      { id: "review/code-review", description: "PR review" },
      { id: "meta/doctor", description: "Diagnose" },
    ]);
    expect(manifest).toContain("## Available Skills (lazy-loaded)");
    expect(manifest).toContain("**code-review**");
    expect(manifest).toContain("`review/code-review`");
    expect(manifest).toContain("PR review");
    expect(manifest).toContain("**doctor**");
  });

  test("empty skills returns empty string", () => {
    expect(generateLazyManifest([])).toBe("");
  });

  test("includes on-demand instruction", () => {
    const manifest = generateLazyManifest([{ id: "x/y", description: "test" }]);
    expect(manifest).toContain("reference it by name");
  });
});

describe("isLazyEnabled", () => {
  test("returns false for normal profile", () => {
    const profile = { name: "test", lazy: undefined } as any;
    expect(isLazyEnabled(profile)).toBe(false);
  });

  test("returns true when lazy: true", () => {
    const profile = { name: "test", lazy: true } as any;
    expect(isLazyEnabled(profile)).toBe(true);
  });
});
