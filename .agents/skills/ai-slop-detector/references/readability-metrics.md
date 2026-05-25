# Readability Metrics

Quantitative formulas the comprehension axis computes alongside the pattern catalog. These are well-validated, decades-old measurements with known limitations. The scanner reports them as a panel; calibration thresholds are in `calibration.md`.

The metrics measure mechanical proxies for difficulty (sentence length, syllable count, word familiarity), not actual comprehension. They're useful as a panel — no single metric is decisive — and they ground the verdict in something more than regex hits.

## The 8 metrics the scanner computes

The scanner computes these eight (chosen for breadth of coverage and lack of redundancy):

1. **Flesch Reading Ease** — overall ease of reading (0–100 scale, higher = easier)
2. **Flesch-Kincaid Grade Level** — U.S. school grade required to understand
3. **SMOG Index** — grade level for full comprehension (gold standard for healthcare)
4. **Coleman-Liau Index** — grade level via character counts (no syllable estimation)
5. **Dale-Chall Score** — grade level via word familiarity against a 3,000-word list
6. **Lexical Density** — content words ÷ total words
7. **Average Sentence Length** + variance
8. **Passive Voice Percentage**

Plus the comprehension-specific density signals (acronym density, named-entity density, numeric density) defined in `comprehension.md`.

---

## 1. Flesch Reading Ease (FRE)

```
206.835 − 1.015 × (words / sentences) − 84.6 × (syllables / words)
```

**Scale:** 0–100. Higher = easier.

| Score | Grade equivalent | Description |
|---|---|---|
| 90–100 | 5th grade | Very easy |
| 80–89 | 6th grade | Easy |
| 70–79 | 7th grade | Fairly easy |
| 60–69 | 8th–9th grade | Plain English |
| 50–59 | 10th–12th | Fairly difficult |
| 30–49 | College | Difficult |
| 0–29 | College graduate | Very difficult |

**Targets** (per audience, see `calibration.md`):
- General blog: 60–70
- Marketing copy: 65–80
- Technical docs: 40–50
- Healthcare patient material: 70–80
- Academic: 30–50

**Limitations:** Ignores reader prior knowledge, syntax complexity, jargon density, organization, and layout. Random character strings can produce absurd scores. Use as one signal among several.

**Source:** [Wikipedia: Flesch–Kincaid](https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests), [Readable on FRE](https://readable.com/readability/flesch-reading-ease-flesch-kincaid-grade-level/)

---

## 2. Flesch-Kincaid Grade Level (FKGL)

```
0.39 × (words / sentences) + 11.8 × (syllables / words) − 15.59
```

**What it measures:** U.S. school grade level required to understand the text.

**Targets:**
- General audience: 7–9
- Marketing: 7–8
- Technical docs: 10–12
- Hemingway editor's default: grade 9
- GOV.UK: age 9 (~grade 4)
- Average U.S. adult reads at: ~grade 8

**Limitations:** Two metrics only (sentence and word length). Doesn't measure comprehension, only mechanical proxies. Built on 1970s Navy training material; may not generalize to modern topics.

**Source:** [Hemingway on FK](https://hemingwayapp.com/articles/readability/flesch-kincaid-readability-test), [AHRQ on readability formula limitations](https://www.ahrq.gov/talkingquality/resources/writing/tip6.html)

---

## 3. SMOG Index (Simple Measure of Gobbledygook)

```
1.0430 × √(polysyllables × 30 / sentences) + 3.1291
```

Where *polysyllables* = words of 3+ syllables.

**What it measures:** Years of education needed for *full* comprehension (vs. 50–75% for Flesch-Kincaid). The healthcare gold standard.

**Targets:**
- Patient-facing healthcare materials: grade 6–8
- General public: 7–9
- Best for shorter texts (≥30 sentences); may be unreliable on very short samples

**Limitations:** Designed for full comprehension, so scores skew higher than FK. Overestimates difficulty for short pieces.

**Source:** [Readability Formulas: how to choose](https://readabilityformulas.com/how-to-decide-which-readability-formula-to-use/), [Gorby readability guide](https://gorby.app/readability/readability-formulas-guide/)

---

## 4. Coleman-Liau Index (CLI)

```
0.0588 × L − 0.296 × S − 15.8
```

Where:
- L = average letters per 100 words
- S = average sentences per 100 words

**What it measures:** Grade level using character counts instead of syllables.

**Targets:** Grade 8–10 for general; 12+ for academic.

**Strength:** Avoids syllable-counting ambiguity, which makes it reliable for technical text with acronyms and abbreviations (where syllable counting often errors).

**Limitations:** Doesn't capture vocabulary difficulty within similar character counts. *"Bake"* and *"work"* score the same as *"axes"* and *"bond"*.

**Source:** [Gorby readability guide](https://gorby.app/readability/readability-formulas-guide/)

---

## 5. Dale-Chall Readability Score

```
raw_score = 0.1579 × (% difficult words) + 0.0496 × (words / sentences)
if % difficult words > 5:
    raw_score += 3.6365
```

Where *difficult* = not in the Dale-Chall list of 3,000 words that 80% of 4th-graders know.

| Score | Grade |
|---|---|
| < 5.0 | 4th grade or below |
| 5.0–5.9 | 5th–6th |
| 6.0–6.9 | 7th–8th |
| 7.0–7.9 | 9th–10th |
| 8.0–8.9 | 11th–12th |
| 9.0–9.9 | College |
| 10.0+ | College graduate |

**Strength:** The only major formula that catches simple-syntax-but-obscure-vocabulary problems. Direct check of word familiarity, not length proxy. *"The man eschewed the indolent quotidian routine"* scores high here even though every word is short.

**Limitations:** Word list last updated 1995; missing modern vocabulary (it doesn't know *email*, *online*, *startup*, etc.). The scanner uses a curated subset since the full 3,000-word list is large.

**Source:** [Wikipedia: Dale–Chall](https://en.wikipedia.org/wiki/Dale%E2%80%93Chall_readability_formula), [Dale-Chall word list](https://readabilityformulas.com/word-lists/the-dale-chall-word-list-for-readability-formulas/)

---

## 6. Lexical Density

```
(content_words / total_words) × 100
```

Where *content words* = nouns, main verbs, adjectives, adverbs (everything except function words: articles, prepositions, conjunctions, pronouns, auxiliaries).

**Thresholds:**
| Density | Type |
|---|---|
| 30–40% | Spoken English |
| 40–50% | Written prose, news |
| 50–55% | Magazine features |
| 55–65% | Academic, legal, technical |
| 65%+ | Information-dense, hard to scan |

**What it measures:** How "packed" with content words a text is. High density = hard to skim; reader has to absorb every word.

**Limitations:** Only measures vocabulary, not syntactic complexity or organization. Density alone doesn't equal difficulty if structure is clear. The scanner uses POS-tag heuristics (no full parser) so the number is approximate.

**Source:** [Wikipedia: lexical density](https://en.wikipedia.org/wiki/Lexical_density), [TextInspector on lexical density](https://textinspector.com/lexical-density-vs-lexical-diversity/)

---

## 7. Average Sentence Length + Variance

```
mean = total_words / total_sentences
stddev = sqrt(Σ(sentence_length − mean)² / n)
variance_ratio = stddev / mean   # also called burstiness
```

**Comprehension thresholds:**
| Avg length | Comprehension |
|---|---|
| ≤ 8 words | ~100% |
| 14 words | > 90% |
| 25 words | noticeable drop |
| 43+ words | < 10% |

**Targets:**
- General prose: 15–18 words average
- Marketing copy: 12–16
- GOV.UK / civic: 12–15
- Technical docs: 18–22
- Academic: 20–28

**Variance:** humans cluster 0.6–1.2 (variance / mean ratio). LLMs cluster 0.2–0.4 (uniform sentences).

**Mechanism:** Working memory holds the sentence in a buffer. Long sentences overflow it; the reader loses the thread. This metric also feeds the AI-slop axis (low burstiness = AI tell).

**Source:** [Letter Counter on sentence length](https://lettercounter.org/blog/sentence-length-readability/), [Siteimprove on long sentences](https://help.siteimprove.com/support/solutions/articles/80000447968-readability-why-are-long-sentences-over-20-words-)

---

## 8. Passive Voice Percentage

```
passive_count / total_sentences × 100
```

Detected via regex: *be-verb (is/was/were/been/being/are/am) + past participle (-ed or irregular)*.

**Thresholds:**
| Tool | Threshold |
|---|---|
| Yoast | < 10% (cap) |
| Readable | < 3% (recommendation) |
| Monash | < 5% |
| Common consensus | 4–10% for general prose |

**What it measures:** Sentences where the subject receives the action rather than performs it.

**Why it matters:** Passive constructions hide the agent, lengthen sentences, and reverse subject-verb-object expectation. *"Mistakes were made"* obscures who made them.

**Limitations:** Some passive is fine and necessary (when the agent is unknown, irrelevant, or being de-emphasized for tact). The regex catches many but not all forms; some active sentences match the pattern (*"The book was finished by Tuesday"* — finished here is past tense, not participle).

**Source:** [Yoast on passive voice](https://yoast.com/the-passive-voice-what-is-it-and-how-to-avoid-it/), [Readable on active voice](https://readable.com/blog/are-you-using-the-active-voice-in-your-content/)

---

## Cold-reader-specific density signals

These three are not classic readability formulas. They're new measurements that target the failure modes in `comprehension.md` patterns F1, F2, F3.

### Acronym density per 100 words

```
undefined_acronyms / words × 100
```

**Definition:** *Undefined* = uppercase token of 2–5 letters not in the known-acronyms allowlist (USB, FAQ, URL, API, JSON, HTML, CSS, SQL, AWS, CEO, CFO, CTO, etc.) and not introduced earlier in the document with a parenthetical expansion.

**Threshold:** 3+ undefined acronyms per 100 words = high cognitive load.

### Named-entity density per 100 words

```
proper_noun_runs / words × 100
```

**Definition:** Proper noun runs = capitalized non-sentence-start tokens (excluding common-noun-uses-of-capitalization like in titles).

**Threshold:** 5+ named-entity introductions without context per 100 words = "named-entity bombing."

### Numeric density per sentence

```
max(numeric_claims_per_sentence)
```

**Threshold:** Any sentence with 3+ numeric claims (with units like %, $, K, M, year) is a stat-bombing flag.

---

## How the metrics feed the verdict

The verdict is computed from the pattern catalog (`comprehension.md`) — not from the readability formulas directly. The metrics serve three purposes:

1. **Diagnosis.** When the verdict is HIGH/CRITICAL on comprehension, the metrics tell the reader *why*. "FK Grade 16, average sentence 32 words, lexical density 68%" is a different failure mode than "FK Grade 4 but acronym density 8 per 100 words."

2. **Audience calibration.** The same Flesch score has different meanings for different audiences. `calibration.md` maps the metrics to audience targets.

3. **Compound triggers.** A draft can pass the pattern catalog (no individual H violations) and still fail the metrics panel (FK Grade 16, lexical density 70%, no concrete examples). The metrics catch the cumulative texture of dense academic prose that any single pattern would miss.

The audit report includes the metrics panel under the verdict line. See `audit-report-template.md` for the format.

---

## Why these eight, not all twenty researched

There are 20+ readability formulas in the literature (Gunning Fog, ARI, FORCAST, Linsear Write, etc.). The scanner ships with the 8 above because:

- **Three Flesch-family** (FRE, FKGL) covers the most-cited and most-validated baseline
- **SMOG** is the healthcare gold standard
- **Coleman-Liau** is character-based, robust against acronyms
- **Dale-Chall** uniquely captures vocabulary familiarity
- **Lexical density, sentence length variance, passive voice** are independent signals that the others don't catch

Other formulas are largely correlated with FK and don't add diagnostic information. They're documented in `sources.md` for reference but not computed by the scanner.

## Limitations of metrics overall

Janice Redish's classic critique applies: readability formulas measure mechanical proxies (length) for properties they don't actually measure (comprehension). A short-sentence document can be incoherent. A long-sentence document can be lucid. The scanner reports the metrics because they correlate with comprehension on average, but the patterns in `comprehension.md` are the load-bearing checks. The metrics calibrate; the patterns rule.

**Source:** [Redish on readability formulas](https://redish.net/wp-content/uploads/Redish_on_Readability_Formulas.pdf)
