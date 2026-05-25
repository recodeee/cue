/**
 * Lazy skill loading — generate stubs and manifests for deferred skill bodies.
 */

import type { ResolvedProfile } from "../../profiles/_types";

/**
 * Generate a minimal SKILL.md stub with just name + description.
 */
export function generateSkillStub(skillId: string, description: string): string {
  const name = skillId.split("/").pop() ?? skillId;
  return `---
name: ${name}
description: "${description}"
---

# ${name}

${description}

> Full skill body available on demand. Reference this skill by name to load it.
`;
}

/**
 * Generate a CLAUDE.md manifest section listing all available lazy skills.
 */
export function generateLazyManifest(skills: { id: string; description: string }[]): string {
  if (skills.length === 0) return "";
  let out = `## Available Skills (lazy-loaded)\n\n`;
  out += `The following skills are available. Ask for the full body by name when needed:\n\n`;
  for (const s of skills) {
    const name = s.id.split("/").pop() ?? s.id;
    out += `- **${name}** (\`${s.id}\`): ${s.description}\n`;
  }
  out += `\n> To use a skill, reference it by name. The full instructions will be loaded on demand.\n`;
  return out;
}

/**
 * Check if a profile has lazy mode enabled.
 */
export function isLazyEnabled(profile: ResolvedProfile): boolean {
  return (profile as any).lazy === true;
}
