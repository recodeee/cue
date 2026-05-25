import { describe, it, expect, beforeEach, afterEach } from "bun:test";
import { mkdtempSync, mkdirSync, writeFileSync, existsSync, readFileSync, rmSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";

import {
  fetchCompanionFiles,
  parseCompanionsField,
  findIncompleteSkills,
  vendorSkill,
  readSourceFile,
  type Fetcher,
  type GitHubContentEntry,
} from "./companion-fetch";

// ---------------------------------------------------------------------------
// Mock fetcher
// ---------------------------------------------------------------------------

function createMockFetcher(tree: Record<string, GitHubContentEntry[]>): Fetcher & { downloads: string[] } {
  const downloads: string[] = [];
  return {
    downloads,
    listDir(_repo: string, path: string) {
      return tree[path] ?? null;
    },
    downloadFile(url: string, dest: string) {
      downloads.push(dest);
      writeFileSync(dest, `content-of-${url}`);
      return true;
    },
  };
}

function createFailingFetcher(): Fetcher {
  return {
    listDir() { return null; },
    downloadFile() { return false; },
  };
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

let tmpDir: string;

beforeEach(() => {
  tmpDir = mkdtempSync(join(tmpdir(), "cue-cf-test-"));
});

afterEach(() => {
  rmSync(tmpDir, { recursive: true, force: true });
});

// ---------------------------------------------------------------------------
// parseCompanionsField
// ---------------------------------------------------------------------------

describe("parseCompanionsField", () => {
  it("returns null when no frontmatter", () => {
    const p = join(tmpDir, "SKILL.md");
    writeFileSync(p, "# Hello\nNo frontmatter here.");
    expect(parseCompanionsField(p)).toBeNull();
  });

  it("returns null when no companions field", () => {
    const p = join(tmpDir, "SKILL.md");
    writeFileSync(p, "---\nname: test\ndescription: foo\n---\n# Test");
    expect(parseCompanionsField(p)).toBeNull();
  });

  it("parses inline array format", () => {
    const p = join(tmpDir, "SKILL.md");
    writeFileSync(p, "---\nname: pdf\ncompanions: [scripts/, forms.md, reference.md]\n---\n# PDF");
    expect(parseCompanionsField(p)).toEqual(["scripts/", "forms.md", "reference.md"]);
  });

  it("parses YAML list format", () => {
    const p = join(tmpDir, "SKILL.md");
    writeFileSync(p, "---\nname: pdf\ncompanions:\n  - scripts/\n  - forms.md\n---\n# PDF");
    expect(parseCompanionsField(p)).toEqual(["scripts/", "forms.md"]);
  });

  it("returns null for non-existent file", () => {
    expect(parseCompanionsField("/nonexistent/SKILL.md")).toBeNull();
  });
});

// ---------------------------------------------------------------------------
// fetchCompanionFiles
// ---------------------------------------------------------------------------

describe("fetchCompanionFiles", () => {
  it("fetches files listed by the API", () => {
    const localDir = join(tmpDir, "skill");
    mkdirSync(localDir);
    writeFileSync(join(localDir, "SKILL.md"), "---\nname: test\n---\n# Test");

    const fetcher = createMockFetcher({
      "document-skills/pdf": [
        { name: "SKILL.md", path: "document-skills/pdf/SKILL.md", type: "file", sha: "abc1", download_url: "https://raw.example/SKILL.md" },
        { name: "forms.md", path: "document-skills/pdf/forms.md", type: "file", sha: "abc2", download_url: "https://raw.example/forms.md" },
        { name: "reference.md", path: "document-skills/pdf/reference.md", type: "file", sha: "abc3", download_url: "https://raw.example/reference.md" },
      ],
    });

    const result = fetchCompanionFiles("owner/repo", "document-skills/pdf", localDir, { fetcher });

    expect(result.fetched).toEqual(["forms.md", "reference.md"]);
    expect(result.errors).toEqual([]);
    expect(existsSync(join(localDir, "forms.md"))).toBe(true);
    expect(existsSync(join(localDir, "reference.md"))).toBe(true);
  });

  it("skips SKILL.md (already present)", () => {
    const localDir = join(tmpDir, "skill");
    mkdirSync(localDir);
    writeFileSync(join(localDir, "SKILL.md"), "---\nname: test\n---\n");

    const fetcher = createMockFetcher({
      "pdf": [
        { name: "SKILL.md", path: "pdf/SKILL.md", type: "file", sha: "x", download_url: "https://x/SKILL.md" },
        { name: "extra.md", path: "pdf/extra.md", type: "file", sha: "x", download_url: "https://x/extra.md" },
      ],
    });

    const result = fetchCompanionFiles("o/r", "pdf", localDir, { fetcher });
    expect(result.fetched).toEqual(["extra.md"]);
    // SKILL.md download should NOT have been called
    expect(fetcher.downloads.every(d => !d.endsWith("SKILL.md"))).toBe(true);
  });

  it("skips files that already exist locally", () => {
    const localDir = join(tmpDir, "skill");
    mkdirSync(localDir);
    writeFileSync(join(localDir, "SKILL.md"), "---\nname: test\n---\n");
    writeFileSync(join(localDir, "forms.md"), "existing content");

    const fetcher = createMockFetcher({
      "pdf": [
        { name: "SKILL.md", path: "pdf/SKILL.md", type: "file", sha: "x", download_url: "https://x/SKILL.md" },
        { name: "forms.md", path: "pdf/forms.md", type: "file", sha: "x", download_url: "https://x/forms.md" },
        { name: "new.md", path: "pdf/new.md", type: "file", sha: "x", download_url: "https://x/new.md" },
      ],
    });

    const result = fetchCompanionFiles("o/r", "pdf", localDir, { fetcher });
    expect(result.fetched).toEqual(["new.md"]);
    // forms.md should not have been overwritten
    expect(readFileSync(join(localDir, "forms.md"), "utf8")).toBe("existing content");
  });

  it("respects companions: field in SKILL.md frontmatter", () => {
    const localDir = join(tmpDir, "skill");
    mkdirSync(localDir);
    writeFileSync(join(localDir, "SKILL.md"), "---\nname: pdf\ncompanions: [forms.md]\n---\n# PDF");

    const fetcher = createMockFetcher({
      "pdf": [
        { name: "SKILL.md", path: "pdf/SKILL.md", type: "file", sha: "x", download_url: "https://x/SKILL.md" },
        { name: "forms.md", path: "pdf/forms.md", type: "file", sha: "x", download_url: "https://x/forms.md" },
        { name: "reference.md", path: "pdf/reference.md", type: "file", sha: "x", download_url: "https://x/reference.md" },
        { name: "LICENSE.txt", path: "pdf/LICENSE.txt", type: "file", sha: "x", download_url: "https://x/LICENSE.txt" },
      ],
    });

    const result = fetchCompanionFiles("o/r", "pdf", localDir, { fetcher });
    // Only forms.md should be fetched (declared in companions)
    expect(result.fetched).toEqual(["forms.md"]);
    expect(existsSync(join(localDir, "reference.md"))).toBe(false);
  });

  it("fetches directories recursively", () => {
    const localDir = join(tmpDir, "skill");
    mkdirSync(localDir);
    writeFileSync(join(localDir, "SKILL.md"), "---\nname: test\n---\n");

    const fetcher = createMockFetcher({
      "pdf": [
        { name: "SKILL.md", path: "pdf/SKILL.md", type: "file", sha: "x", download_url: "https://x/SKILL.md" },
        { name: "scripts", path: "pdf/scripts", type: "dir", sha: "x", download_url: null },
      ],
      "pdf/scripts": [
        { name: "check.py", path: "pdf/scripts/check.py", type: "file", sha: "x", download_url: "https://x/check.py" },
        { name: "fill.py", path: "pdf/scripts/fill.py", type: "file", sha: "x", download_url: "https://x/fill.py" },
      ],
    });

    const result = fetchCompanionFiles("o/r", "pdf", localDir, { fetcher });
    expect(result.fetched).toEqual(["scripts/ (2 files)"]);
    expect(existsSync(join(localDir, "scripts", "check.py"))).toBe(true);
    expect(existsSync(join(localDir, "scripts", "fill.py"))).toBe(true);
  });

  it("falls back to git clone when API fails", () => {
    const localDir = join(tmpDir, "skill");
    mkdirSync(localDir);
    writeFileSync(join(localDir, "SKILL.md"), "---\nname: test\n---\n");

    const fetcher = createFailingFetcher();
    // This will attempt git clone which will also fail in test env
    const result = fetchCompanionFiles("o/r", "pdf", localDir, { fetcher });
    // Should report git clone failure
    expect(result.errors.length).toBeGreaterThan(0);
  });

  it("vendors to target dir when vendorDir is set", () => {
    const localDir = join(tmpDir, "skill");
    const vendorDir = join(tmpDir, "vendor", "pdf");
    mkdirSync(localDir);
    writeFileSync(join(localDir, "SKILL.md"), "---\nname: test\n---\n");

    const fetcher = createMockFetcher({
      "pdf": [
        { name: "SKILL.md", path: "pdf/SKILL.md", type: "file", sha: "x", download_url: "https://x/SKILL.md" },
        { name: "forms.md", path: "pdf/forms.md", type: "file", sha: "x", download_url: "https://x/forms.md" },
      ],
    });

    fetchCompanionFiles("o/r", "pdf", localDir, { fetcher, vendorDir });
    expect(existsSync(join(vendorDir, "SKILL.md"))).toBe(true);
    expect(existsSync(join(vendorDir, "forms.md"))).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// findIncompleteSkills
// ---------------------------------------------------------------------------

describe("findIncompleteSkills", () => {
  it("returns empty for skills without companions field", () => {
    const root = join(tmpDir, "skills");
    mkdirSync(join(root, "content", "pdf"), { recursive: true });
    writeFileSync(join(root, "content", "pdf", "SKILL.md"), "---\nname: pdf\n---\n# PDF");

    expect(findIncompleteSkills(root)).toEqual([]);
  });

  it("detects missing companions", () => {
    const root = join(tmpDir, "skills");
    mkdirSync(join(root, "content", "pdf"), { recursive: true });
    writeFileSync(
      join(root, "content", "pdf", "SKILL.md"),
      "---\nname: pdf\ncompanions: [scripts/, forms.md]\n---\n# PDF",
    );

    const result = findIncompleteSkills(root);
    expect(result).toHaveLength(1);
    expect(result[0]!.id).toBe("content/pdf");
    expect(result[0]!.missing).toEqual(["scripts/", "forms.md"]);
  });

  it("reports only missing companions (not present ones)", () => {
    const root = join(tmpDir, "skills");
    const skillDir = join(root, "content", "pdf");
    mkdirSync(skillDir, { recursive: true });
    writeFileSync(
      join(skillDir, "SKILL.md"),
      "---\nname: pdf\ncompanions: [scripts/, forms.md]\n---\n# PDF",
    );
    writeFileSync(join(skillDir, "forms.md"), "forms content");

    const result = findIncompleteSkills(root);
    expect(result).toHaveLength(1);
    expect(result[0]!.missing).toEqual(["scripts/"]);
  });

  it("returns empty when all companions are present", () => {
    const root = join(tmpDir, "skills");
    const skillDir = join(root, "content", "pdf");
    mkdirSync(join(skillDir, "scripts"), { recursive: true });
    writeFileSync(
      join(skillDir, "SKILL.md"),
      "---\nname: pdf\ncompanions: [scripts/, forms.md]\n---\n# PDF",
    );
    writeFileSync(join(skillDir, "forms.md"), "forms");

    expect(findIncompleteSkills(root)).toEqual([]);
  });

  it("returns empty for non-existent root", () => {
    expect(findIncompleteSkills("/nonexistent/path")).toEqual([]);
  });
});

// ---------------------------------------------------------------------------
// vendorSkill
// ---------------------------------------------------------------------------

describe("vendorSkill", () => {
  it("copies skill directory to vendor location", () => {
    const src = join(tmpDir, "src-skill");
    const dest = join(tmpDir, "vendor", "pdf");
    mkdirSync(join(src, "scripts"), { recursive: true });
    writeFileSync(join(src, "SKILL.md"), "# PDF");
    writeFileSync(join(src, "scripts", "check.py"), "print('ok')");

    const ok = vendorSkill(src, dest);
    expect(ok).toBe(true);
    expect(existsSync(join(dest, "SKILL.md"))).toBe(true);
    expect(existsSync(join(dest, "scripts", "check.py"))).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// .source file
// ---------------------------------------------------------------------------

describe("readSourceFile", () => {
  it("returns null when no .source file exists", () => {
    expect(readSourceFile(tmpDir)).toBeNull();
  });

  it("parses repo::skillPath format", () => {
    writeFileSync(join(tmpDir, ".source"), "ComposioHQ/awesome-claude-skills::document-skills/pdf");
    const result = readSourceFile(tmpDir);
    expect(result).toEqual({
      repo: "ComposioHQ/awesome-claude-skills",
      skillPath: "document-skills/pdf",
      ref: undefined,
    });
  });

  it("parses repo::skillPath@ref format", () => {
    writeFileSync(join(tmpDir, ".source"), "owner/repo::skills/test@v1.2.3");
    const result = readSourceFile(tmpDir);
    expect(result).toEqual({
      repo: "owner/repo",
      skillPath: "skills/test",
      ref: "v1.2.3",
    });
  });
});

// ---------------------------------------------------------------------------
// .source auto-write on fetch
// ---------------------------------------------------------------------------

describe("fetchCompanionFiles .source auto-write", () => {
  it("writes .source file after successful fetch", () => {
    const localDir = join(tmpDir, "skill");
    mkdirSync(localDir);
    writeFileSync(join(localDir, "SKILL.md"), "---\nname: test\n---\n");

    const fetcher = createMockFetcher({
      "document-skills/pdf": [
        { name: "SKILL.md", path: "x", type: "file", sha: "abc", download_url: "https://x/SKILL.md" },
        { name: "forms.md", path: "x", type: "file", sha: "def", download_url: "https://x/forms.md" },
      ],
    });

    fetchCompanionFiles("ComposioHQ/awesome-claude-skills", "document-skills/pdf", localDir, { fetcher });

    const source = readSourceFile(localDir);
    expect(source).toEqual({
      repo: "ComposioHQ/awesome-claude-skills",
      skillPath: "document-skills/pdf",
      ref: undefined,
    });
  });

  it("does not write .source when nothing was fetched", () => {
    const localDir = join(tmpDir, "skill");
    mkdirSync(localDir);
    writeFileSync(join(localDir, "SKILL.md"), "---\nname: test\n---\n");
    writeFileSync(join(localDir, "forms.md"), "already here");

    const fetcher = createMockFetcher({
      "pdf": [
        { name: "SKILL.md", path: "x", type: "file", sha: "a", download_url: "https://x/SKILL.md" },
        { name: "forms.md", path: "x", type: "file", sha: "b", download_url: "https://x/forms.md" },
      ],
    });

    fetchCompanionFiles("o/r", "pdf", localDir, { fetcher });
    expect(existsSync(join(localDir, ".source"))).toBe(false);
  });
});

// ---------------------------------------------------------------------------
// SHA256 sidecar files
// ---------------------------------------------------------------------------

describe("SHA256 integrity", () => {
  it("writes .sha256 sidecar files after download", () => {
    const localDir = join(tmpDir, "skill");
    mkdirSync(localDir);
    writeFileSync(join(localDir, "SKILL.md"), "---\nname: test\n---\n");

    const fetcher = createMockFetcher({
      "pdf": [
        { name: "SKILL.md", path: "x", type: "file", sha: "a", download_url: "https://x/SKILL.md" },
        { name: "check.py", path: "x", type: "file", sha: "b", download_url: "https://x/check.py" },
      ],
    });

    fetchCompanionFiles("o/r", "pdf", localDir, { fetcher });
    expect(existsSync(join(localDir, "check.py.sha256"))).toBe(true);
    // The sha256 file should contain a hex string
    const sha = readFileSync(join(localDir, "check.py.sha256"), "utf8");
    expect(sha).toMatch(/^[a-f0-9]{64}$/);
  });
});
