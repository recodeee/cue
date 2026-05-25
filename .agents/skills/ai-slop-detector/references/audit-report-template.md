# Audit Report Template

Every slop-cop audit produces a report in this format. The report has **two parallel verdicts** — AI-Slop and Comprehension — plus a single combined recommendation drawn from whichever axis is worse.

The structure scales with the verdicts. Two PASS verdicts can produce a 5-line report. Two CRITICAL verdicts need every section filled.

---

## Template

```markdown
# slop-cop Audit

## Verdicts

| Axis | Verdict | Density |
|---|---|---|
| AI-Slop | [PASS / LOW / MEDIUM / HIGH / CRITICAL] | D1 per 500w |
| Comprehension | [PASS / LOW / MEDIUM / HIGH / CRITICAL] | D2 per 500w |

**Combined recommendation:** [single sentence based on worse-of-two — see calibration.md §11]

## Stats

- Word count: N
- Audience detected: [casual / marketing / academic / encyclopedic / technical / fiction]
- Burstiness: 0.X (humans 0.6–1.2, AI 0.2–0.4)
- Likely model fingerprint: [none / GPT / Claude / Gemini / mixed]

## AI-Slop axis

### Counts
- High-severity: H1 per 500w
- Medium-severity: M1 per 500w
- Low-severity: L1 per 500w (informational)
- Computed density: D1

### Top fixes (AI-Slop)
1. **[Pattern or vocabulary name]** — "exact quote" → suggested rewrite
2. **[...]** — "..." → ...

### Mechanical violations (from scan.py — AI-Slop section)
[verbatim scanner output for slop axis]

### Qualitative violations (from reading)
- **[Pattern N: name]** (severity, group): "exact quote" → fix
- ...

### Calibration notes (AI-Slop)
- Genre adjustment applied: [details]
- Em-dash count: N (contested tell, weighted [0.5x / 1x])
- Compound triggers: [none / escalation reason]
- Sanded-prose signature: [present / absent]
- Uncanny-valley pattern: [present / absent]
- Model-fingerprint markers: [2-3 specific phrases supporting fingerprint, or "no clear fingerprint"]

## Comprehension axis

### Counts
- High-severity: H2 per 500w
- Medium-severity: M2 per 500w
- Low-severity: L2 per 500w (informational)
- Computed density: D2

### Readability metrics panel
- Flesch Reading Ease: X (target [Y–Z] for [audience])
- Flesch-Kincaid Grade: X (target [Y–Z])
- SMOG: X
- Coleman-Liau: X
- Dale-Chall: X
- Lexical density: X% (target [Y–Z]%)
- Avg sentence length: X words (target [Y–Z])
- Passive voice: X% (cap [Y]%)

### Density signals
- Acronym density: X per 100w (threshold 3+)
- Named-entity density: X per 100w (threshold 5+)
- Numeric claims per sentence (max): X (threshold 3+)
- Telegraphic colon-labels per paragraph (max): X (threshold 3+)
- Paragraph length (max): X sentences / Y words

### Top fixes (Comprehension)
1. **[Pattern name]** — "exact quote" → fix (e.g., define "SRA" inline)
2. **[...]** — "..." → ...

### Mechanical violations (from scan.py — Comprehension section)
[verbatim scanner output for comprehension axis]

### Qualitative violations (from reading)
- **[Pattern name]** (severity, group): "exact quote" → fix
- ...

### Calibration notes (Comprehension)
- Audience target: [audience]
- Metric panel hits/misses vs audience targets: [list]
- Compound triggers: [none / acronym window / named-entity window / paragraph length / etc.]

## Combined top 3 fixes

The highest-leverage edits across both axes, ordered by impact:

1. **[axis: pattern]** — "quote" → fix
2. **[axis: pattern]** — "quote" → fix
3. **[axis: pattern]** — "quote" → fix

## Combined recommended action

Choose one based on the cross-axis matrix in calibration.md §11:

- **Ship it.** Both verdicts PASS or LOW. Polish-pass at most.
- **Spot-fix listed items.** Both LOW or one MEDIUM. Apply the listed corrections.
- **Significant cleanup.** Both MEDIUM or one HIGH. The fixes overlap; tackle them together.
- **Substantial revision.** One HIGH, the other anything. Worse axis drives the work.
- **Recommend rewrite.** Both HIGH/CRITICAL, or either at CRITICAL. Cleaner to start over.

## If revising: clean rewrite

[Full revised text — only when in fix mode. Preserves meaning, addresses both axes' violations, hits the audience-specific metric targets. Re-scan after the rewrite.]
```

---

## Section-by-section guidance

### Verdicts header

The two-line table is the most-read part of the audit. The reader stops here if both verdicts are PASS or LOW. The combined recommendation is one sentence — pulled from the matrix in `calibration.md` §11.

Verdict tier maps directly to density score:

| Verdict | Density |
|---|---|
| PASS | 0–2 |
| LOW | 2–5 |
| MEDIUM | 5–10 |
| HIGH | 10–18 |
| CRITICAL | 18+ |

Same scale for both axes.

### Stats block

Always include word count, audience, burstiness, fingerprint. Audience is critical because it changes which thresholds apply (see calibration.md §10).

### AI-Slop axis section

Existing slop-cop logic. The 45 patterns + ~150 vocabulary tells + ~33 formatting tells. Mechanical violations come from scan.py; qualitative require reading.

### Comprehension axis section

The 35 comprehension patterns plus the 8 readability metrics + the 3 cold-reader-specific density signals (acronyms, named entities, numerics). Mechanical violations from scan.py (about 17 of 35 patterns are mechanically detectable); qualitative require reading.

The **readability metrics panel** is diagnostic, not part of the verdict score. The patterns drive the score; the metrics calibrate. When the panel and the patterns disagree (clean patterns, bad metrics), call it out.

### Combined top 3 fixes

Pull from both axes by impact:
1. The highest-impact item from whichever axis scored worse
2. The highest-impact item from the other axis
3. The next highest-impact item from the worse axis

This gives the reader maximum leverage in the smallest read.

### Combined recommended action

One sentence. Pulled from the cross-axis matrix in calibration.md §11. Don't restate the verdicts — the table already does that.

### When in fix mode (revise + audit)

The rewrite must address violations on both axes. Common synthesis points:
- Replace `delve`-class verbs (slop) AND define acronyms (comp)
- Cut em-dash clusters (slop) AND break long sentences (comp)
- Rewrite `serves as a beacon` (slop) AND add a thesis sentence (comp)
- Drop `Great question!` opener (slop) AND add a real first-sentence hook (comp)

Re-run scan.py after the rewrite. Both axes should drop to PASS or LOW.

---

## Tone and length guidance for the audit

- **Be specific.** Quote exact text. Reference exact pattern numbers/names.
- **Don't soften findings.** The audit's job is catching what the writer missed. If a draft fails one axis, say so.
- **Don't pad.** Two PASS verdicts can be a 100-word audit. Two CRITICALs need 800. Match length to the verdicts.
- **Avoid AI tells in the audit itself.** The detector must not write like the thing it detects. Re-read your audit before delivery.
- **Avoid comprehension tells in the audit itself.** Define any acronyms you use. Don't bury the lede. Don't telegraphic-colon-label.

---

## Example: minimal audit (both PASS)

```markdown
# slop-cop Audit

## Verdicts

| Axis | Verdict | Density |
|---|---|---|
| AI-Slop | PASS | 1.5 per 500w |
| Comprehension | PASS | 1.8 per 500w |

**Combined recommendation:** Ship it. Polish-pass at most.

## Stats
Word count: 487 | Audience: casual | Burstiness: 0.81 | Fingerprint: none

## AI-Slop axis
0H, 1M, 3L. One instance of `actually` survives the contrasting-reality rule.

## Comprehension axis
0H, 1M, 2L. Avg sentence 18w, lexical density 47%, passive voice 4%. Reads cleanly.

## Combined recommended action
Ship it.
```

## Example: split verdict (slop fail, comp pass)

```markdown
# slop-cop Audit

## Verdicts

| Axis | Verdict | Density |
|---|---|---|
| AI-Slop | HIGH | 13.2 per 500w |
| Comprehension | LOW | 3.1 per 500w |

**Combined recommendation:** AI-Slop rewrite. The reader-friendliness is fine but the AI texture is loud.

## Stats
Word count: 612 | Audience: marketing | Burstiness: 0.58 | Fingerprint: GPT

## AI-Slop axis
8H, 4M, 6L. `delve` ×3, em-dashes ×7, "I hope this helps", grandiose framing.
Top fixes: replace `delve` (×3), cut em-dash clusters, drop sycophancy closer.

## Comprehension axis
0H, 2M, 5L. Avg sentence 16w, FK grade 8 (good for marketing), 0 undefined acronyms.
Top fixes: convert one telegraphic colon-label to a sentence; add one concrete example.

## Combined top 3 fixes
1. AI-Slop: replace `delve into` (×3) with `look at` or similar
2. AI-Slop: cut 7 em dashes; restructure as sentences with commas/periods
3. AI-Slop: drop "I hope this helps clarify things" closer

## Combined recommended action
Substantial AI-Slop revision. Comprehension is fine.
```

## Example: split verdict (comp fail, slop pass) — the case that drove v2

```markdown
# slop-cop Audit

## Verdicts

| Axis | Verdict | Density |
|---|---|---|
| AI-Slop | LOW | 3.0 per 500w |
| Comprehension | CRITICAL | 28.4 per 500w |

**Combined recommendation:** Comprehension rewrite. Texture is fine; reader has no chance.

## Stats
Word count: 125 | Audience: marketing | Burstiness: 0.72 | Fingerprint: none

## AI-Slop axis
0H, 2M, 0L. Em-dashes ×4 (contested), "X meets Y" ×1.

## Comprehension axis
9H, 3M, 1L. 7 undefined acronyms (SRA, HIRO, ARR, AEO, GEO, B2B, ARR), 14 named entities introduced without context (Refine Labs, Passetto, Sprout, Hootsuite, Taplio, AuthoredUp, Cision Trajaan, Chili Piper, Vandenberghe, Recall.ai, Genesys, Dell, EA, Justin Welsh), 13 numeric claims with no comparative anchors, 4 telegraphic colon-labels (Anchor case:, Tools that win:, What changed in v3:), 2 coined insider terms ("two-stack social management thesis", "1-3-5 atomization method").

## Combined top 3 fixes
1. Comprehension: define acronyms inline (SRA, HIRO, ARR, AEO/GEO) or cut them
2. Comprehension: pick one anchor case; reference others by category not name-drop
3. Comprehension: convert telegraphic colon-labels into actual paragraphs with topic sentences

## Combined recommended action
Comprehension rewrite. The reader can't follow this even though it doesn't read AI.
```
