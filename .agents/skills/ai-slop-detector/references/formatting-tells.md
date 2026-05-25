# AI Slop — Formatting and Structural Tells

These tells aren't about prose; they're about the shape of the output. LLMs default to predictable formatting choices — bold-first bullets, "X: A Comprehensive Guide" titles, exactly-three-H2s structures, fractal recaps. Each one is a weak tell on its own; in clusters they're a strong signal.

This file covers what the prose-level patterns and vocabulary lists don't catch. The mechanical scanner detects most of these; some require reading.

---

## 3A. Markdown / list formatting

LLM training data is full of bulleted documentation, FAQ pages, and Q-and-A SEO templates. RLHF then rewards "well-structured" answers. The result: models reach for bullets, headers, and bolded keywords by default — even when running prose would serve the reader better. These ten tells are the most reliable visual fingerprints of unedited LLM output.

1. **Bold-first bullets** — Every bullet starts with **bolded keyword:** then explanation. Universal in LLM output and the single most recognisable structural fingerprint. Severity: H. [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), [Pangram](https://www.pangram.com/blog/comprehensive-guide-to-spotting-ai-writing-patterns).
2. **Inline-header lists** — Numbered items where each is a bolded inline header followed by colon and prose ("1. **Speed:** The system processes..."). Wikipedia's number-one formatting tell. Severity: H. [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
3. **Excessive H2/H3 nesting** — Short pieces with 5+ subheaders; treats every paragraph as its own section. Severity: M. [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), [Beutler Ink](https://www.beutlerink.com/blog/how-to-spot-ai-writing).
4. **Emoji bullets** — Using `🔹` `✨` `📌` `🎯` `💡` instead of `-` or `*`. Severity: M-H. [Pangram](https://www.pangram.com/blog/comprehensive-guide-to-spotting-ai-writing-patterns), [Ignorance.ai](https://www.ignorance.ai/p/the-field-guide-to-ai-slop).
5. **Unicode decoration** — Arrows (→), smart quotes / curly apostrophes outside markdown, bold-italic Unicode characters (𝗯𝗼𝗹𝗱). Severity: M. [Pangram](https://www.pangram.com/blog/comprehensive-guide-to-spotting-ai-writing-patterns).
6. **Numbered lists for short ideas** — Three-item numbered lists where a single sentence would carry the same meaning. Severity: M. [Beutler Ink](https://www.beutlerink.com/blog/how-to-spot-ai-writing).
7. **Title-case headings** — Every Word Capitalized in headings even where house style is sentence-case. Severity: M. [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
8. **Universal Oxford comma + American spelling** — AI defaults to both regardless of dialect. Isolated, not damning; a weak corroborating tell. Severity: L. [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
9. **Code-style backticks misused in prose** — `` `term` `` used where italics or quotation marks belong. Severity: L. [Pangram](https://www.pangram.com/blog/comprehensive-guide-to-spotting-ai-writing-patterns).
10. **Markdown bleed** — Visible asterisks (`*text*`, `**bold**`) appearing on a platform that doesn't render them. Direct paste-from-ChatGPT artifact. Severity: H. [Ignorance.ai](https://www.ignorance.ai/p/the-field-guide-to-ai-slop), [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).

Run the scanner — it catches bold-first bullets, emoji bullets, markdown bleed, and backtick misuse with high precision. Read the piece for the rest, especially heading-case consistency against the surrounding house style.

---

## 3B. Title patterns

Headlines are the most-trained-on text on the open web. SEO templates ("X: A Comprehensive Guide"), People-Also-Ask scrapes (question-headings), and listicle conventions (5/7/10) saturate the training corpus. LLMs reproduce these formulas verbatim because the reward signal during fine-tuning told them these are what "good" titles look like.

1. **Colon-pattern titles** — "X: A Comprehensive Guide", "X: Everything You Need to Know", "X: A Step-by-Step Guide". Severity: M-H. [Storylab.ai](https://storylab.ai/blog-title-generator/), [Hunting the Muse](https://huntingthemuse.net/library/how-to-tell-if-writing-is-ai).
2. **"The Ultimate Guide to X" / "The Definitive Guide to X"** — Pure SEO-template residue. Severity: H. [Hunting the Muse](https://huntingthemuse.net/library/how-to-tell-if-writing-is-ai), [trySight](https://www.trysight.ai/blog/seo-content-generation-for-beginners).
3. **Numbered listicles in 5/7/10** — "10 Reasons", "7 Tips", "5 Ways". The 5/7/10 cluster is overrepresented because these are the canonical listicle counts in the training corpus. Severity: L. [Storylab.ai](https://storylab.ai/blog-title-generator/).
4. **"How to X in [year]"** — "How to Rank in 2025" / "How to Invest in 2026". Severity: L. [trySight](https://www.trysight.ai/blog/seo-content-generation-for-beginners).
5. **Question-headings** — H2/H3 phrased as questions ("What is X?", "Why does X matter?") inside prose articles. People-Also-Ask SEO artifact bleeding into general writing. Severity: M. [Hunting the Muse](https://huntingthemuse.net/library/how-to-tell-if-writing-is-ai).

The scanner can match title strings, but it can't tell whether "Comprehensive Guide" is appropriate for the brief. Read the headline against the genre — a research review can earn one; a personal blog post cannot.

---

## 3C. Section-organization patterns

These tells emerge from two pressures fused together: the five-paragraph essay structure baked into instructional training data, and RLHF's preference for "show your work" answers. The model wants to demonstrate that it understood the question (acknowledgment loop), preview what it's about to say (TL;DR), and prove it stayed on topic (compulsive recap). Real writers trust the reader more.

1. **Acknowledgment-loop opening** — First paragraph paraphrases the title or restates the question before answering. Severity: H. [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing), [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
2. **TL;DR / Key Takeaways at top** — Bolded bulleted summary block before the body. Severity: M. [Beutler Ink](https://www.beutlerink.com/blog/how-to-spot-ai-writing).
3. **"In conclusion" or "To wrap up" section** — Compulsive recap that compresses the body into a closing block. Severity: H. [Beutler Ink](https://www.beutlerink.com/blog/how-to-spot-ai-writing), [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
4. **Section pattern: Intro → exactly 3-5 H2s → conclusion** — The five-paragraph essay scaled up into the standard SEO blog skeleton. Severity: M. [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing).
5. **"Challenges and Future Directions" section in any topic** — Wikipedia-flagged formula. Appropriate inside a research review; an immediate tell on a blog post about pizza. Severity: H. [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
6. **Mini-summary at top of each section** — Fractal recap; the same content rephrased at every nesting level. Severity: M. [Beutler Ink](https://www.beutlerink.com/blog/how-to-spot-ai-writing).

These are read tells, not scanner tells. Skim the document outline (titles + headings + first sentence of each section) and check whether the structure matches the brief or whether it's been forced into the SEO-essay shape.

---

## 3D. Repetition / uniformity

LLMs sample tokens from a probability distribution conditioned on prior context. The same model on the same prompt produces sentences of similar length, similar grammatical shape, and similar opening structure — because the conditional distribution doesn't vary the way a human writer's intent varies from sentence to sentence. Burstiness research (the variance in sentence length and structure) is the most quantitatively documented signal across the field.

1. **Uniform sentence length / low burstiness** — AI averages 15-25 words per sentence with low variance; human writing has sentence-length standard-deviation-to-mean ratios of 0.6-1.2 versus AI's 0.2-0.4. Severity: H. [GPTZero](https://gptzero.me/news/perplexity-and-burstiness-what-is-it/), [Hastewire](https://hastewire.com/blog/uncover-linguistic-patterns-of-ai-writing-key-tells).
2. **Uniform paragraph length** — Same number of sentences per paragraph through the whole piece. Severity: H. [Hastewire](https://hastewire.com/blog/uncover-linguistic-patterns-of-ai-writing-key-tells).
3. **No fragments or run-ons** — Every sentence grammatically complete; no rhythm-breaking. Real prose has both. Severity: M. [Pangram](https://www.pangram.com/blog/comprehensive-guide-to-spotting-ai-writing-patterns).
4. **No contractions** — "It is" and "do not" clusters where "it's" and "don't" would be natural. Severity: M. [Pangram](https://www.pangram.com/blog/comprehensive-guide-to-spotting-ai-writing-patterns).
5. **Zero typos / suspiciously perfect grammar** — In casual prose contexts where minor errors are normal. Severity: L. [Hastewire](https://hastewire.com/blog/uncover-linguistic-patterns-of-ai-writing-key-tells).
6. **Same paragraph opener type** — Every paragraph begins with a similar sentence structure (e.g. all start with a subject-noun, or all with a participial phrase). Severity: M. [Hastewire](https://hastewire.com/blog/uncover-linguistic-patterns-of-ai-writing-key-tells).
7. **Identical sentence structures repeating** — Three or more subject-verb-object sentences in a row, same shape. Severity: H. [Pangram](https://www.pangram.com/blog/comprehensive-guide-to-spotting-ai-writing-patterns).
8. **Bigram repetition** — The same two-word phrase appearing 5+ times across a single piece. Severity: H. [Pangram](https://www.pangram.com/blog/comprehensive-guide-to-spotting-ai-writing-patterns).

The scanner reports burstiness, contraction ratio, paragraph-length variance, and bigram counts mechanically. Trust those numbers but verify by reading three random paragraphs — uniformity feels different from how it scores.

---

## 3E. Whitespace / spacing patterns

Whitespace tells fall into two buckets: rhythm defaults (single-sentence paragraphs and the three-sentence cadence are LLM defaults, not deliberate choices) and copy-paste artifacts (curly quotes mixed with straight, weird en-space indents) that betray the rendering pipeline. These are the easiest to overlook because they're almost invisible.

1. **Single-sentence paragraphs throughout** — Substack/LinkedIn rhythm applied without judgment, regardless of subject. Severity: M. [Pangram](https://www.pangram.com/blog/comprehensive-guide-to-spotting-ai-writing-patterns).
2. **Consistent ~3-sentence paragraph rhythm** — AI's default; every paragraph clocks in at the same count. Severity: M. [Hastewire](https://hastewire.com/blog/uncover-linguistic-patterns-of-ai-writing-key-tells).
3. **Curly quotes / smart apostrophes mixed with straight** — Direct copy-paste-from-ChatGPT artifact; the model emits curly, the surrounding text uses straight. Severity: M. [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
4. **Three-en-space indents or other unusual whitespace** — Markdown-rendering artifacts that survive copy-paste. Severity: L. [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).

The scanner detects mixed-quote characters and unusual whitespace bytes; paragraph rhythm shows up in the burstiness metrics. View the raw bytes if a piece feels off but you can't see why — invisible characters often explain it.

---

## How to use this file

1. Run the scanner first — `scripts/scan.py` detects most of these mechanically, including bold-first bullets, emoji bullets, burstiness, paragraph uniformity, contraction ratio, and bigram repetition.
2. The scanner can't tell whether a "Comprehensive Guide" title is appropriate — that requires reading the brief. Same for "Challenges and Future Directions" sections — appropriate for a research paper, AI-tell for a blog post.
3. Severity tiers apply: H tells are always cut; M tells are cut absent strong context; L tells inform the report but don't down-score.
4. Density still rules. A single bold-first bullet in a 3,000-word document is not a signal. Five of them in 500 words is.

See `calibration.md` for the density-scoring formula and genre-specific thresholds.
