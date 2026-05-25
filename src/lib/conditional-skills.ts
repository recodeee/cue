/**
 * Conditional skill loading — gate skills based on cwd file/dir presence or env vars.
 */

import { existsSync, readdirSync } from "node:fs";
import { join } from "node:path";

export interface SkillCondition {
  has_file?: string | string[];
  has_dir?: string | string[];
  env?: string | string[];
}

export interface ConditionalSkill {
  id: string;
  when: SkillCondition;
}

/** Check if a single file pattern exists in cwd. Supports simple glob (*) at start. */
function fileExists(pattern: string, cwd: string): boolean {
  if (pattern.startsWith("*.")) {
    const ext = pattern.slice(1); // e.g. ".pdf"
    try {
      return readdirSync(cwd).some(f => f.endsWith(ext));
    } catch { return false; }
  }
  return existsSync(join(cwd, pattern));
}

/** Check if a directory exists in cwd. */
function dirExists(name: string, cwd: string): boolean {
  // Strip trailing slash for consistency
  const clean = name.endsWith("/") ? name.slice(0, -1) : name;
  try {
    const { statSync } = require("node:fs");
    return statSync(join(cwd, clean)).isDirectory();
  } catch { return false; }
}

function toArray(v: string | string[] | undefined): string[] {
  if (!v) return [];
  return Array.isArray(v) ? v : [v];
}

/**
 * Evaluate whether a condition is met in the given cwd.
 * All specified checks must pass (AND logic within a condition).
 */
export function evaluateCondition(condition: SkillCondition, cwd: string): boolean {
  const files = toArray(condition.has_file);
  const dirs = toArray(condition.has_dir);
  const envs = toArray(condition.env);

  // has_file: at least one must exist
  if (files.length > 0 && !files.some(f => fileExists(f, cwd))) return false;

  // has_dir: at least one must exist
  if (dirs.length > 0 && !dirs.some(d => dirExists(d, cwd))) return false;

  // env: all must be set
  if (envs.length > 0 && !envs.every(e => process.env[e] !== undefined)) return false;

  return true;
}

/**
 * Filter conditional skills, returning IDs of those whose conditions pass.
 */
export function filterConditionalSkills(skills: ConditionalSkill[], cwd: string): string[] {
  return skills.filter(s => evaluateCondition(s.when, cwd)).map(s => s.id);
}
