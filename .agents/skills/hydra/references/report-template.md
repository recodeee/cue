# Hydra Report Template

Save to `.hydra/reports/hydra-YYYYMMDDTHHMMSS-{slug}.md`.
Slug = first 3-4 words, kebab-case, `[a-z0-9-]` only, max 40 chars. Fallback: `review`.
`{{TITLE}}` = one-line summary of the reviewed subject, derived from user's input.
Create `.hydra/.gitignore` with `*` on first run.

**Status labels:**
- `responded` -- advisor/reviewer completed successfully
- `timeout` -- spawned but did not respond within 120s
- `not run` -- excluded by active mode (e.g., Navigator/Volta in standard mode)

**Mode-aware section rules:**
- Keep status table rows for excluded roles as `not run`. Omit their full response sections.
- Omit `## Peer Reviews` entirely if no reviewers ran (standard, or deep --no-review).
- Omit `### Cross-Model Signals` if Opus-only.
- Omit `## Blind Spots` if no reviewers ran (blind spots come from reviewer labels).
- Omit `## Decision Rationale` if no reviewers ran (chairman without reviewers produces simpler output).
- In `--no-codex`: replace "Codex" with "Opus" in Model column.
- Thresholds and mode definitions: see SKILL.md Modes table (single source of truth).
- If fewer than expected responded, add after the Verdict heading:
  `> **Note:** Degraded confidence -- only {{N}} of {{EXPECTED}} responded (score capped at 25, forced LOW).`
- `is_windowed`: `true` for branch/iterate/pr reviews (diff_context active); `false` for `hydra this`. Emit as unquoted YAML boolean (`is_windowed: true` -- NOT `"true"`).
- `scope_pct`: integer 0-100 when `is_windowed: true`; YAML `null` (bareword, unquoted) when `false`. Never emit the string `"null"`. Sourced from SKILL.md Step 1 scope metrics; matches the `SCOPE` line in the in-conversation summary.

---

## Report

```markdown
---
hydra_version: "1.0"
timestamp: "{{TIMESTAMP}}"
question_type: "{{QUESTION_TYPE}}"
mode: "{{MODE}}"
severity_counts: {critical: {{CRITICAL_COUNT}}, serious: {{SERIOUS_COUNT}}, moderate: {{MODERATE_COUNT}}}
confidence_score: {{CONFIDENCE_SCORE}}
confidence_label: "{{CONFIDENCE_LABEL}}"
is_windowed: {{IS_WINDOWED}}
scope_pct: {{SCOPE_PCT_OR_NULL}}
top_actions:
  - id: A1
    severity: "{{A1_SEVERITY}}"
    file: "{{A1_FILE}}"
    lines: "{{A1_LINES}}"
    effort: "{{A1_EFFORT}}"
    summary: "{{A1_SUMMARY}}"
reviewed_files: {{REVIEWED_FILES_LIST}}
iteration: {{ITERATION_NUMBER}}
previous_report: {{PREV_REPORT_PATH_OR_NULL}}
---

# Hydra Report: {{TITLE}}

> {{TIMESTAMP}} | {{QUESTION_TYPE}}

| Role | Model | Status | Position |
|------|-------|--------|----------|
| Cassandra | Opus | {{responded/timeout}} | {{APPROVE/CONCERN/REJECT/N/A}} |
| Mies+ | {{Model}} | {{responded/timeout}} | {{position}} |
| Navigator | Opus | {{responded/timeout/not run}} | {{position}} |
| Volta | Opus | {{responded/timeout/not run}} | {{position}} |
| Sentinel | {{Model}} | {{responded/timeout}} | {{position}} |
| Echo | Opus | {{responded/timeout}} | {{position}} |

**Navigation:** [Verdict](#verdict) | [Actions](#actions) | [Consensus](#consensus-map) | [Advisors](#full-advisor-responses) | [Reviews](#peer-reviews)

---

## Verdict

{{CHAIRMAN_VERDICT}}

---

## Actions

Priority order -- fix in sequence when dependencies exist:

### A1 -- {{SEVERITY}} -- {{FILE}}:{{LINES}} -- Est: {{EFFORT}}

**What:** {{DESCRIPTION}}
**Why:** {{RATIONALE}}
**How:** {{CONCRETE_FIX_OR_DIFF}}
**Dependency:** {{BLOCKS_NOTE_OR_NONE}}
**Verified by:** {{ADVISOR_NAMES}}

[Repeat for each Top Action]

---

## Consensus Map

| Advisor (Model) | Position | Key Finding | Evidence | Agrees With |
|-----------------|----------|-------------|----------|-------------|
{{CHAIRMAN_CONSENSUS_MAP}}

Legend: Evidence = count of [VERIFIED] findings. Agrees With = advisor(s) who found the same issue.

### Cross-Model Signals

{{Where Opus and Codex diverged or converged -- highest-value insights}}

---

## Decision Rationale

{{CHAIRMAN_DECISION_RATIONALE}}

---

## Blind Spots

{{Gaps identified by reviewers: [SHARED BLIND SPOT] labels, [CRITICAL MISS] labels, areas no advisor examined}}

---

## Reviewer Highlights

{{Synthesized: strongest/weakest advisor, shared blind spots, devil's advocate counter-case}}

---

## The Question

{{FRAMED_QUESTION}}

---

## Full Advisor Responses

### Cassandra -- Failure Archaeologist (Opus)
{{FULL_RESPONSE or [TIMEOUT]}}

### Mies+ -- Reductionist & Adversarial First-Reader ({{Model}})
{{FULL_RESPONSE or [TIMEOUT]}}

### Navigator -- Systems Cartographer (Opus)
{{FULL_RESPONSE or [TIMEOUT]}}

### Volta -- Efficiency Surgeon (Opus)
{{FULL_RESPONSE or [TIMEOUT]}}

### Sentinel -- Adversarial Security ({{Model}})
{{FULL_RESPONSE or [TIMEOUT]}}

### Echo -- AI-Assisted-Development Reviewer (Opus)
{{FULL_RESPONSE or [TIMEOUT]}}

---

## Peer Reviews

### Reviewer 1 -- Cross-Examiner (Opus)
{{FULL_REVIEW or [TIMEOUT]}}

### Reviewer 2 -- Effort-Risk Ranker (Opus)
{{FULL_REVIEW or [TIMEOUT]}}

### Reviewer 3 -- Devil's Advocate (Opus)
{{FULL_REVIEW or [TIMEOUT]}}

---

*Hydra | Based on Karpathy's LLM Council methodology | MIT License*
```

---

## In-Conversation Summary

Map question type to signal line:
- CODE_REVIEW -> severity counts + one-sentence quality assessment
- ARCHITECTURE_DECISION -> CONFIDENCE level
- SECURITY_AUDIT -> RISK LEVEL
- DEBUGGING -> ROOT-CAUSE CONFIDENCE

```
## Hydra: {{TITLE}}

SEVERITY   CRITICAL [{{N}}]  SERIOUS [{{N}}]  MODERATE [{{N}}]
CONFIDENCE {{SCORE}}% ({{LABEL}}) -- {{N}}/{{M}} advisors -- {{cross-model|opus-only}}
{{IF diff_context}} SCOPE    {{DIFF_LINES}}/{{EST_TOTAL_LINES}} lines ({{SCOPE_PCT}}%) -- diff-anchored review{{ENDIF}}
VERDICT    {{ONE sentence from chairman. Active voice. No hedging.}}

--- ACTION REQUIRED ---
1. [{{SEVERITY}}] {{file:line}} -- {{what + why}}. Est: {{effort}}.
2. [{{SEVERITY}}] {{file:line}} -- {{what + why}}. Est: {{effort}}.
3. [{{SEVERITY}}] {{file:line}} -- {{what + why}}. Est: {{effort}}.
--- END ACTIONS ---

TENSION  {{Advisor vs Advisor -> Reason -> Ruling}}
INSIGHT  {{Non-obvious compound finding from chairman. 1-2 sentences.}}

Full report: `.hydra/reports/hydra-{{TIMESTAMP}}-{{SLUG}}.md`
```

---

## In-Conversation Summary -- Iteration Mode (if `HYDRA_ITERATE`)

Use the chairman's DELTA BLOCK instead of the standard summary:

```
## Hydra Delta: {{TITLE}} (Iteration {{N}})

PROGRESS  {{X}}/{{Y}} previous actions addressed
TREND     {{Improving/Stable/Degrading}} -- CRITICAL: {{prev}} -> {{now}}, SERIOUS: {{prev}} -> {{now}}

FIXED     {{resolved actions with evidence}}
REMAINING {{unresolved actions -- why?}}
REGRESSION {{things that WERE working and now aren't}}
NEW       {{findings not in previous review}}

NEXT STEP  {{ONE action}}

Full report: `.hydra/reports/hydra-{{TIMESTAMP}}-{{SLUG}}.md`
Previous:    `{{PREV_REPORT}}`
```

---

## Transcript (if `--transcript`)

Save raw outputs to `.hydra/reports/hydra-YYYYMMDDTHHMMSS-{slug}-transcript.md`.
Dump each section under its heading. Include advisor label mappings (A=Cassandra, etc.).
