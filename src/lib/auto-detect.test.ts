import { describe, expect, test, beforeEach, afterEach } from "bun:test";
import { mkdtempSync, rmSync, writeFileSync, mkdirSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

import { detectProfile, detectProfileV2 } from "./auto-detect";

let tmp: string;

beforeEach(() => {
  tmp = mkdtempSync(join(tmpdir(), "cue-detect-"));
});
afterEach(() => {
  try { rmSync(tmp, { recursive: true, force: true }); } catch {}
});

describe("detectProfileV2", () => {
  test("Cargo.toml → rust with 0.9 confidence", () => {
    writeFileSync(join(tmp, "Cargo.toml"), "[package]");
    const results = detectProfileV2(tmp);
    const rust = results.find(r => r.profile === "rust");
    expect(rust).toBeDefined();
    expect(rust!.confidence).toBe(0.9);
    expect(rust!.reasons).toContain("Cargo.toml");
  });

  test("Cargo.toml + src/main.rs → rust-cli at 0.7", () => {
    writeFileSync(join(tmp, "Cargo.toml"), "[package]");
    mkdirSync(join(tmp, "src"));
    writeFileSync(join(tmp, "src/main.rs"), "fn main() {}");
    const results = detectProfileV2(tmp);
    const cli = results.find(r => r.profile === "rust-cli");
    expect(cli).toBeDefined();
    expect(cli!.confidence).toBe(0.7);
  });

  test("package.json with next → nextjs 0.9", () => {
    writeFileSync(join(tmp, "package.json"), JSON.stringify({ dependencies: { next: "14.0.0" } }));
    const results = detectProfileV2(tmp);
    const nextjs = results.find(r => r.profile === "nextjs");
    expect(nextjs).toBeDefined();
    expect(nextjs!.confidence).toBe(0.9);
  });

  test("package.json with react (no next) → frontend 0.8", () => {
    writeFileSync(join(tmp, "package.json"), JSON.stringify({ dependencies: { react: "18.0.0" } }));
    const results = detectProfileV2(tmp);
    const frontend = results.find(r => r.profile === "frontend");
    expect(frontend).toBeDefined();
    expect(frontend!.confidence).toBe(0.8);
  });

  test("package.json with no framework → backend 0.6", () => {
    writeFileSync(join(tmp, "package.json"), JSON.stringify({ dependencies: { express: "4.0.0" } }));
    const results = detectProfileV2(tmp);
    const backend = results.find(r => r.profile === "backend");
    expect(backend).toBeDefined();
    expect(backend!.confidence).toBeGreaterThanOrEqual(0.6);
  });

  test("go.mod → go-api 0.8", () => {
    writeFileSync(join(tmp, "go.mod"), "module example.com/app");
    const results = detectProfileV2(tmp);
    const goApi = results.find(r => r.profile === "go-api");
    expect(goApi).toBeDefined();
    expect(goApi!.confidence).toBe(0.8);
  });

  test("empty dir returns empty", () => {
    const results = detectProfileV2(tmp);
    expect(results).toEqual([]);
  });

  test("results sorted by confidence descending, max 5", () => {
    writeFileSync(join(tmp, "Cargo.toml"), "");
    mkdirSync(join(tmp, "src"));
    writeFileSync(join(tmp, "src/main.rs"), "");
    writeFileSync(join(tmp, "go.mod"), "");
    writeFileSync(join(tmp, "package.json"), JSON.stringify({ dependencies: { next: "14" } }));
    mkdirSync(join(tmp, ".github"));
    mkdirSync(join(tmp, ".github/workflows"));
    const results = detectProfileV2(tmp);
    expect(results.length).toBeLessThanOrEqual(5);
    for (let i = 1; i < results.length; i++) {
      expect(results[i]!.confidence).toBeLessThanOrEqual(results[i - 1]!.confidence);
    }
  });
});

describe("detectProfile (v1 compat)", () => {
  test("returns results with confidence 0-100", () => {
    writeFileSync(join(tmp, "Cargo.toml"), "");
    const results = detectProfile(tmp);
    expect(results.length).toBeGreaterThan(0);
    expect(results[0]!.confidence).toBeGreaterThan(0);
    expect(results[0]!.confidence).toBeLessThanOrEqual(100);
  });
});
