/**
 * `cue skills new <category/name>` — scaffold a new skill.
 */

import { mkdirSync, writeFileSync, existsSync, cpSync, readFileSync } from "node:fs";
import { resolve, dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const REPO_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..", "..");
const SKILLS_ROOT = join(REPO_ROOT, "resources", "skills", "skills");

export async function run(args: string[]): Promise<number> {
  let id = args.find(a => !a.startsWith("-"));
  const descIdx = args.indexOf("--description");
  const description = descIdx >= 0 ? args[descIdx + 1] ?? "" : "";
  const categoryIdx = args.indexOf("--category");
  const nameIdx = args.indexOf("--name");
  const fromIdx = args.indexOf("--from");
  const fromId = fromIdx >= 0 ? args[fromIdx + 1] ?? "" : "";

  // Support --category X --name Y form
  if (!id && categoryIdx >= 0 && nameIdx >= 0) {
    id = `${args[categoryIdx + 1]}/${args[nameIdx + 1]}`;
  }

  if (!id || !id.includes("/")) {
    process.stderr.write("Usage: cue skills new <category>/<name> [--from <source-id>]\n");
    process.stderr.write("       cue skills new --category review --name my-checker\n");
    return 1;
  }

  const [category, name] = id.split("/");
  const skillDir = join(SKILLS_ROOT, category!, name!);

  if (existsSync(skillDir)) {
    process.stderr.write(`Skill "${id}" already exists at ${skillDir}\n`);
    return 1;
  }

  // --from: copy from existing skill
  if (fromId) {
    const sourceDir = join(SKILLS_ROOT, fromId);
    if (!existsSync(sourceDir)) {
      process.stderr.write(`Source skill "${fromId}" not found at ${sourceDir}\n`);
      return 1;
    }
    cpSync(sourceDir, skillDir, { recursive: true });
    // Replace name in frontmatter
    const skillMd = join(skillDir, "SKILL.md");
    if (existsSync(skillMd)) {
      let content = readFileSync(skillMd, "utf8");
      content = content.replace(/^(name:\s*).+$/m, `$1${name}`);
      writeFileSync(skillMd, content);
    }
    process.stdout.write(`✅ Created skill: ${id} (from ${fromId})\n`);
    process.stdout.write(`   ${skillDir}/\n`);
    return 0;
  }

  mkdirSync(skillDir, { recursive: true });

  const desc = description || `When user asks for ${name!.replace(/-/g, " ")}, do this`;
  const template = `---
description: "${desc}"
tags: [${category}]
category: ${category}
version: 1.0.0
requires_mcps: []
---

# ${name!.replace(/-/g, " ").replace(/\b\w/g, c => c.toUpperCase())}

## When to use

Trigger this skill when the user asks for ${name!.replace(/-/g, " ")}.

## Instructions

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Examples

\`\`\`
User: [example input]
Action: [what to do]
\`\`\`

## Notes

- [Any constraints or edge cases]
`;

  writeFileSync(join(skillDir, "SKILL.md"), template);

  // Create test directory with example test
  mkdirSync(join(skillDir, "test"), { recursive: true });
  writeFileSync(join(skillDir, "test", "case-1.md"), `---
input: "${name!.replace(/-/g, " ")}"
expect_contains: ["${name!.split("-")[0]}"]
expect_not_contains: []
---
`);

  process.stdout.write(`✅ Created skill: ${id}\n`);
  process.stdout.write(`   ${skillDir}/SKILL.md\n`);
  process.stdout.write(`   ${skillDir}/test/case-1.md\n\n`);
  process.stdout.write(`Next steps:\n`);
  process.stdout.write(`  1. Edit SKILL.md with your instructions\n`);
  process.stdout.write(`  2. Add to a profile: cue skills add-to-profile ${id}\n`);
  process.stdout.write(`  3. Test: cue skills test ${id}\n`);
  return 0;
}
