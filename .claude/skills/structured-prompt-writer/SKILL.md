---
name: structured-prompt-writer
description: Structured AI prompt writing tool with 395+ built-in prompt templates. Supports both detailed mode and simple mode. Used for creating professional AI persona prompts, system prompts, or task prompts. Use this skill when the user needs to: (1) create a new AI prompt (2) design an AI persona (3) write a system prompt (4) optimize the structure of an existing prompt.
---

# Structured Prompt Writer

Create professional AI prompts with **395+ built-in prompt templates**. Supports detailed mode (complex personas / specialized domains) and simple mode (single tasks / rapid deployment).

## Built-in Resources

| Category | Count | Description |
|------|------|------|
| Structured Personas | 5 | High-quality Chinese structured prompts |
| Xiaohongshu (RedNote) Series | 4 | Dedicated to Xiaohongshu operations |
| Creative Writing | 3 | Prompts for creative work |
| GPT Store | 282 | Prompts from OpenAI's GPT Store |
| System Prompts | 101 | Tools like Claude / Cursor / Gemini |

## Writing Workflow

```
Choose mode → Gather requirements → Pick a template → Fill in content → Polish style → Validate output
```

## Mode Selection

**Detailed Mode** — use for:
- Complex role-playing (experts, masters, mentors, celebrity avatars)
- Specialized domain applications (product design, content operations, financial analysis, medical consulting)
- Scenarios that require multi-turn, in-depth interaction
- Scenarios that need a multi-dimensional knowledge framework

**Simple Mode** — use for:
- Single creative tasks (writing, translation, summarization, rewriting)
- Utility assistants (code generation, format conversion, data processing)
- Lightweight scenarios for rapid deployment
- Simple, rule-driven tasks

## Core Format

### Required Elements (shared by both modes)

```markdown
# [Persona Name]

━━━━━━━━
## Requirements
: Input   [Description of user input]
: Output  [Description of AI output]
: Model   Gemini 3.0 Pro / Claude Sonnet 4.5
: Author  [Author name]
: Version [Version number]

## Initialization
[Opening line for the persona, written in first person, guiding the user to start interacting]
```

### Extra Elements for Detailed Mode

| Section | Purpose | Description |
|------|------|------|
| `## Essence / Worldview` | Core mindset of the persona | Use poetic language to describe the persona's way of thinking and values |
| `## Knowledge / Framework` | Multi-dimensional knowledge structure | Use ①②③ and tree structures to lay out knowledge dimensions |
| `## Methodology / Process` | Tree-shaped workflow | Use `├─` `└─` to express processing logic |
| `## Taboos / Constraints` | Rules and boundaries | Make clear what the persona will not do |
| `## Interaction Protocol` | Interaction details | Mark specific protocols with `〖〗` |

### Extra Elements for Simple Mode

| Section | Purpose | Description |
|------|------|------|
| `## Essence` | 1–2 paragraphs on core traits | Briefly describe the persona's positioning |
| `## Rules` | 3–5 core rules | Use ①②③ lists |
| `## Process` | Steps linked by arrows | `Step 1 → Step 2 → Step 3` |

### Format Symbols Cheat Sheet

| Symbol | Purpose | Example |
|------|------|------|
| ━━━━ | Section divider | 8–16 full-width em dashes |
| : | Requirement definition | `: Input text` |
| ├─ └─ | Tree structure | Show hierarchy |
| ▸ | Points to an explanation | `Core ▸ Explanation` |
| ▪ | Unordered list | Enumerate key points |
| ① ② ③ | Ordered steps | Knowledge dimensions / rules |
| 『』 | Emphasized title | `『Minimalist Aesthetics』` |
| 〖〗 | Protocol title | `〖Refuse Ambiguity〗` |
| ? | Conditional trigger | `? Upon receiving the proposal` |

## Writing Principles

**Poetic Opening**
Use metaphor to describe the essence of the persona. Avoid mechanical phrasing like "I am an AI assistant."
> You are a solitary golfer, and also a relentless product craftsman.

**Inject Humanity**
Expose personality, values, even small flaws — give the persona warmth.
> Let me say up front: I might just tell you flat out that it's garbage.

**Restrained Precision**
Be as concise as an instruction manual. Every sentence must earn its place.

**Anti-AI Flavor**
Avoid clichés, pursue a distinctive voice, and reject corporate jargon like "empower, lever, closed loop."

## Reference Resources

The skill ships with a rich set of examples — consult them as needed:

| Resource | Path | Description |
|------|------|------|
| Format Templates | [format-templates.md](references/format-templates.md) | Complete templates for detailed / simple modes |
| Example Prompts | [example-prompts.md](references/example-prompts.md) | Side-by-side comparison of two complete examples |
| Prompt Catalog | [prompt-catalog.md](references/prompt-catalog.md) | Full index of 395+ prompts |

### Built-in Prompt Library

```
references/prompts/
├── personas/           # Structured personas (5)
│   ├── Zhang Xiaolong AI Avatar.md
│   ├── Dangnian Mingyue.md
│   └── ...
├── xiaohongshu/        # Xiaohongshu (RedNote) series (4)
│   ├── Xiaohongshu Viral Account Positioning Architect.md
│   └── ...
├── creative/           # Creative writing (3)
│   ├── God of Micro-Sci-Fi.md
│   ├── LangGPT.md
│   └── Xiaohongshu Writing Expert.md
├── gpts-personas/      # GPT Store (282)
│   ├── Grimoire.md
│   ├── Mr. Ranedeer.md
│   ├── 10x Engineer.md
│   └── ...
├── system-tools/       # System prompts (101)
│   ├── Anthropic/
│   ├── Cursor Prompts/
│   ├── Google/
│   ├── Open Source prompts/
│   └── ...
└── awesome-chatgpt-prompts.md  # ChatGPT collection
```

## Quick Start

1. **Pick a mode**: detailed mode for complex personas, simple mode for simple tasks
2. **Review the template**: read `format-templates.md` for the complete format
3. **Consult examples**: pick a similar scenario from `references/prompts/`
   - Learning structured format → `personas/`
   - Xiaohongshu operations → `xiaohongshu/`
   - Looking for a specific function → `gpts-personas/`
   - Studying system prompts → `system-tools/`
4. **Fill in content**: complete each section following the template structure
5. **Audit the style**: make sure it follows the principles of "poetic opening, injected humanity, restrained precision, anti-AI flavor"
