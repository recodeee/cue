# Comprehension Patterns

These patterns hurt the reader, not the texture. A piece can pass the AI-slop axis (no `delve`, no em-dash clusters, no sycophancy) and still be unreadable: jargon-bombed, structure-less, telegraphic, or written for an audience that already knows everything.

This file is the **comprehension axis** of slop-cop. Where the AI-slop axis asks *"did a machine write this?"*, the comprehension axis asks *"can a fresh reader follow this?"* Both axes can fail independently. The output is two parallel verdicts, not one merged score.

Most patterns here are catalogued from cognitive-load research (Miller, Sweller, Cowan), plain-language style guides (plainlanguage.gov, GOV.UK, Microsoft, Google developer style), the curse-of-knowledge literature (Pinker), web-readability eyetracking (NN/g), and the Plain Writing Act / WCAG accessibility standards. See `sources.md` for the full bibliography.

The 35 patterns are organized into 5 groups by failure mode:

- **Group F: Density overload** (5) — too much per unit of text
- **Group G: Telegraphic compression** (5) — author crammed instead of explained
- **Group H: Audience-assumption failures** (5) — writer assumes shared context the reader lacks
- **Group I: Structure / scannability** (12) — reader can't navigate or preview
- **Group J: Sentence-level cognitive friction** (8) — the prose itself is hard to parse

## Severity tiers

- **H (high)** — comprehension blocker; reader can't extract meaning. Always cut.
- **M (medium)** — comprehension friction; readers slow down or re-read. Cut unless context-justified.
- **L (low)** — informational; a tell among others, doesn't kill the verdict alone.

---

## Group F — Density overload

### F1. Undefined acronym stacking

**Pattern:** Multiple acronyms used as if known, no inline definition, no glossary link.

**Examples:**
- "12-month SRA implementation: $50M HIRO pipeline, $14M closed-won ARR."
- "Use the API to POST to the SDK endpoint."
- "AEO/GEO Brand Report"

**Mechanism:** Each undefined acronym costs a working-memory slot to "park as unknown." Three undefined acronyms in 100 words exceeds Cowan's 4-chunk limit. Reader either guesses or quits.

**Fix:** Define on first mention: "search request agent (SRA)". If 3+ acronyms in 100 words, restructure to spell out the most consequential ones.

**Severity:** H. **Detection:** mechanical — count uppercase 2–5 letter tokens not in a "known acronym" allowlist (USB, FAQ, URL, API for dev contexts, etc.).

**Sources:** [Microsoft style: acronyms](https://learn.microsoft.com/en-us/style-guide/acronyms), [Google developer style: abbreviations](https://developers.google.com/style/abbreviations), [Chicago Manual of Style](https://www.chicagomanualofstyle.org/qanda/data/faq/topics/Abbreviations.html), [Miller's 7±2](https://lawsofux.com/millers-law/)

---

### F2. Named-entity bombing

**Pattern:** Five or more proper nouns (companies, people, products) introduced without context per 100 words.

**Examples:**
- "Sprout/Hootsuite for company page + Taplio/AuthoredUp for individual exec profiles; Cision Trajaan AEO/GEO Brand Report."
- "Refine Labs / Passetto — 12-month SRA implementation."

**Mechanism:** Cold reader has no schema for unknown brand names. Each unfamiliar entity competes for working-memory buffer. Reader drowns.

**Fix:** Pick one anchor example, contextualize it, reference others by category: *"two LinkedIn-focused tools, like Taplio."*

**Severity:** H. **Detection:** mechanical — capitalized-token density (excluding sentence starts), or NER if available.

**Sources:** [NN/g on technical jargon](https://www.nngroup.com/articles/technical-jargon/), [Miller's 7±2](https://en.wikipedia.org/wiki/The_Magical_Number_Seven,_Plus_or_Minus_Two)

---

### F3. Stat bombing without comparative anchor

**Pattern:** Three or more numeric claims in a sentence (or six in a paragraph) without baseline, comparison, or source.

**Examples:**
- "$50M pipeline, $14M ARR, 93% gap, 50% pipeline lift, 40K audience, $680K spend."
- "83% of B2B buying time happens in dark social."

**Mechanism:** Numbers without baseline don't register. A reader can't tell if $50M is impressive without context.

**Fix:** For each stat: add (a) baseline (*"vs. industry average of X"*), (b) source (*"per Gartner"*), or (c) interpretation (*"3× the previous quarter"*).

**Severity:** H. **Detection:** mechanical — count numerals + units per sentence/paragraph, flag when ratio of numerals to comparative phrases is high.

**Sources:** [CDC Clear Communication Index — Numbers section](https://www.cdc.gov/ccindex/tool/index.html), [AHRQ on writing about numbers](https://www.ahrq.gov/talkingquality/resources/writing/tip6.html)

---

### F4. Wall-of-text / paragraph density

**Pattern:** Paragraphs over 5–6 sentences for web; lack of white space; visually intimidating.

**Mechanism:** Eye fatigue plus lack of natural break points. 79% of web readers scan; long paragraphs defeat scanning.

**Fix:** Break at every clear topic shift. Cap web paragraphs at 3 sentences / 100 words.

**Severity:** M. **Detection:** mechanical — sentences per paragraph; flag if any paragraph >5 sentences or >100 words.

**Sources:** [NN/g: Applying writing guidelines to web pages](https://www.nngroup.com/articles/applying-writing-guidelines-web-pages/), [Vayce: ideal paragraph length for web](https://vayce.app/blog/ideal-paragraph-length-for-web-writing/)

---

### F5. Density-without-headings trap

**Pattern:** 500+ words of dense prose with no subheadings, no bolded keywords, no callouts.

**Mechanism:** F-pattern readers rely on subheadings to navigate. Without them, scanners bail. Three levels of headings is ideal for medium-long articles.

**Fix:** Insert H2 or H3 every 200–300 words. Add bold for key phrases (sparingly).

**Severity:** H (web). **Detection:** mechanical — count headings vs word count.

**Sources:** [NN/g: Applying writing guidelines](https://www.nngroup.com/articles/applying-writing-guidelines-web-pages/), [W3C: heading hierarchy](https://www.w3.org/WAI/tutorials/page-structure/headings/)

---

## Group G — Telegraphic compression

### G1. Telegraphic colon-labeling

**Pattern:** A paragraph compressed by colon labels rather than sentences. *"Anchor case: X. Tools that win: Y. What changed: Z."*

**Examples:**
- "Anchor case: Refine Labs / Passetto. Tools that win: dual stack. What changed in v3: added 6 named cases."

**Mechanism:** Forces 3+ topic shifts in one paragraph; no semantic glue between them. Labels read as headings without the visual hierarchy that headings provide.

**Fix:** Either convert each colon-label to its own paragraph with a topic sentence, or convert the block to a true list with sub-headings.

**Severity:** H. **Detection:** mechanical — count `: ` (colon-space-Capital) mid-paragraph; flag at 3+ per paragraph.

**Sources:** [ERIC on telegraphic prose](https://eric.ed.gov/?id=ED062090), [NN/g: be succinct](https://www.nngroup.com/articles/be-succinct-writing-for-the-web/)

---

### G2. List-pretending-to-be-prose

**Pattern:** A paragraph that's actually a list of parallel items joined by commas, semicolons, or `+` signs — would be cleaner as a bulleted list.

**Examples:**
- "Tools that win: dual stack — Sprout/Hootsuite for company page + Taplio/AuthoredUp for individual exec profiles; Cision Trajaan AEO/GEO Brand Report."

**Mechanism:** Parallel discrete items don't need narrative. Prose creates artificial transitions and obscures structure.

**Fix:** Convert to bulleted list.

**Severity:** M. **Detection:** mechanical — paragraphs with 2+ semicolons or 3+ `+` separators creating sub-lists.

**Sources:** [Writing Skills: bullets won't make case](https://www.writing-skills.com/bullets-wont-make-case)

---

### G3. Long sentences past comprehension cliff

**Pattern:** Sentences over 25 words. At 43 words, comprehension drops below 10%.

**Mechanism:** Working memory holds ~4–7 chunks. A 30+ word sentence overflows the buffer before the reader reaches the verb or main clause.

**Fix:** Break at conjunctions (*and*, *but*, *which*) into two sentences. Cap at 20–25 words.

**Severity:** H. **Detection:** mechanical — word count per sentence; flag any over 30.

**Sources:** [Letter Counter on sentence length](https://lettercounter.org/blog/sentence-length-readability/), [Siteimprove: long sentences over 20 words](https://help.siteimprove.com/support/solutions/articles/80000447968-readability-why-are-long-sentences-over-20-words-)

---

### G4. Paragraph-length sentence (run-on continuation)

**Pattern:** Sentence joining 4+ independent clauses with conjunctions and dashes; often comma-spliced.

**Mechanism:** Working memory exhausted before reader reaches the end. Different from "long sentence" — these are structurally compound, not lexically dense.

**Fix:** Break at every *and / but / —* that introduces a new clause.

**Severity:** H. **Detection:** mechanical — clause counter (commas + conjunctions per sentence).

**Sources:** [Letter Counter](https://lettercounter.org/blog/sentence-length-readability/)

---

### G5. Glue-word bloat

**Pattern:** *There is*, *it is*, *what is happening is* — placeholders that delay the actual subject.

**Examples:**
- "There are many factors that influence the outcome." → "Many factors influence the outcome."
- "It is important that you remember to..." → "Remember to..."

**Mechanism:** Empty leading phrases steal attention without delivering meaning.

**Fix:** Cut *there is/are*, *it is*, start with the real subject.

**Severity:** L. **Detection:** mechanical — regex on sentence starts.

**Sources:** [Microsoft style: top 10 tips](https://learn.microsoft.com/en-us/style-guide/top-10-tips-style-voice)

---

## Group H — Audience-assumption failures

### H1. Coined insider terms used as known

**Pattern:** Author-invented or niche terminology deployed without definition.

**Examples:**
- "two-stack social management thesis"
- "1-3-5 atomization method"
- "founder LinkedIn rhythm playbook"
- "dark social"

**Mechanism:** Pinker's curse of knowledge — writer assumes reader shares jargon the writer just minted.

**Fix:** First mention spelled out: *"the two-stack approach (one tool for the company page, one for individual executives)."* Or strip the coined term and describe in plain language.

**Severity:** H. **Detection:** partial — flag multi-word noun phrases used without an article (*"the"*, *"a"*) where the phrase wasn't introduced earlier; reading required to confirm.

**Sources:** [Pinker on curse of knowledge — Harvard](https://news.harvard.edu/gazette/story/2012/11/exorcising-the-curse-of-knowledge/), [APS on Pinker](https://www.psychologicalscience.org/observer/the-curse-of-knowledge-pinker-describes-a-key-cause-of-bad-writing)

---

### H2. Curse of knowledge

**Pattern:** Writer assumes shared jargon, intermediate steps, or mental images. Doesn't bother to define terms or spell out logic.

**Mechanism:** Pinker: *"the failure to understand that other people don't know what we know."* The single biggest cause of opaque writing.

**Fix:** Show the draft to someone outside the field. Mark every spot they ask "what's that?" Spell those out.

**Severity:** H. **Detection:** qualitative — requires knowing the target audience.

**Sources:** [Pinker — Harvard](https://news.harvard.edu/gazette/story/2012/11/exorcising-the-curse-of-knowledge/), [Poynter applied](https://www.poynter.org/reporting-editing/2021/how-and-why-writers-should-avoid-the-curse-of-knowledge/)

---

### H3. Definition-by-synonym (empty definition)

**Pattern:** Defining a term with another equally-jargony term. *"Schema markup is structured data that uses microdata vocabulary."*

**Mechanism:** Reader still can't form a mental model — the unknown just shifts.

**Fix:** Define with a concrete example, not a synonym chain. *"Schema markup is invisible code on a webpage that tells Google 'this is a recipe' or 'this is a product.'"*

**Severity:** M. **Detection:** qualitative.

**Sources:** [Pinker — Harvard](https://news.harvard.edu/gazette/story/2012/11/exorcising-the-curse-of-knowledge/)

---

### H4. Mixed audience ambiguity

**Pattern:** Document sometimes assumes expert knowledge, sometimes assumes naïveté, with no signaling of which paragraph is for whom.

**Fix:** Pick one audience. If multiple, segment with explicit headings: *"For experienced users"*, *"Background for newcomers."*

**Severity:** M. **Detection:** qualitative.

**Sources:** [Lumen technical writing: audience](https://courses.lumenlearning.com/suny-esc-technicalwriting/chapter/audience/)

---

### H5. Forward-reference / "we'll see later"

**Pattern:** Author defers explanation to a later section, leaving reader holding an unresolved question.

**Examples:**
- "We'll cover this in section 4."
- "More on this later."
- "As we'll see..."

**Mechanism:** Each forward reference loads working memory with an "open ticket" the reader has to remember.

**Fix:** Define inline at first mention, or restructure so the explanation comes first.

**Severity:** M. **Detection:** mechanical — regex for "as we'll see", "more on this later", "covered below", "we'll discuss".

**Sources:** [Pinker — Harvard](https://news.harvard.edu/gazette/story/2012/11/exorcising-the-curse-of-knowledge/)

---

## Group I — Structure / scannability

### I1. Buried lede

**Pattern:** Most important information arrives after secondary detail. Reader wades through 2–5 paragraphs to find the point.

**Mechanism:** First paragraph is the most-read; deferring the thesis means most readers leave before reaching it. F-pattern eyetracking confirms upper-left dominance.

**Fix:** BLUF — bottom line up front. Inverted pyramid: most newsworthy first, supporting details after.

**Severity:** H. **Detection:** qualitative.

**Sources:** [Wikipedia: BLUF](https://en.wikipedia.org/wiki/BLUF_(communication)), [Wikipedia: inverted pyramid](https://en.wikipedia.org/wiki/Inverted_pyramid_(journalism)), [NN/g: F-pattern](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/)

---

### I2. Missing thesis / no throughline

**Pattern:** Reader can't summarize the central claim after reading. No single sentence carries the point.

**Mechanism:** Without a top-level claim, all sub-claims are isolated facts. Working memory has nothing to hang them on. Violates Minto's Pyramid Principle.

**Fix:** Insert one sentence within the first 100 words: *"The point is X."* Each section thereafter supports it.

**Severity:** H. **Detection:** qualitative.

**Sources:** [Barbara Minto — McKinsey](https://www.mckinsey.com/alumni/news-and-events/global-news/alumni-news/barbara-minto-mece-i-invented-it-so-i-get-to-say-how-to-pronounce-it)

---

### I3. No topic sentence

**Pattern:** Paragraph has no opening sentence that telegraphs its point.

**Mechanism:** F-pattern readers scan first words and first sentences. Without topic sentences, scanning fails. Reader can't preview.

**Fix:** First sentence of each paragraph = the paragraph's claim.

**Severity:** H. **Detection:** qualitative.

**Sources:** [Indiana writing center on topic sentences](https://wts.indiana.edu/writing-guides/paragraphs-and-topic-sentences.html)

---

### I4. Missing transitions / no signposts

**Pattern:** Paragraphs jump between ideas without *however*, *in contrast*, *as a result*, *the second factor*.

**Mechanism:** Without transition words, the reader infers logical relationships, increasing extraneous load.

**Fix:** Add explicit transitions; signal direction changes.

**Severity:** M. **Detection:** heuristic — transition word density per N paragraphs (note: differs from AI-tell connector clichés like "furthermore" which are AI texture, not comprehension).

**Sources:** [UNC writing center on transitions](https://writingcenter.unc.edu/tips-and-tools/transitions/)

---

### I5. Hierarchy collapse

**Pattern:** Heading levels skip (H1 → H4) or only one level used. Long body of content with no subheadings at all.

**Mechanism:** Without visual hierarchy, scanners can't navigate. Skipping H2 to H4 confuses screen readers and breaks the document outline.

**Fix:** Use H1 once; H2 for major sections; H3 for sub-sections; never skip levels going down.

**Severity:** M (web). **Detection:** mechanical — heading-level scan.

**Sources:** [W3C heading structure](https://www.w3.org/WAI/tutorials/page-structure/headings/), [A11Y project](https://www.a11yproject.com/posts/how-to-accessible-heading-structure/)

---

### I6. No concrete examples

**Pattern:** Claim made in the abstract with no specific instance. *"Companies improved efficiency"* with no example company, action, or before/after.

**Mechanism:** Concrete words boost understanding by ~43%; pictures plus words by ~76%. Memory recall is higher for concrete sentences.

**Fix:** For each abstract claim, append *"for example"* + a specific instance.

**Severity:** M. **Detection:** qualitative.

**Sources:** [Wylie: concrete images in writing](https://www.wyliecomm.com/2020/02/concrete-images-in-writing/), [Vanderbilt: show don't tell](https://www.vanderbilt.edu/writing/resources/handouts/show-dont-tell/)

---

### I7. Nut-graf missing

**Pattern:** After the lede, no paragraph explains why the topic matters. Reader doesn't know stakes.

**Fix:** Add a "why this matters" paragraph within the first 200 words.

**Severity:** M. **Detection:** qualitative.

**Sources:** [Wikipedia: inverted pyramid](https://en.wikipedia.org/wiki/Inverted_pyramid_(journalism))

---

### I8. First sentence doesn't hook

**Pattern:** Opening sentence is throat-clearing, vague, or buries the question.

**Mechanism:** F-pattern readers consume the first 1–2 inches of headlines and the first sentence most heavily. If it doesn't deliver, they leave (55% spend <15 seconds on a page).

**Fix:** First sentence = clear question, claim, or stake.

**Severity:** H (web/marketing); M (academic). **Detection:** qualitative.

**Sources:** [NN/g: F-pattern reading](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/), [Omnizant: how people read online](https://omnizant.com/how-people-read-online/)

---

### I9. No skim layer

**Pattern:** All content presented at one density level. No bolded keywords, no callouts, no summary at top.

**Mechanism:** 79% of web users scan, only 16% read word-by-word. Without a skim layer (bold keywords, summary, callouts), scanners get nothing.

**Fix:** Add TL;DR at top; bold key phrases sparingly; use callout boxes for critical points.

**Severity:** M (web). **Detection:** mechanical — count bold/strong elements vs total prose; flag if zero bolded keywords in 500+ words.

**Sources:** [NN/g: concise, scannable, objective](https://www.nngroup.com/articles/concise-scannable-and-objective-how-to-write-for-the-web/)

---

### I10. Old-to-new inversion

**Pattern:** Sentences begin with new information, ending with familiar. Williams' principle: begin with old, end with new.

**Examples:**
- Bad: *"Quantum entanglement was Einstein's chief objection. We discussed this in the previous chapter."*
- Better: *"In the previous chapter we discussed Einstein's chief objection: quantum entanglement."*

**Mechanism:** Working memory uses old info as scaffolding for new. Inverting the order forces re-parsing.

**Fix:** Start sentences with what the reader already knows; end with the new information.

**Severity:** M. **Detection:** qualitative.

**Sources:** [Yale: coherence and old-to-new flow](https://poorvucenter.yale.edu/sites/default/files/2024-12/Coherence%20and%20Flow%20From%20Old%20to%20New%20Information%20GWL%20Handout.pdf), [Duke scientific writing](https://sites.duke.edu/scientificwriting/lesson-2-cohesion-coherence-and-emphasis/)

---

### I11. Prose-pretending-to-be-list (inverse)

**Pattern:** Bulleted list where items are causally connected and need narrative. Bullets strip the connections.

**Mechanism:** Removing connective tissue forces the reader to reconstruct the logical chain.

**Fix:** Convert to prose with explicit *"First X, which causes Y, then Z."*

**Severity:** L. **Detection:** qualitative.

**Sources:** [Writing Skills](https://www.writing-skills.com/bullets-wont-make-case)

---

### I12. Parallelism failure in lists

**Pattern:** Bullet points that mix grammatical forms.

**Examples:**
- *"Optimize the page; SEO best practices; Should we A/B test?"* (mixes verb / noun phrase / question)

**Mechanism:** Reader expects parallel structure. Mixing breaks the pattern and forces re-parsing.

**Fix:** Make every bullet start with the same form (verb, noun phrase, complete sentence).

**Severity:** M. **Detection:** parser-based; partial regex check (compare first POS of each bullet).

**Sources:** [GOV.UK style guide](https://www.gov.uk/guidance/style-guide)

---

## Group J — Sentence-level cognitive friction

### J1. Passive voice excess

**Pattern:** Passive constructions used where active is available. *"It was decided that..."* vs. *"The team decided..."*

**Mechanism:** Passive hides the agent, lengthens sentences, reverses subject-verb-object expectation.

**Fix:** Identify the actor; rewrite with the actor as subject.

**Severity:** M. **Detection:** mechanical — regex for *be + past participle*; flag when ratio exceeds 10% of sentences (Yoast threshold) or 5% (Monash / Readable).

**Sources:** [Yoast on passive voice](https://yoast.com/the-passive-voice-what-is-it-and-how-to-avoid-it/), [Readable: active voice](https://readable.com/blog/are-you-using-the-active-voice-in-your-content/)

---

### J2. Nominalization / zombie nouns

**Pattern:** Verbs converted to abstract nouns. *"Make a determination"* instead of *"decide"*. *"Implementation of optimization"* instead of *"we optimized"*.

**Examples:**
- "The implementation of the strategy resulted in the realization of efficiencies." → "We implemented the strategy and became more efficient."

**Mechanism:** Helen Sword's *zombie nouns* cannibalize active verbs, hiding the agent and the action. Forces extra words and abstraction.

**Fix:** Find *-tion / -ment / -ance / -ity* nouns; convert back to verbs.

**Severity:** M. **Detection:** mechanical — suffix-based regex.

**Sources:** [Helen Sword on zombie nouns — Skagit](https://www.skagit.edu/wp-content/uploads/2022/11/svcwc_wg_nominalizations.pdf), [Sword in NYT — LSU](https://www.lsu.edu/hss/english/files/university_writing_files/item51054.pdf)

---

### J3. Abstract noun stacking

**Pattern:** Sequences of abstract nouns (*strategy*, *framework*, *approach*, *methodology*) with no concrete referent.

**Examples:**
- *"The framework provides a strategy for implementation of methodology approaches."*

**Mechanism:** No mental image forms. Concrete words boost comprehension by ~43%. Memory recall is higher for concrete vs. abstract.

**Fix:** Replace each abstract with a concrete instance or example.

**Severity:** M. **Detection:** mechanical — flag strings of *-ity / -tion / -ness / -ment* in proximity.

**Sources:** [Wylie on concrete images](https://www.wyliecomm.com/2020/02/concrete-images-in-writing/), [Vanderbilt: show don't tell](https://www.vanderbilt.edu/writing/resources/handouts/show-dont-tell/)

---

### J4. Hedge stacking (comprehension version)

**Pattern:** Multiple qualifiers in one claim. *"It's somewhat likely that this could potentially be a mostly accurate answer."*

**Mechanism:** Reader can't extract the claim. Different from AI-slop hedge stacking — that pattern is about texture; this is about whether the reader can determine what's actually being said.

**Fix:** Pick one hedge if needed; cut the rest. State the claim.

**Severity:** M. **Detection:** mechanical — count hedge words (*somewhat*, *potentially*, *may*, *might*, *could*, *perhaps*, *arguably*, *relatively*) per sentence; flag at 3+.

**Sources:** [Jane Friedman on hedge inflation](https://janefriedman.com/hedge-word-inflation-words-prune/)

---

### J5. Decorative qualifiers / intensifier drift

**Pattern:** *Very*, *really*, *quite*, *extremely*, *incredibly* used non-functionally. Adds bulk without precision.

**Mechanism:** Each filler word steals attention without delivering meaning, increasing extraneous cognitive load (Sweller).

**Fix:** Cut or replace with stronger word. *"Very tired"* → *"exhausted."*

**Severity:** L. **Detection:** mechanical — regex.

**Sources:** [Grammarbook on qualifiers](https://www.grammarbook.com/blog/adjectives-adverbs/qualifiers-and-intensifiers/)

---

### J6. Ambiguous pronoun reference

**Pattern:** *It*, *this*, *they*, *that* with multiple possible antecedents.

**Examples:**
- *"The CEO told the manager that he had been promoted."* (Who?)

**Mechanism:** Reader pauses to resolve. Each ambiguity is a comprehension stutter.

**Fix:** Repeat the noun, or restructure so the antecedent is unambiguous.

**Severity:** M. **Detection:** parser-based; regex catches some cases (vague pronoun + 2+ candidate antecedents in prior sentence).

**Sources:** [Swarthmore on pronoun reference](https://www.swarthmore.edu/writing/pronoun-reference-0)

---

### J7. Misplaced or dangling modifier

**Pattern:** Modifying phrase placed away from what it modifies.

**Examples:**
- *"Walking down the street, the building looked tall."* (Building was walking?)

**Mechanism:** Reader's parsing fails; has to re-parse.

**Fix:** Move the modifier next to the subject; or rewrite to make the subject explicit.

**Severity:** M. **Detection:** parser-based; partial regex (sentence-initial *-ing* phrase + non-matching subject).

**Sources:** [Purdue OWL on dangling modifiers](https://owl.purdue.edu/owl/general_writing/mechanics/dangling_modifiers_and_how_to_correct_them.html)

---

### J8. Negative construction where positive available

**Pattern:** *Don't fail to remember* instead of *remember*. *Not infrequent* instead of *frequent*.

**Mechanism:** Negation requires extra processing — hold the proposition, then negate it. Strunk & White: *"Put statements in positive form."*

**Fix:** State positively.

**Severity:** L. **Detection:** mechanical — regex (*don't fail to / not un- / not in-*).

**Sources:** [Strunk & White](https://faculty.washington.edu/heagerty/Courses/b572/public/StrunkWhite.pdf)

---

## How to use this file

**During audit:** Walk groups F through J in order. For each pattern, scan the draft for instances. Flag with quote + severity. The scanner catches the mechanically-detectable subset (~17 of 35); the rest require reading.

**Severity guidelines:**
- **High severity:** acronym stacking, named-entity bombing, stat bombing, telegraphic colon-labeling, density-without-headings, long sentences, run-on sentences, coined terms used as known, curse of knowledge, buried lede, missing thesis, no topic sentence, first sentence doesn't hook
- **Medium severity:** wall of text, list-pretending-to-be-prose, definition-by-synonym, mixed audience, forward-reference, missing transitions, hierarchy collapse, no concrete examples, nut-graf missing, no skim layer, old-to-new inversion, parallelism failure, passive voice excess, nominalization, abstract noun stacking, hedge stacking, ambiguous pronoun, dangling modifier
- **Low severity:** glue-word bloat, prose-pretending-to-be-list, decorative qualifiers, negative construction

If a draft has 5+ H-severity violations within 500 words, recommend a substantial rewrite. See `calibration.md` for the dual-axis density formula.

## What this list is not

This is not "rules for good writing." Plenty of skilled writers use long sentences, named-entity-heavy prose, or list-like compression on purpose, in contexts where the reader has the schema. The point is that *prose written for a fresh reader who lacks context* will lose them when these patterns stack.

For Mahmoud's specific voice or other voice-aware judgments, see [`mahmouds-writing-voice`](https://github.com/MahmoudHalat/...). This file is voice-agnostic — it asks only "can a fresh reader follow this?", not "does this sound like the author."

Overlap with the AI-slop axis (`patterns.md`):
- **Decorative adverbs / qualifiers** — flagged on both axes for different reasons (texture vs cognitive load)
- **Hedge stacking** — texture hedge (AI-slop) vs claim-extractability hedge (comprehension)
- **Em-dash density** — AI signal AND telegraphic compression
- **Nominalization / abstract nouns** — AI texture vs no mental model

A piece can fail one axis and pass the other. The dual verdict in `audit-report-template.md` makes this explicit.
