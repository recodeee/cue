/**
 * Regression tests for suggestProfiles — the profile mapper that decides which
 * cue profile pages a discovered skill lands on.
 *
 * Locks in known-bad mismaps:
 *   - korean-privacy-terms landed in frontend/nextjs (single `nextjs` tag)
 *   - russian-text-quality landed in frontend (single `vue-i18n` tag)
 *   - bbc-skill (Bilibili scraper) landed in frontend (incidental css+tailwind)
 *   - fs25-claude-skill (Farming Simulator) landed in core only — kept that way
 *
 * Real positives must continue to map correctly.
 */

import { describe, expect, test } from "bun:test";
import { suggestProfiles, type GemRepo } from "./discover";

function gem(partial: Partial<GemRepo>): GemRepo {
  return {
    full_name: "",
    owner: "",
    name: "",
    description: "",
    stars: 0,
    forks: 0,
    created_at: new Date().toISOString(),
    pushed_at: new Date().toISOString(),
    topics: [],
    language: "",
    has_skill_md: false,
    has_claude_dir: false,
    has_mcp_sdk: false,
    gem_score: 0,
    suggested_profiles: [],
    suggested_mcps: [],
    suggested_clis: [],
    quality: 0,
    url: "",
    ...partial,
  };
}

describe("suggestProfiles — niche-subject veto for stack profiles", () => {
  test("korean-privacy-terms (legal-tech via Next.js) does NOT land in frontend/nextjs", () => {
    const r = gem({
      name: "korean-privacy-terms",
      description: "Generate compliant Korean privacy policies and terms of service automatically using local laws and updated Claude Code skills.",
      topics: ["agent-skills", "claude-code", "claude-skill", "korean-law", "legal-tech", "mdx", "nextjs", "privacy-policy", "shadcn-ui", "terms-of-service"],
      language: "Go Template",
    });
    const out = suggestProfiles(r);
    expect(out).not.toContain("frontend");
    expect(out).not.toContain("nextjs");
  });

  test("russian-text-quality (i18n linter) does NOT land in frontend via vue-i18n tag", () => {
    const r = gem({
      name: "russian-text-quality",
      description: "Analyze Russian text quality using automated checks for i18n, plural rules, and CLDR standards to ensure linguistic accuracy.",
      topics: ["agent-skills", "ai-agents", "claude-skill", "cldr", "codex-cli", "content-design", "cursor", "editorial", "i18n", "icu-messageformat", "info-style", "linter", "localization", "notion", "openclaw", "russian", "russian-language", "ux-writing", "vue-i18n"],
    });
    expect(suggestProfiles(r)).not.toContain("frontend");
  });

  test("bbc-skill (Bilibili scraper) does NOT land in frontend via incidental css/tailwind tags", () => {
    const r = gem({
      name: "bbc-skill",
      description: "Fetch Bilibili comments and video metadata for AI agent analysis using a zero-dependency CLI tool.",
      topics: ["automation", "backend", "basic", "bbc", "bilibili-api", "claude-code-skill", "css", "daisyui", "documentation", "machine-learning", "openclaw", "tailwind", "web-scraping"],
      language: "Python",
    });
    expect(suggestProfiles(r)).not.toContain("frontend");
  });

  test("Farming Simulator skill stays in core, not frontend/backend/python-api", () => {
    const r = gem({
      name: "fs25-claude-skill",
      description: "Automate Farming Simulator 25 mod development using a Claude skill trained on game APIs and common coding patterns.",
      topics: ["anthropic", "claude-ai", "claude-skill", "farming-simulator", "farming-simulator-25"],
      language: "Lua",
    });
    const out = suggestProfiles(r);
    expect(out).toEqual(["core"]);
  });
});

describe("suggestProfiles — real positives keep working", () => {
  test("a genuine pentest/recon skill still maps to cybersecurity", () => {
    const r = gem({
      name: "Claude-OSINT",
      description: "Claude skills for external recon, dorks, credential validators, and red-team tradecraft for authorized engagements.",
      topics: ["recon", "osint", "pentest", "red-team", "claude-skill"],
      language: "Python",
    });
    expect(suggestProfiles(r)).toContain("cybersecurity");
  });

  test("a Next.js skill with Next.js-focused description still maps to nextjs", () => {
    const r = gem({
      name: "next-auth-helpers",
      description: "Next.js App Router helpers for next-auth with server components and Vercel deploy presets.",
      topics: ["nextjs", "next.js", "vercel", "next-auth", "app-router", "server-component"],
      language: "TypeScript",
    });
    expect(suggestProfiles(r)).toContain("nextjs");
  });

  test("a real cybersecurity audit skill is not blocked by single-tag rule", () => {
    const r = gem({
      name: "vuln-scanner",
      description: "Automated vulnerability scanner with CVE lookup and OWASP top-10 checks.",
      topics: ["security", "vulnerability", "cve", "owasp"],
      language: "Go",
    });
    expect(suggestProfiles(r)).toContain("cybersecurity");
  });

  test("single-tag matches no longer auto-assign — distinct≥2 enforced", () => {
    const r = gem({
      name: "some-skill",
      description: "Does a thing.",
      topics: ["nextjs"], // single keyword, single distinct hit
    });
    const out = suggestProfiles(r);
    expect(out).toEqual(["core"]);
  });
});
