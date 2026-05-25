# AI Slop Patterns — Rhetorical and Structural

These 45 patterns reliably make prose read as AI-generated. Each is documented in published research, in editorial takedowns, or both. They're rhetorically tidy, they sound polished, and once you see them you can't unsee them. Eliminate them at the editing pass.

This file is the qualitative-pass reference. The mechanical scanner (`scripts/scan.py`) catches what regex can; the rest requires reading the draft against this list.

The patterns are organized into 5 groups by kind of tell:

- **Group A: Rhetorical structures** (12) — sentence-pair and paragraph-shape patterns
- **Group B: Sentence-level tells** (10) — single-sentence constructions
- **Group C: Voice / register tells** (10) — what the prose performs
- **Group D: Decorative content tells** (10) — filler that adds no substance
- **Group E: Density / quantitative** (3) — patterns that show up as count or ratio

## Table of contents

### Group A — Rhetorical structures
1. [Negative parallelism / stylistic negation](#1-negative-parallelism--stylistic-negation)
2. [Dramatic countdown](#2-dramatic-countdown)
3. [Self-posed rhetorical question + immediate answer](#3-self-posed-rhetorical-question--immediate-answer)
4. [Anaphora abuse](#4-anaphora-abuse)
5. [Tricolon abuse](#5-tricolon-abuse)
6. [Symmetrical sentence pairs](#6-symmetrical-sentence-pairs)
7. [Punchy fragment clusters](#7-punchy-fragment-clusters)
8. [Two-word punchline after long setup](#8-two-word-punchline-after-long-setup)
9. [Setup-setup-setup-reveal](#9-setup-setup-setup-reveal)
10. [Crafted closer / mic-drop ending](#10-crafted-closer--mic-drop-ending)
11. [Acknowledgment-loop opening](#11-acknowledgment-loop-opening)
12. [Whether-or falsely inclusive openers](#12-whether-or-falsely-inclusive-openers)

### Group B — Sentence-level tells
13. [Superficial -ing tail](#13-superficial--ing-tail)
14. [False range](#14-false-range)
15. [Copula avoidance](#15-copula-avoidance)
16. [Hedge stacking](#16-hedge-stacking)
17. [Hedged superlatives](#17-hedged-superlatives)
18. [While X, Y sentence opener](#18-while-x-y-sentence-opener)
19. [X meets Y / X is more than just Y](#19-x-meets-y--x-is-more-than-just-y)
20. [Both-sides-ism](#20-both-sides-ism)
21. [False concession](#21-false-concession)
22. [The real tic](#22-the-real-tic)

### Group C — Voice / register tells
23. [Sycophancy / opener flattery](#23-sycophancy--opener-flattery)
24. [Sycophancy / closing flattery](#24-sycophancy--closing-flattery)
25. [Performative opener clichés](#25-performative-opener-clichés)
26. [Let's break this down — pedagogical voice](#26-lets-break-this-down--pedagogical-voice)
27. [Royal-we / as-a-society framing](#27-royal-we--as-a-society-framing)
28. [Servile positivity / uplift tone](#28-servile-positivity--uplift-tone)
29. [Knowledge-cutoff disclaimer leakage](#29-knowledge-cutoff-disclaimer-leakage)
30. [Vague-authority weasel attribution](#30-vague-authority-weasel-attribution)
31. [Stake inflation / future-flourish](#31-stake-inflation--future-flourish)
32. [Grandiose framing](#32-grandiose-framing)

### Group D — Decorative content tells
33. [Magic adverbs](#33-magic-adverbs)
34. [Vapid analogies](#34-vapid-analogies)
35. [Cliché metaphors](#35-cliché-metaphors)
36. [Fabricated case study / generic name](#36-fabricated-case-study--generic-name)
37. [Invented compound concept labels](#37-invented-compound-concept-labels)
38. [Dead-metaphor repetition](#38-dead-metaphor-repetition)
39. [Historical analogy stacking](#39-historical-analogy-stacking)
40. [Synonym cycling / elegant variation](#40-synonym-cycling--elegant-variation)
41. [Throat-clearing meta-comments](#41-throat-clearing-meta-comments)
42. [Compulsive summary / signposted conclusion](#42-compulsive-summary--signposted-conclusion)

### Group E — Density / quantitative
43. [Em-dash overuse](#43-em-dash-overuse)
44. [Buzzword stacking](#44-buzzword-stacking)
45. [Listicle transitions](#45-listicle-transitions)

---

## Group A — Rhetorical structures

### 1. Negative parallelism / stylistic negation

**Pattern:** "It's not X, it's Y." "This isn't X, it's Y." "Not because X, but because Y."

**Examples:**
- "This isn't a job, it's a calling."
- "It's not a tool, it's a thinking partner."
- "Not just marketing — a movement."

**Why it's a tell:** Saturates LinkedIn and blog text post-2023. Cognitive-psych research (Wegner's white-bear effect, plus 2003-2004 negation studies) shows negation backfires — readers retain the negated concept first. RLHF reward models love this construction because it sounds nuanced without committing to a claim. It validates the reader's existing assumption while adding apparent elaboration.

**Fix:** State what it IS. Specify, don't contrast.

**Severity:** H

**Sources:** [The Conversation](https://theconversation.com/slanguage-why-ais-stylistic-negation-its-not-x-its-y-is-both-annoying-and-doesnt-work-278967), [LessWrong](https://www.lesswrong.com/posts/RzPXywNbsRCss3Swy/why-do-llms-so-often-say-it-s-not-an-x-it-s-a-y), [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), [Blake Stockton](https://www.blakestockton.com/dont-write-like-ai-1-101-negation/)

**Audit instruction:** Scan for sentences starting with "It's not", "It wasn't", "This isn't", "Not just", "Not a". Also flag two-sentence pairs where the first asserts a negative and the second pivots. Each is a violation candidate.

---

### 2. Dramatic countdown

**Pattern:** Multi-part negation before a reveal. "Not X. Not Y. Just Z."

**Examples:**
- "Not a bug. Not a feature. A fundamental design flaw."
- "No fluff. No filler. Just signal."
- "Not the first. Not the loudest. The most accurate."

**Why it's a tell:** Variant of pattern 1, escalated. Wikipedia's "Signs of AI writing" guide explicitly flags this construction as a top tell. The fragment-rhythm signals careful crafting, which is itself the giveaway in casual prose.

**Fix:** Lead with the actual point. Cut the buildup.

**Severity:** H

**Sources:** [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), [tropes.fyi](https://tropes.fyi/directory), [agentkit AI tropes](https://github.com/joshuadavidthomas/agentkit/blob/main/skills/ai-writing-tropes/references/sentence-structure.md)

**Audit instruction:** Look for 2-3 short fragmentary sentences in a row, each starting with a negation, followed by an affirmative reveal. Reading required.

---

### 3. Self-posed rhetorical question + immediate answer

**Pattern:** "The result? X." "The catch? Y." "The kicker? Z." "But now? Devastating."

**Examples:**
- "The solution? Simpler than you think."
- "The bottom line? Your customers don't care."
- "The catch? It only works when X."

**Why it's a tell:** Mimics infomercial cadence. AI uses it for false-suspense regardless of stakes. Documented as "Self-Posed Rhetorical Questions" in multiple AI-trope catalogs.

**Fix:** Merge into one statement with concrete evidence. "The solution is simpler than you'd guess: X." Or just give the answer.

**Severity:** H

**Sources:** [tropes.fyi](https://tropes.fyi/directory), [WriteWithAI](https://writewithai.substack.com/p/10-dead-giveaways-your-content-screams), [Hyacinth.ai](https://hyacinth.ai/spot-ai-written-content-phrases/)

**Audit instruction:** Scan for short noun-phrase questions (2-5 words ending in `?`) followed immediately by a short declarative answer. Regex catches the form; reading confirms the cadence.

---

### 4. Anaphora abuse

**Pattern:** Three or more consecutive sentences starting identically. "They assume X. They assume Y. They assume Z."

**Examples:**
- "We need clarity. We need decisiveness. We need execution."
- "The tool helps. The tool scales. The tool ships."
- "I built this for X. I built this for Y. I built this for Z."

**Why it's a tell:** Real writers vary. AI uses anaphora as a default emphasis tool because the structure was rewarded during training on speeches and op-eds. One anaphora across a piece is rhetoric; three in a paragraph is a tic.

**Fix:** Vary openings. Combine related claims with conjunctions or vary clause structure.

**Severity:** M

**Sources:** [agentkit](https://github.com/joshuadavidthomas/agentkit/blob/main/skills/ai-writing-tropes/references/sentence-structure.md), [tropes.fyi](https://tropes.fyi/directory), [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

**Audit instruction:** Read consecutive sentences. Flag any run of 3+ that share the same opening 2-3 words. The scanner catches identical 2-word openings mechanically.

---

### 5. Tricolon abuse

**Pattern:** Triple structures used reflexively, not for emphasis. Three-adjective stacks; three-clause sentences; three-item list patterns.

**Examples:**
- "Innovative, transformative, and groundbreaking."
- "Products impress; platforms empower. Products solve; platforms create. Products deliver; platforms inspire."
- "Fast, focused, and uncompromising."
- "Sharp, specific, and substantive."

**Why it's a tell:** Wikipedia, Beutler Ink, and Pangram all flag this. A single tricolon is elegant; three back-to-back is pattern-recognition failure. Per Colin Gorrie's analysis (Dead Language Society): "the LLM lacks the taste to know when to deploy these techniques."

**Fix:** Use one or two items, or four. Break the rhythm. If three is required, the third element should do *different work* — not another adjective, but a phrase that adds a different kind of information.

**Severity:** H

**Sources:** [Dead Language Society](https://www.deadlanguagesociety.com/p/rhetorical-analysis-ai), [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), [Beutler Ink](https://www.beutlerink.com/blog/how-to-spot-ai-writing)

**Audit instruction:** Scan for any list of three adjectives joined by commas + "and." Apply the sub-rule: if the third element is a different *type* of phrase (not another adjective), it survives. The scanner catches candidates; reading judges.

---

### 6. Symmetrical sentence pairs

**Pattern:** Two adjacent sentences with identical clause structure. "Products solve problems. Platforms create worlds." "X is fast. Y is reliable."

**Examples:**
- "The Mila partnership tells me the science is real. The Sanofi renewal tells me the buyers agree."
- "The studio does six figures. The dev shop signs five."
- "Most companies say it. You did it."

**Why it's a tell:** Burstiness research (GPTZero, Pangram, Quillbot) confirms human writing varies; AI defaults to balanced pairs. Once per piece is fine for emphasis; twice in adjacent sentences is a pattern.

**Fix:** Vary the construction. "X, and Y" or "X, while Y" to break it. Combine into one sentence with two clauses.

**Severity:** M

**Sources:** [GPTZero burstiness](https://gptzero.me/news/perplexity-and-burstiness-what-is-it/), [Pangram](https://www.pangram.com/blog/why-perplexity-and-burstiness-fail-to-detect-ai), [tropes.fyi](https://tropes.fyi/directory)

**Audit instruction:** Read consecutive sentences aloud. If they share the same opening structure (same subject type + same verb pattern), flag. Even if individually fine, the parallel reads engineered.

---

### 7. Punchy fragment clusters

**Pattern:** Three or more short verbless or single-clause fragments in a row.

**Examples:**
- "Fast. Cheap. Reliable."
- "It works. It scales. It ships."
- "It's a system. It's measurable. It's repeatable."

**Why it's a tell:** Burstiness signal — AI either runs uniform-medium or punchy-uniform-short. Both feel mechanical. Documented across agentkit, tropes.fyi, and burstiness research.

**Fix:** Mix one fragment with longer prose. Never stack three. If three short sentences must stay in a row, find one to absorb into a clause with "and" or "which."

**Severity:** H

**Sources:** [agentkit](https://github.com/joshuadavidthomas/agentkit/blob/main/skills/ai-writing-tropes/references/sentence-structure.md), [tropes.fyi](https://tropes.fyi/directory), [GPTZero burstiness](https://gptzero.me/news/perplexity-and-burstiness-what-is-it/)

**Audit instruction:** Count consecutive sentences of ≤8 words. Three or more in a row is a violation. The scanner detects this mechanically.

---

### 8. Two-word punchline after long setup

**Pattern:** Long sentence (20+ words) followed by a short fragment (≤4 words).

**Examples:**
- "...whether the operating model in your job description actually works. **It does.**"
- "...won against 5,800 builders. **It works.**"
- "Most products don't survive the first user. **Most don't.**"
- "...the data is in. **It's bad.**"

**Why it's a tell:** Default LLM rhythm move. The prose equivalent of a drum hit. Once is forgivable; twice in a piece signals AI rhythm.

**Fix:** Fold the punchline into the prior sentence with a comma or "which": "...whether the operating model actually works, which it does." Or replace the setup-and-punchline with one continuous claim.

**Severity:** M

**Sources:** [tropes.fyi](https://tropes.fyi/directory), [agentkit](https://github.com/joshuadavidthomas/agentkit/blob/main/skills/ai-writing-tropes/references/sentence-structure.md)

**Audit instruction:** Look for any sentence ≤4 words immediately following one ≥20 words. Flag each instance. The scanner detects this mechanically.

---

### 9. Setup-setup-setup-reveal

**Pattern:** Buildup paragraphs explicitly announce the conclusion. "The point is..." "What this means is..." "Here's what matters..."

**Examples:**
- "I've worked across product, design, engineering, and marketing. I've shipped at startup speed and at enterprise scale. I've won prizes, signed contracts, built teams. **The point is: I've done what you're hiring for.**"
- "...After all of that, the truth is — we're back where we started."

**Why it's a tell:** AI signposts; humans show. The reader sees the setup and feels manipulated. The reveal becomes obligatory rather than earned.

**Fix:** Trust the reader. Show the substance and let them draw the conclusion. Cut the announcement.

**Severity:** M

**Sources:** [tropes.fyi](https://tropes.fyi/directory), [Hyacinth.ai](https://hyacinth.ai/spot-ai-written-content-phrases/), [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

**Audit instruction:** Look for paragraphs that end with "The point is...", "The thing is...", "What this means is...", "In short...", "Bottom line...", "Here's what matters..." Each is a likely violation. The scanner flags these mechanically.

---

### 10. Crafted closer / mic-drop ending

**Pattern:** Final sentence designed to "land." A one-line punchline that restates the thesis with rhythm. Often a tricolon or negation.

**Examples:**
- "I'd like to build it a fourth time, with you."
- "The category is winnable, and you've earned the right to win it."
- "Build it. Ship it. Run it."
- "Let's go."
- "The future belongs to those who build it."

**Why it's a tell:** AI was trained on op-eds and TED talks; defaults to mic-drop endings even when the topic doesn't warrant. The performative final line signals that the writer is auditioning. It pulls focus from substance and lands on rhetoric.

**Fix:** End on a working sentence that does real work. State what you want, or end on the last actual claim. Resist the urge to land.

**Severity:** M

**Sources:** [tropes.fyi](https://tropes.fyi/directory), [WriteWithAI](https://writewithai.substack.com/p/10-dead-giveaways-your-content-screams)

**Audit instruction:** Read the final sentence in isolation. If it sounds like a Tweet caption or a pull-quote, flag. The voice should close flat and substantive, not sharp.

---

### 11. Acknowledgment-loop opening

**Pattern:** First sentence echoes the title or question. "When it comes to writing better, there are many things to consider." "Understanding how to X requires looking at Y."

**Examples:**
- Title: "How to write better cold emails." First sentence: "When it comes to writing cold emails, there are many factors to consider."
- Title: "Why our pricing changed." First sentence: "There are several reasons why our pricing has changed."

**Why it's a tell:** SEO-blog-trained behavior plus RLHF "show you understood the question" reflex. Immediately deletable. Wikipedia and avoid-ai-writing both flag this as a top opening tell.

**Fix:** Skip to the answer. Open with substance, not orientation.

**Severity:** H

**Sources:** [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing), [Augmented Educator](https://www.theaugmentededucator.com/p/the-ten-telltale-signs-of-ai-generated), [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

**Audit instruction:** Compare the title (or the user's prompt) with the first sentence. If the first sentence paraphrases the title, flag.

---

### 12. Whether-or falsely inclusive openers

**Pattern:** "Whether you're A or B, [main statement]."

**Examples:**
- "Whether you're a beginner or a seasoned pro, this guide will help."
- "Whether you're scaling a startup or running an enterprise, X applies."
- "Whether you're new to X or a longtime user, you'll find Y useful."

**Why it's a tell:** Defensive inclusiveness — avoids choosing an audience. STRYNG's analysis ranks this in the top six AI sentence patterns. Real writing picks a reader.

**Fix:** Pick a reader. Talk to them.

**Severity:** M

**Sources:** [STRYNG](https://stryng.io/common-sentence-structures-in-ai-writing/)

**Audit instruction:** Search for "Whether you're" or "Whether you are" at sentence start. Each instance is a candidate. The scanner catches the form mechanically.

---

## Group B — Sentence-level tells

### 13. Superficial -ing tail

**Pattern:** Main clause + comma + "-ing" phrase that adds vague significance. "X happened, highlighting/emphasizing/symbolizing/contributing to/reflecting Y."

**Examples:**
- "The team launched the feature, demonstrating their commitment to innovation."
- "Sales rose, underscoring the importance of marketing."
- "She submitted her resignation, reflecting growing dissatisfaction in the industry."

**Why it's a tell:** Wikipedia and avoid-ai-writing both flag this as a top sentence-level tell. The "-ing" phrase adds the appearance of analysis without supplying substance. AI uses it as filler that gestures at meaning.

**Fix:** Either give the analysis its own sentence with content, or cut. "Sales rose. The pattern matched what we'd seen each time marketing increased spend by 20%." Specific beats decorative.

**Severity:** H

**Sources:** [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing), [STRYNG](https://stryng.io/common-sentence-structures-in-ai-writing/)

**Audit instruction:** Scan for sentences ending with `, [verb]ing [the/that/how/why/its]`. Most are violations. Regex catches the form.

---

### 14. False range

**Pattern:** "From X to Y..." implying a spectrum where the items are just two loosely-related examples.

**Examples:**
- "From small startups to global enterprises, X applies."
- "From intimate gatherings to global movements, the principle holds."
- "From routine tasks to complex workflows..."

**Why it's a tell:** Wikipedia explicitly catalogs this. STRYNG ranks it in the top six AI sentence patterns. AI uses "from X to Y" as a default scoping phrase even when the two endpoints don't define a real spectrum.

**Fix:** List items directly. Or pick one and be specific about which audience or case you mean.

**Severity:** M

**Sources:** [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), [STRYNG](https://stryng.io/common-sentence-structures-in-ai-writing/), [tropes.fyi](https://tropes.fyi/directory)

**Audit instruction:** Search for "From [noun-phrase] to [noun-phrase]" at sentence start or after a colon. Ask: does X-to-Y describe a real spectrum, or just two examples? If the latter, flag.

---

### 15. Copula avoidance

**Pattern:** Replacing "is" / "are" with marketing verbs: "serves as," "stands as," "marks," "represents," "embodies." Replacing "has" with "boasts," "features," "offers," "maintains."

**Examples:**
- "The gallery serves as a beacon for emerging artists." (vs "The gallery is...")
- "The product boasts a sleek interface." (vs "The product has...")
- "X represents a new era of Y." (vs "X is...")

**Why it's a tell:** Wikipedia documents this as a structural tell; Pangram lists it among 24 core LLM patterns. The scanner can detect the verb signature deterministically. RLHF rewards "elevated" language; "is" reads plain.

**Fix:** Use plain copulas. "Is" is fine. "Has" is fine.

**Severity:** H

**Sources:** [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), [Pangram](https://www.pangram.com/blog/comprehensive-guide-to-spotting-ai-writing-patterns), [GRC Health](https://www.grc-health.com/knowledge-centre/the-predictable-rhetoric-of-ai-generated-text-overused-stylistic-devices), [tropes.fyi](https://tropes.fyi/directory)

**Audit instruction:** Scanner catches "serves as", "stands as", "marks", "represents", "embodies", "boasts", "features", "offers", "maintains" mechanically. Each instance is a candidate.

---

### 16. Hedge stacking

**Pattern:** Multiple hedges in one clause. "It may be possible that adjusting X could potentially improve Y." "Generally speaking, in many cases, it might be that..."

**Examples:**
- "This could potentially help, in many cases."
- "It may generally be possible to improve performance somewhat."
- "Adjustments might possibly yield modest gains."

**Why it's a tell:** RLHF rewards safety; models learn to hedge multiple times to avoid commitment. SciRP's research on hedging devices in AI vs human essays measures this directly. Calibrated hedging (one well-placed "might") is fine. Saturation hedging is the tell.

**Fix:** Cut hedges to zero or one. Commit. "This helps in most cases" beats "This could potentially help in many cases."

**Severity:** H

**Sources:** [SciRP: Hedging Devices in AI vs Human Essays](https://www.scirp.org/journal/paperinformation?paperid=145708), [Hanalarock](https://www.hanalarockwriting.com/post/10-common-chatgpt-isms-what-to-watch-out-for-when-writing-content-with-ai-infographics), [LessWrong](https://www.lesswrong.com/posts/vBDupg8iPqgdwhFzz/demands-are-all-you-need-prompt-imperativeness-drastically)

**Audit instruction:** Scanner counts hedge words within sentence boundaries: may, might, could, possibly, potentially, perhaps, generally, in many cases, somewhat, probably. Three or more in one sentence is a violation.

---

### 17. Hedged superlatives

**Pattern:** "Perhaps the most..." "Arguably the best..." "One of the most..." "Among the most influential..."

**Examples:**
- "Perhaps the most important framework in software design."
- "Arguably the best approach for early-stage startups."
- "One of the most influential thinkers of his generation."

**Why it's a tell:** RLHF makes models avoid bare superlatives. They hedge to seem balanced; reads as evasive. Documented in Grammarly's hedging guide and SciRP's hedging research.

**Fix:** "It's the best." Or rank concretely. "The third-most-cited paper in this subfield" beats "one of the most influential papers."

**Severity:** M

**Sources:** [Grammarly](https://www.grammarly.com/blog/writing-techniques/hedging-language/), [SciRP](https://www.scirp.org/journal/paperinformation?paperid=145708)

**Audit instruction:** Scanner catches the phrase patterns. For each, ask: is the hedge calibrated to genuine uncertainty, or is the writer dodging commitment?

---

### 18. While X, Y sentence opener

**Pattern:** "While historically used in X, the technology now Y." Used as a default contrast device, often opening multiple paragraphs in a row.

**Examples:**
- "While most teams default to X, the smarter approach is Y."
- "While the technology has matured, adoption remains slow."
- "While previous attempts failed, this iteration succeeded."

**Why it's a tell:** Becomes a tic when used >2 times. Documented in Content Beta and Pangram lists. AI defaults to it as a contrast structure when "but" or "however" would do.

**Fix:** Use "X. But Y." or just drop the contrast. If you need the contrast, "X, but Y" is shorter and reads better.

**Severity:** M

**Sources:** [Content Beta](https://www.contentbeta.com/blog/list-of-words-overused-by-ai/), [Pangram](https://www.pangram.com/blog/comprehensive-guide-to-spotting-ai-writing-patterns)

**Audit instruction:** Scanner counts sentences starting with "While [pronoun/noun]". Three or more in a piece flags the pattern.

---

### 19. X meets Y / X is more than just Y

**Pattern:** Compound positioning. "It's where X meets Y." "X is more than just Y, it's Z."

**Examples:**
- "It's where craft meets precision."
- "Marketing is more than just promotion, it's strategy."
- "Where art meets engineering."

**Why it's a tell:** Marketing-speak that AI defaults to. Always feels like a tagline. The construction signals product-launch-deck training.

**Fix:** Describe what it actually is. Specific verbs and nouns beat formula.

**Severity:** M

**Sources:** [Sai Gaddam Medium](https://saigaddam.medium.com/it-isnt-just-x-it-s-y-54cb403d61a8), [Ruben Hassid Substack](https://ruben.substack.com/p/its-not-x-its-y)

**Audit instruction:** Search for "meets" or "more than just" mid-sentence. Each is a candidate.

---

### 20. Both-sides-ism

**Pattern:** Listing pros and cons even when the question doesn't warrant it. "On one hand X, on the other hand Y."

**Examples:**
- "On one hand, the data supports X. On the other hand, some argue Y."
- "There are advantages and disadvantages to consider."
- "Both perspectives have merit."

**Why it's a tell:** RLHF rewards safety; safety = balance even when truth is one-sided. Hanalarock and Olivia Cal both flag this. The result reads as evasion when commitment is warranted.

**Fix:** Take a position. If you're genuinely uncertain, say so once and explain why.

**Severity:** M

**Sources:** [Hanalarock](https://www.hanalarockwriting.com/post/10-common-chatgpt-isms-what-to-watch-out-for-when-writing-content-with-ai-infographics), [Olivia Cal](https://www.oliviacal.com/post/ai-writing-tells)

**Audit instruction:** Look for "on one hand", "on the other hand", "both sides", "advantages and disadvantages". Ask: does the topic genuinely require balance, or is the writer dodging?

---

### 21. False concession

**Pattern:** Acknowledge a problem, then immediately dismiss it without engaging.

**Examples:**
- "While the evidence is limited, the conclusions are clear."
- "Despite its challenges, the future looks bright."
- "Although there are concerns, the benefits outweigh them."

**Why it's a tell:** Documented as the "Despite its challenges" formula. Hollow contrast structure that fakes balance. Wikipedia and tropes.fyi both flag.

**Fix:** State the real tradeoff. If the challenge matters, engage with it. If it doesn't, don't mention it.

**Severity:** M

**Sources:** [tropes.fyi](https://tropes.fyi/directory), [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing), [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

**Audit instruction:** Look for sentences starting with "Despite", "Although", "While [concession]", followed by a dismissive turn. Reading required.

---

### 22. The real tic

**Pattern:** "Real" used as an authenticity intensifier. "Real money," "real stakes," "real research," "real connection."

**Examples:**
- "Run against a real deadline with real money on the line."
- "Real research, not positioning."
- "Real stakes, real outcomes."
- "Real human connection."

**Why it's a tell:** AI uses "real" as a substanceless intensifier. It's signaling authenticity rather than demonstrating it. Confirmed in Embryo and Twixify catalogs.

**Fix:** Be specific. "$100K against 5,800 builders" demonstrates real stakes without using "real". "Real" survives only when contrasting with something specific in the same sentence ("real research rather than positioning").

**Severity:** M

**Sources:** [Embryo](https://embryo.com/blog/list-words-ai-overuses/), [Twixify](https://www.twixify.com/post/most-overused-words-by-chatgpt)

**Audit instruction:** Find every instance of "real". For each, ask: is this contrasting with something specific in this sentence? If yes, it survives. If no, cut it and replace with the specific thing it points at.

---

## Group C — Voice / register tells

### 23. Sycophancy / opener flattery

**Pattern:** "Great question!" "Excellent point!" "I'd be happy to help!" "Absolutely!" "Certainly!" Praise of the user's prompt before answering.

**Examples:**
- "Great question! Let me explain..."
- "What a wonderful idea!"
- "Absolutely, I can help with that."

**Why it's a tell:** Direct RLHF artifact. OpenAI's GPT-4o sycophancy scare (April 2025) confirmed it as reward-model misspecification. Anthropic's own paper documents the same vulnerability in Claude. Less common in formal prose, but bleeds in.

**Fix:** Delete. Always. There is no version of professional prose that opens with "Great question!"

**Severity:** H

**Sources:** [DeGPT](https://www.degpt.app/blog/chatgpt-tells-phrases-list), [Anthropic sycophancy paper](https://arxiv.org/pdf/2310.13548), [Sean Goedecke](https://www.seangoedecke.com/ai-sycophancy/), [The Batch](https://www.deeplearning.ai/the-batch/openai-pulls-gpt-4o-update-after-users-report-sycophantic-behavior/)

**Audit instruction:** Scanner catches "Great question!", "Excellent point!", "Absolutely!", "Certainly!", "Of course!", "I'd be happy to" mechanically. Every instance is a violation.

---

### 24. Sycophancy / closing flattery

**Pattern:** "I hope this helps!" "Let me know if you have any questions!" "Feel free to reach out!" "Don't hesitate to ask!"

**Examples:**
- "I hope this helps clarify things!"
- "Let me know if you'd like me to elaborate."
- "Feel free to reach out with further questions."

**Why it's a tell:** Even more reliable than opener sycophancy because humans rarely close formal prose this way. RLHF artifact. Bleeds through into ghostwritten content because writers forget to strip it.

**Fix:** Cut entirely. End on the last load-bearing sentence.

**Severity:** H

**Sources:** [DeGPT](https://www.degpt.app/blog/chatgpt-tells-phrases-list), [LitHub](https://lithub.com/heres-a-handy-guide-to-help-you-spot-ai-writing/)

**Audit instruction:** Scanner catches all the closing-flattery phrases mechanically. The trailing pattern is so consistent that detection is trivial.

---

### 25. Performative opener clichés

**Pattern:** "Imagine a world where..." "Picture this..." "In a world where..." "Have you ever wondered..." "Are you struggling with..." "In today's fast-paced world..."

**Examples:**
- "Imagine a world where every meeting was productive."
- "In today's fast-paced world, efficiency matters more than ever."
- "Picture this: a tool that handles everything."

**Why it's a tell:** GPTZero's frequency data: "Today's fast-paced world" appears 107x more in AI than in human text. "Imagine a world" is a top-tier giveaway. Performing brevity, performing vision, performing thoughtfulness in the opening is the rhetorical equivalent of clearing your throat.

**Fix:** Open with a specific scene, claim, or fact. Cut the throat-clearing.

**Severity:** H

**Sources:** [GPTZero](https://gptzero.me/news/most-common-ai-vocabulary/), [Hyacinth.ai](https://hyacinth.ai/spot-ai-written-content-phrases/), [Olivia Cal](https://www.oliviacal.com/post/ai-writing-tells)

**Audit instruction:** Scanner catches the full list mechanically: "imagine a world", "picture this", "in a world where", "have you ever wondered", "in today's", "let me cut to it", "i'll be brief".

---

### 26. Let's break this down — pedagogical voice

**Pattern:** "Let's dive into..." "Let's explore..." "Let's break this down..." "We'll walk through..."

**Examples:**
- "Let's dive into the details."
- "Let's break this down step by step."
- "We'll explore the implications."

**Why it's a tell:** Patronizing pedagogical tone. Adopts a teaching persona uninvited. AI was trained on tutorials and explainer videos; defaults to this register when the task is informational.

**Fix:** Just provide the breakdown without announcing it. "The details:" can replace "Let's dive into the details." Or skip the announcement entirely.

**Severity:** M

**Sources:** [tropes.fyi](https://tropes.fyi/directory), [DeGPT](https://www.degpt.app/blog/chatgpt-tells-phrases-list)

**Audit instruction:** Scanner catches "Let's [verb]", "We'll [verb]" at paragraph start. Each is a candidate.

---

### 27. Royal-we / as-a-society framing

**Pattern:** "We live in an age where..." "As a society, we must..." "Our world is..." Performs universal speakership.

**Examples:**
- "We live in an age of unprecedented technological change."
- "As a society, we need to address X."
- "Our collective future depends on Y."

**Why it's a tell:** AI defaults to omniscient-narrator voice; real writers usually have a specific I and you. The royal-we is a marker of the voice not having a specific perspective.

**Fix:** First or second person. Pick a specific reader. "We live in an age" → "Twitter has changed how people argue" — the second is a specific claim with a specific subject.

**Severity:** M

**Sources:** [tropes.fyi](https://tropes.fyi/directory), [Hyacinth.ai](https://hyacinth.ai/spot-ai-written-content-phrases/)

**Audit instruction:** Search for "We live in", "As a society", "Our world", "In our time". Each is a candidate.

---

### 28. Servile positivity / uplift tone

**Pattern:** Constant upbeat framing even when topic is neutral or warrants criticism.

**Examples:**
- "While there are challenges, the future is bright."
- "Despite setbacks, X remains an exciting opportunity."
- "These are amazing developments."

**Why it's a tell:** RLHF positivity bias. LitHub and Wikipedia describe as "tone trying too hard to be uplifting." Real prose allows neutral and critical registers; AI prose smooths everything to mildly enthusiastic.

**Fix:** Allow the topic's actual register. If something is bad, say so. If neutral, write neutrally. The relentless uplift is the tell.

**Severity:** M

**Sources:** [LitHub](https://lithub.com/heres-a-handy-guide-to-help-you-spot-ai-writing/), [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

**Audit instruction:** Read the piece for tonal consistency. If every paragraph ends on an upbeat note regardless of content, flag.

---

### 29. Knowledge-cutoff disclaimer leakage

**Pattern:** "As of my last update..." "I don't have access to real-time data..." "While my training data may be limited..."

**Examples:**
- "As of my knowledge cutoff in early 2024..."
- "I don't have access to real-time data, but..."
- "While my training data may not include the most recent events..."

**Why it's a tell:** Direct LLM artifact. Leaks Claude/GPT system framing into prose. Wikipedia and Originality.ai both catalog this as an instant giveaway.

**Fix:** Cut entirely. If real-time information is needed and unavailable, say so in plain language without the AI-specific framing.

**Severity:** H

**Sources:** [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), [Originality.ai](https://originality.ai/blog/obvious-chatgpt-sayings)

**Audit instruction:** Scanner catches "as of my", "knowledge cutoff", "my training data", "I don't have access to real-time" mechanically. Every instance is a violation.

---

### 30. Vague-authority weasel attribution

**Pattern:** "Studies show..." "Research suggests..." "Many experts agree..." "Industry reports indicate..." with no citation, no name, no link.

**Examples:**
- "Studies show that exercise improves productivity."
- "Many experts believe AI will reshape the economy."
- "Research suggests that this approach works."

**Why it's a tell:** Wikipedia's number-one content-pattern flag. AI defaults to filler when it lacks specifics. The "studies" often don't exist. Real writers cite or admit they don't have a source.

**Fix:** Either cite or cut. "I think" beats "experts say" when you don't have a source. If you have a source, name it.

**Severity:** H

**Sources:** [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), [arXiv slop measurement](https://arxiv.org/html/2509.19163v1), [Influence Intelligence](https://influenceintelligence.substack.com/p/slop-and-signal-the-new-vocabulary)

**Audit instruction:** Scanner catches "studies show", "research suggests", "many experts", "industry reports", "observers have noted", "some critics argue" mechanically. For each, check whether a citation follows. If not, flag.

---

### 31. Stake inflation / future-flourish

**Pattern:** "This will revolutionize..." "We're entering a new era..." "Pave the way..." "Transformative..." "A new paradigm..."

**Examples:**
- "This will revolutionize the way we work."
- "We're entering a new era of productivity."
- "X is paving the way for Y."

**Why it's a tell:** AI treats every topic as world-historical. The "transformative power of" / "has revolutionized" cluster appears in every list. Stakes inflation is the rhetoric equivalent of a "groundbreaking" press release.

**Fix:** Match the size of the claim to the size of the actual change. If something is incremental, say it's incremental.

**Severity:** H

**Sources:** [Hyacinth.ai](https://hyacinth.ai/spot-ai-written-content-phrases/), [aiphrasefinder](https://aiphrasefinder.com/common-chatgpt-phrases/), [Twixify](https://www.twixify.com/post/most-overused-words-by-chatgpt)

**Audit instruction:** Scanner catches "revolutionize", "new era", "paradigm shift", "pave the way", "transformative", "game-changing" mechanically.

---

### 32. Grandiose framing

**Pattern:** Cosmic framing of mundane subjects. "Stands as a testament to..." "Serves as a beacon..." "At its core, X is..." "Embodies the spirit of..."

**Examples:**
- "Stands as a testament to human ingenuity."
- "At its core, this is about freedom."
- "Embodies the spirit of innovation."

**Why it's a tell:** Wikipedia's first content-pattern flag. Appears in every blacklist. AI was trained heavily on award speeches, museum captions, and aspirational marketing — defaults to this framing for any subject.

**Fix:** Use plain claim verbs. "X is Y" beats "X stands as a testament to Y." Specific beats cosmic.

**Severity:** H

**Sources:** [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), [aiphrasefinder](https://aiphrasefinder.com/common-chatgpt-phrases/), [Olivia Cal](https://www.oliviacal.com/post/ai-writing-tells)

**Audit instruction:** Scanner catches "stands as a", "serves as a", "testament to", "embodies", "at its core", "represents a" mechanically.

---

## Group D — Decorative content tells

### 33. Magic adverbs

**Pattern:** Adverbs that don't add meaning. "Quietly", "subtly", "deeply", "fundamentally", "remarkably", "arguably", "genuinely", "actually", "truly", "honestly", "literally."

**Examples:**
- "Quietly orchestrating workflows."
- "Fundamentally changes how we think."
- "Genuinely innovative approach."
- "Honestly, the framework speaks for itself."

**Why it's a tell:** Documented in tropes.fyi as "magic adverbs." Removable without changing meaning equals pure filler. The Hemingway editor flags adverbs as a general writing weakness; AI compounds it by reaching for them as filler.

**Fix:** Delete. If the sentence needs the adverb, the verb is wrong. "Actually" survives only when contrasting concrete reality with theory. The other magic adverbs almost never survive.

**Severity:** H

**Sources:** [tropes.fyi](https://tropes.fyi/directory), [Pangram](https://www.pangram.com/blog/comprehensive-guide-to-spotting-ai-writing-patterns), [Hemingway App](https://hemingwayapp.com/blog/posts/20240624-fix-adverbs-and-toggle-highlights)

**Audit instruction:** Scanner catches each adverb mechanically. For each instance, attempt to delete and re-read the sentence. If unchanged or stronger, the adverb was filler. Cut.

---

### 34. Vapid analogies

**Pattern:** "Think of it as a Swiss Army knife for..." "It's like having a personal assistant in your pocket." Generic, low-resonance comparisons.

**Examples:**
- "Think of it as a Swiss Army knife for productivity."
- "It's like having a personal trainer for your finances."
- "Imagine it as a co-pilot for your inbox."

**Why it's a tell:** AI grabs the most-trained metaphor. Lacks domain specificity. Real writers pull comparisons from their own experience or the reader's specific tribe.

**Fix:** Find a comparison only the reader's tribe would recognize. Or skip — most analogies aren't load-bearing.

**Severity:** M

**Sources:** [tropes.fyi](https://tropes.fyi/directory), [Hastewire](https://hastewire.com/blog/uncover-linguistic-patterns-of-ai-writing-key-tells)

**Audit instruction:** Look for "Think of it as", "It's like", "Imagine it as". Reading required to judge whether the analogy resonates or is generic.

---

### 35. Cliché metaphors

**Pattern:** Tapestry, beacon, treasure trove, symphony, embark on a journey, through the lens of, bridging the gap, navigating the landscape.

**Examples:**
- "A rich tapestry of experiences."
- "A beacon of innovation."
- "Embark on a journey of self-discovery."
- "Through the lens of modern psychology."

**Why it's a tell:** Documented across The Decoder's Reddit-compiled list, aiphrasefinder, and Olivia Cal. AI defaults to the most-trained metaphors. Specific cliché metaphors are catalogued in `vocabulary.md` (category 2B); the *pattern* is reaching for elevated metaphor where plain language would do.

**Fix:** Use plain nouns. "A range of experiences" beats "a rich tapestry of experiences." Cut metaphors that don't add specific clarification.

**Severity:** H

**Sources:** [The Decoder](https://the-decoder.com/reddit-users-compile-list-of-words-and-phrases-that-unmask-chatgpts-writing-style/), [aiphrasefinder](https://aiphrasefinder.com/common-chatgpt-phrases/), [Olivia Cal](https://www.oliviacal.com/post/ai-writing-tells)

**Audit instruction:** Scanner catches the specific words from `vocabulary.md` category 2B. Each instance is a candidate.

---

### 36. Fabricated case study / generic name

**Pattern:** "Take Sarah, a marketing manager from Chicago..." Suspicious common names ("Emily", "Sarah", "John", "Sarah Chen") with rounded-off details.

**Examples:**
- "Take Sarah, a marketing manager from Chicago."
- "Consider John, a startup founder."
- "Meet Emily, a software engineer."

**Why it's a tell:** Pangram explicitly lists "Sarah Chen" / "Emily" as a name signature. AI generates fabricated examples to support claims when it doesn't have real ones. The names cluster around training-data-frequent first names.

**Fix:** Use real, attributable examples or none. If illustrating a point, "a friend who runs a logistics company" beats "Take Sarah."

**Severity:** H

**Sources:** [Pangram](https://www.pangram.com/blog/comprehensive-guide-to-spotting-ai-writing-patterns), [WriteWithAI](https://writewithai.substack.com/p/10-dead-giveaways-your-content-screams)

**Audit instruction:** Search for "Take [Name]", "Meet [Name]", "Consider [Name]" patterns where Name is a single first name. Reading required to judge whether the example is real or fabricated.

---

### 37. Invented compound concept labels

**Pattern:** Made-up bigrams that sound analytical. "The supervision paradox." "The acceleration trap." "The clarity gap."

**Examples:**
- "The supervision paradox of remote work."
- "We call this the clarity gap."
- "Enter the acceleration trap."

**Why it's a tell:** AI generates capital-letter phrases that look like established concepts but Google searches return nothing. The construction signals "I have a framework" without the substance.

**Fix:** If the concept exists, link to it. If not, describe the pattern in plain language. "The thing where managers can't tell what their reports are doing" beats "The supervision paradox."

**Severity:** M

**Sources:** [tropes.fyi](https://tropes.fyi/directory)

**Audit instruction:** Look for capitalized 2-3 word phrases that aren't proper nouns. For each, ask: is this an established concept? Quick search confirms.

---

### 38. Dead-metaphor repetition

**Pattern:** Picks one metaphor (journey, landscape, tapestry, ecosystem) and recycles it five-plus times across a piece.

**Examples:**
- A piece that uses "journey" 7 times.
- A piece that returns to "landscape" in every section.

**Why it's a tell:** Real writers swap or drop metaphors after 2-3 uses. AI digs in because the metaphor was rewarded once and the model keeps reaching for it.

**Fix:** Hold metaphors to one use. Or none.

**Severity:** M

**Sources:** [tropes.fyi](https://tropes.fyi/directory)

**Audit instruction:** Scanner counts cliché-metaphor occurrences across the piece. Three or more uses of the same metaphor noun is a flag.

---

### 39. Historical analogy stacking

**Pattern:** Rapid-fire "this is the new printing press / electricity / internet." Comparing the subject to several big revolutions in successive sentences.

**Examples:**
- "Like the printing press, like electricity, like the internet, AI will transform everything."
- "This is the new industrial revolution. The new agricultural revolution. The new..."

**Why it's a tell:** Documented in tropes.fyi. AI grabs the most-trained authority signals and stacks them, mistaking quantity for resonance.

**Fix:** Pick one comparison and earn it. If the subject doesn't merit the comparison, drop it.

**Severity:** M

**Sources:** [tropes.fyi](https://tropes.fyi/directory)

**Audit instruction:** Look for sequential references to "printing press", "electricity", "internet", "industrial revolution" within a paragraph. Reading required.

---

### 40. Synonym cycling / elegant variation

**Pattern:** Refusing to repeat a noun within paragraphs. "The protagonist...the eponymous character...the key player...the lead figure."

**Examples:**
- "The book...the volume...the work...the publication..."
- "The CEO...the executive...the company head...the chief..."

**Why it's a tell:** Wikipedia confirms this is caused by the repetition-penalty in models. Real writers repeat nouns; pronouns are fine. AI swaps obsessively because training rewards lexical variety.

**Fix:** Repeat the noun. Pronouns ("it", "she", "the company") are fine.

**Severity:** M

**Sources:** [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

**Audit instruction:** Scanner heuristic: flag if a noun has 4+ synonym swaps in a 200-word window. Reading confirms whether the variation is forced.

---

### 41. Throat-clearing meta-comments

**Pattern:** "It's worth noting that..." "It's important to mention..." "It bears mentioning..." "Notably..." "Interestingly..."

**Examples:**
- "It's worth noting that this approach has limitations."
- "Notably, the data shows X."
- "It's important to mention that..."

**Why it's a tell:** GoWinston and Pangram both flag the cluster. Filler that announces importance instead of demonstrating it. The phrase adds zero information; the sentence following it carries the actual claim.

**Fix:** Just say the thing. Cut the announcement. "This approach has limitations: X" beats "It's worth noting that this approach has limitations. X."

**Severity:** H

**Sources:** [GoWinston](https://gowinston.ai/most-common-chatgpt-words/), [Pangram](https://www.pangram.com/blog/comprehensive-guide-to-spotting-ai-writing-patterns), [DeGPT](https://www.degpt.app/blog/chatgpt-tells-phrases-list)

**Audit instruction:** Scanner catches "it's worth noting", "it's important to", "it bears mentioning", "notably", "interestingly" at sentence start mechanically.

---

### 42. Compulsive summary / signposted conclusion

**Pattern:** "In conclusion..." "To summarize..." "Overall..." "Ultimately..." "All things considered..." "In essence..." "To put it simply..." "At the end of the day..."

**Examples:**
- "In conclusion, X matters because Y."
- "Overall, the takeaway is Z."
- "Ultimately, this comes down to commitment."

**Why it's a tell:** Beutler Ink calls it the "compulsive summary." AI restates even short pieces. SFU Library's writing guide notes the compulsive-conclusion habit predates AI but compounds in AI prose. Reading past sentence one of the conclusion is rarely worth it because it's just compression of the body.

**Fix:** Cut. End on a substantive sentence.

**Severity:** H

**Sources:** [Beutler Ink](https://www.beutlerink.com/blog/how-to-spot-ai-writing), [SFU Library](https://www.lib.sfu.ca/about/branches-depts/slc/writing/organization/conclusions), [DeGPT](https://www.degpt.app/blog/chatgpt-tells-phrases-list)

**Audit instruction:** Scanner catches the full phrase list mechanically at paragraph or section start. Each instance is a candidate.

---

## Group E — Density / quantitative

### 43. Em-dash overuse

**Pattern:** Multiple em dashes per page, used where commas, periods, or parentheticals would do.

**Examples:**
- "I joined as employee #2 — and helped scale us to 80."
- "The studio — six figures in pipeline within months — proves the model."
- "We shipped a hundred deployments — and the platform that ended up administering a quarter of Canada's COVID doses."

**Why it's a tell:** Most-cited AI tell of 2024-2025. Rolling Stone, TechRadar, NYT all covered. OpenAI added an em-dash opt-out in GPT-5.1 (Nov 2025). Caveat: contested — many human writers (Cory Doctorow, Cormac McCarthy estate) use them constantly. The era of em-dash-as-sole-tell is largely over per OpenAI's fix.

**Fix:** Default to commas, periods, or parentheticals. Allow yourself ~1-2 em dashes per long piece. For users with explicit no-em-dash voice rules (Mahmoud), cut all instances.

**Severity:** H in clusters (3+ per 500 words); M alone

**Sources:** [Rolling Stone](https://www.rollingstone.com/culture/culture-features/chatgpt-hypen-em-dash-ai-writing-1235314945/), [TechRadar](https://www.techradar.com/ai-platforms-assistants/chatgpt/the-days-of-the-em-dash-being-a-chatgpt-giveaway-are-over-its-time-to-bring-it-back), [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

**Audit instruction:** Scanner counts em dashes (—, U+2014), en dashes (–, U+2013), and double-hyphens (--) mechanically. Cluster threshold: 3+ per 500 words = H severity. Single instances: M (or L in non-strict mode).

---

### 44. Buzzword stacking

**Pattern:** Three or more buzzwords stacked in one paragraph or sentence.

**Examples:**
- "Robust, scalable, cutting-edge solutions."
- "Innovative, transformative, revolutionary platforms."
- "AI-native, agent-driven, autonomous workflows."

**Why it's a tell:** Density triggers all detectors. Three buzzwords in a row almost guarantees AI. Confirmed by Olivia Cal, Embryo, and the Pangram catalog.

**Fix:** Pick one. Make it specific. "The platform that administered roughly a quarter of Canada's daily COVID vaccine doses at peak" carries far more weight than "scalable, mission-critical healthcare infrastructure."

**Severity:** H

**Sources:** [Olivia Cal](https://www.oliviacal.com/post/ai-writing-tells), [Embryo](https://embryo.com/blog/list-words-ai-overuses/), [Pangram](https://www.pangram.com/blog/comprehensive-guide-to-spotting-ai-writing-patterns)

**Audit instruction:** Scanner counts buzzwords from `vocabulary.md` category 2C in each paragraph. Three or more is a flag.

---

### 45. Listicle transitions

**Pattern:** "First and foremost..." "Last but not least..." "On the other hand..." "Furthermore..." "Moreover..." "Additionally..."

**Examples:**
- "Furthermore, this approach scales."
- "Moreover, the data confirms it."
- "First and foremost, clarity matters."

**Why it's a tell:** "Furthermore"/"Moreover"/"Additionally" cluster is the most cited AI signal across nearly every source. Wikipedia, GoWinston, Hyacinth, Hastewire all flag. Real prose uses periods or "Also." Most transitions are deletable.

**Fix:** Use periods or "Also." Most transitions don't load-bear and can be cut.

**Severity:** H

**Sources:** [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), [GoWinston](https://gowinston.ai/most-common-chatgpt-words/), [Hyacinth.ai](https://hyacinth.ai/spot-ai-written-content-phrases/), [Hastewire](https://hastewire.com/blog/uncover-linguistic-patterns-of-ai-writing-key-tells)

**Audit instruction:** Scanner catches "Furthermore", "Moreover", "Additionally", "First and foremost", "Last but not least", "On the other hand" at sentence start mechanically. Each is a candidate.

---

## How to use this file

**During audit:** Walk through groups A through E in order. For each pattern, scan the draft for instances. Flag with quote + severity. After all 45 passes, you have a complete violation list. The scanner catches the mechanically-detectable patterns; reading is required for the qualitative ones (anaphora, symmetry, the actual force of metaphors, etc.).

**During compose:** Read the list before drafting to prime awareness. Read it again before delivery as a final-pass check. Most patterns survive only the second pass — first-draft prose contains them and the editing pass removes them.

**Severity guidelines:**
- **High severity (H):** always cut. These actively make the writing read as AI. Em dashes in clusters, sycophancy, grandiose framing, copula avoidance, knowledge-cutoff leakage, compulsive summary, vague-authority weasels, listicle transitions, performative openers, hedge stacking, magic adverbs, throat-clearing, fabricated case studies, cliché metaphors, present-participle "-ing" tails, tricolon abuse, anaphora abuse, negation reversals, dramatic countdown, self-posed Q+A, stake inflation, acknowledgment-loop opening, punchy fragment clusters, buzzword stacking.
- **Medium severity (M):** cut unless context-justified. Symmetrical sentence pairs, two-word punchlines, setup-reveal, crafted closers, "While X, Y" opener, hedged superlatives, false range, "X meets Y", whether-or openers, both-sides-ism, false concession, "real" tic, pedagogical voice, royal-we, servile uplift, vapid analogies, invented compound concepts, dead-metaphor repetition, historical analogy stacking, synonym cycling.
- **Low severity (L):** noted in audit but doesn't down-score. Em dashes alone (1–2 in a long piece), individual decorative adverbs in narrow context.

If a draft has 5+ H-severity violations within 500 words, recommend a rewrite rather than spot-fixes. See `calibration.md` for density-scoring details.

## What this list is not

This list is descriptive of LLM tells, not prescriptive of all good writing. Plenty of human writers use em dashes, three-beat lists, and short punchy sentences and write beautifully. The point is that *AI prose specifically* uses these patterns at much higher density than human prose, and that any draft meant to read as a human's writing will register as AI-generated if the patterns appear in clusters.

The catalog is current through early 2026. Models change; tells change. After "delve" went viral in early 2024, arXiv frequency dropped sharply. Newer/less-famous patterns (copula avoidance, "-ing" tails, anaphora abuse, false ranges) are now more reliable than the original vocabulary list. See `calibration.md` for sanded-prose detection.
