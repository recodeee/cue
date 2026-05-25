/**
 * Context-aware auto-profile detection.
 * Scans cwd for project signals and scores against known profiles.
 */

import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

interface Signal {
  file: string;       // glob-like path to check (relative to cwd)
  weight: number;
  profile: string;
}

const SIGNALS: Signal[] = [
  // Frontend / Next.js
  { file: "next.config.js", weight: 5, profile: "nextjs" },
  { file: "next.config.ts", weight: 5, profile: "nextjs" },
  { file: "next.config.mjs", weight: 5, profile: "nextjs" },
  { file: "app/layout.tsx", weight: 4, profile: "nextjs" },
  { file: "app/page.tsx", weight: 3, profile: "nextjs" },
  { file: "next.config.js", weight: 4, profile: "frontend" },
  { file: "next.config.ts", weight: 4, profile: "frontend" },
  { file: "next.config.mjs", weight: 4, profile: "frontend" },
  { file: "vite.config.ts", weight: 4, profile: "frontend" },
  { file: "vite.config.js", weight: 4, profile: "frontend" },
  { file: "tailwind.config.js", weight: 3, profile: "frontend" },
  { file: "tailwind.config.ts", weight: 3, profile: "frontend" },
  { file: "postcss.config.js", weight: 2, profile: "frontend" },
  { file: "tsconfig.json", weight: 1, profile: "frontend" },

  // Backend (Node/TS)
  { file: "docker-compose.yml", weight: 3, profile: "backend" },
  { file: "docker-compose.yaml", weight: 3, profile: "backend" },
  { file: "Dockerfile", weight: 2, profile: "backend" },
  { file: "prisma/schema.prisma", weight: 4, profile: "backend" },
  { file: "migrations", weight: 3, profile: "backend" },
  { file: "drizzle.config.ts", weight: 4, profile: "backend" },
  { file: "src/server.ts", weight: 3, profile: "backend" },
  { file: "src/index.ts", weight: 1, profile: "backend" },
  { file: ".github/workflows/", weight: 1, profile: "backend" },

  // Python API
  { file: "pyproject.toml", weight: 4, profile: "python-api" },
  { file: "setup.py", weight: 3, profile: "python-api" },
  { file: "requirements.txt", weight: 3, profile: "python-api" },
  { file: "app/main.py", weight: 5, profile: "python-api" },
  { file: "main.py", weight: 3, profile: "python-api" },
  { file: "manage.py", weight: 5, profile: "python-api" },
  { file: "uvicorn.ini", weight: 4, profile: "python-api" },
  { file: "alembic.ini", weight: 4, profile: "python-api" },
  { file: ".python-version", weight: 2, profile: "python-api" },

  // Rust
  { file: "Cargo.toml", weight: 5, profile: "rust" },
  { file: "Cargo.lock", weight: 3, profile: "rust" },
  { file: "src/main.rs", weight: 4, profile: "rust" },
  { file: "src/lib.rs", weight: 3, profile: "rust" },
  { file: ".cargo/config.toml", weight: 2, profile: "rust" },

  // Rust CLI sub-profile
  { file: "src/main.rs", weight: 3, profile: "rust-cli" },
  { file: "Cargo.toml", weight: 3, profile: "rust-cli" },

  // Go API
  { file: "go.mod", weight: 5, profile: "go-api" },
  { file: "go.sum", weight: 3, profile: "go-api" },
  { file: "cmd/", weight: 3, profile: "go-api" },
  { file: "internal/", weight: 2, profile: "go-api" },
  { file: "main.go", weight: 4, profile: "go-api" },

  // Medusa
  { file: "medusa-config.js", weight: 5, profile: "medusa-dev" },
  { file: "medusa-config.ts", weight: 5, profile: "medusa-dev" },
  { file: "packages/medusa", weight: 5, profile: "medusa-dev" },

  // Docs
  { file: "astro.config.mjs", weight: 4, profile: "docs-writer" },
  { file: "docusaurus.config.js", weight: 4, profile: "docs-writer" },
  { file: "mkdocs.yml", weight: 4, profile: "docs-writer" },
  { file: "content/blog", weight: 3, profile: "docs-writer" },
  { file: "docs/", weight: 2, profile: "docs-writer" },

  // Fleet
  { file: ".colony", weight: 5, profile: "fleet-control" },
  { file: ".omx", weight: 4, profile: "fleet-control" },
  { file: "scripts/codex-fleet", weight: 5, profile: "fleet-control" },

  // Creative
  { file: "design-tokens", weight: 4, profile: "creative-media" },
  { file: "figma.config.ts", weight: 4, profile: "creative-media" },

  // Research
  { file: "research/", weight: 3, profile: "research" },
  { file: "papers/", weight: 3, profile: "research" },

  // Three.js
  { file: "three.js", weight: 4, profile: "threejs" },

  // ECC
  { file: "CLAUDE.md", weight: 2, profile: "ecc" },
  { file: ".claude/", weight: 2, profile: "ecc" },

  // Full (meta)
  { file: "profiles/", weight: 2, profile: "full" },
];

export interface DetectionResult {
  profile: string;
  score: number;
  maxScore: number;
  confidence: number; // 0-100
  signals: string[];  // which files matched
}

/**
 * V2 detection result with 0-1 confidence and reasons array.
 */
export interface DetectionResultV2 {
  profile: string;
  confidence: number; // 0.0 - 1.0
  reasons: string[];
}

/**
 * Read package.json dependencies to boost detection.
 */
function readPackageDeps(cwd: string): { deps: Set<string>; devDeps: Set<string> } {
  const deps = new Set<string>();
  const devDeps = new Set<string>();
  try {
    const raw = readFileSync(join(cwd, "package.json"), "utf8");
    const pkg = JSON.parse(raw);
    if (pkg.dependencies) for (const k of Object.keys(pkg.dependencies)) deps.add(k);
    if (pkg.devDependencies) for (const k of Object.keys(pkg.devDependencies)) devDeps.add(k);
  } catch { /* no package.json or invalid */ }
  return { deps, devDeps };
}

/**
 * Enhanced v2 detection with package.json awareness and 0-1 confidence.
 */
export function detectProfileV2(cwd: string): DetectionResultV2[] {
  const results = new Map<string, { confidence: number; reasons: string[] }>();

  function add(profile: string, confidence: number, reason: string) {
    const entry = results.get(profile) ?? { confidence: 0, reasons: [] };
    entry.confidence = Math.max(entry.confidence, confidence);
    entry.reasons.push(reason);
    results.set(profile, entry);
  }

  // File-based signals
  if (existsSync(join(cwd, "Cargo.toml"))) {
    add("rust", 0.9, "Cargo.toml");
    if (existsSync(join(cwd, "src/main.rs"))) add("rust-cli", 0.7, "src/main.rs");
  }
  if (existsSync(join(cwd, "go.mod"))) add("go-api", 0.8, "go.mod");
  if (existsSync(join(cwd, "pyproject.toml"))) add("python-api", 0.7, "pyproject.toml");
  if (existsSync(join(cwd, "requirements.txt"))) add("python-api", 0.7, "requirements.txt");
  if (existsSync(join(cwd, "docker-compose.yml")) || existsSync(join(cwd, "Dockerfile"))) {
    add("backend", 0.5, "docker-compose.yml/Dockerfile");
  }
  if (existsSync(join(cwd, ".github/workflows"))) add("backend", 0.3, ".github/workflows/");
  if (existsSync(join(cwd, "CLAUDE.md")) || existsSync(join(cwd, ".claude"))) {
    add("ecc", 0.4, "CLAUDE.md or .claude/");
  }
  if (existsSync(join(cwd, "profiles"))) add("full", 0.3, "profiles/ dir");

  // package.json-based signals
  if (existsSync(join(cwd, "package.json"))) {
    const { deps, devDeps } = readPackageDeps(cwd);
    const allDeps = new Set([...deps, ...devDeps]);
    if (allDeps.has("next")) add("nextjs", 0.9, "package.json has next");
    else if (allDeps.has("react")) add("frontend", 0.8, "package.json has react");
    else add("backend", 0.6, "package.json (no framework)");
  }

  return [...results.entries()]
    .map(([profile, { confidence, reasons }]) => ({ profile, confidence, reasons }))
    .sort((a, b) => b.confidence - a.confidence)
    .slice(0, 5);
}

export function detectProfile(cwd: string): DetectionResult[] {
  const scores = new Map<string, { score: number; max: number; signals: string[] }>();

  // Compute max possible score per profile
  for (const s of SIGNALS) {
    const entry = scores.get(s.profile) ?? { score: 0, max: 0, signals: [] };
    entry.max += s.weight;
    scores.set(s.profile, entry);
  }

  // Score based on what exists
  for (const s of SIGNALS) {
    const target = join(cwd, s.file);
    if (existsSync(target)) {
      const entry = scores.get(s.profile)!;
      entry.score += s.weight;
      entry.signals.push(s.file);
    }
  }

  return [...scores.entries()]
    .map(([profile, d]) => ({
      profile,
      score: d.score,
      maxScore: d.max,
      confidence: d.max > 0 ? Math.round((d.score / d.max) * 100) : 0,
      signals: d.signals,
    }))
    .filter(r => r.score > 0)
    .sort((a, b) => b.confidence - a.confidence || b.score - a.score);
}
