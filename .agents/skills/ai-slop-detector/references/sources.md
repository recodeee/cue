# slop-cop — Research Sources

This skill is grounded in roughly 130 published sources across two axes:

- **AI-Slop axis** (sections 1–5): roughly 50 sources spanning peer-reviewed linguistic research, the canonical Wikipedia "Signs of AI writing" guide, AI-detector vendor methodology, practitioner literature, and viral takedowns in popular press.
- **Comprehension axis** (sections 6–10): roughly 80 sources spanning readability formula primary literature, cognitive load and working memory psychology, plain-language standards from government and accessibility bodies, web-reading research, and writing-craft canon.

The catalog is current through early 2026. Each source is annotated with a one-line description of what it contributes. URLs are listed verbatim; if a link rots, the title and description should be searchable.

---

## 1. Peer-reviewed / academic

The strongest evidence. These papers measure spike frequencies against pre-2022 baselines, run stylometric classifiers, or analyze corpora.

- **arXiv: Delving into ChatGPT usage in academic writing through excess vocabulary** — Quantifies the +6,697% rise in "delves" in 2024 PubMed abstracts vs 2020, plus +904% for "underscores" and +611% for "intricate." Estimates ≥13.5% of 2024 biomedical abstracts were processed with LLMs. [Link](https://arxiv.org/html/2406.07016v1)
- **arXiv: Why Does ChatGPT "Delve" So Much?** — Identifies the top-21 focal AI-frequency words (garnered, boasts, groundbreaking, advancements, etc.) and analyzes the RLHF mechanism behind them. [Link](https://arxiv.org/html/2412.11385v1)
- **medRxiv: Delving into PubMed Records — terms changed after ChatGPT** — Measures the term-frequency shift in PubMed abstracts pre/post-ChatGPT, confirms meticulous, pivotal, commendable as spike words. [Link](https://www.medrxiv.org/content/10.1101/2024.05.14.24307373v2.full)
- **arXiv: Measuring AI "Slop" in Text** — Defines and operationalizes "slop" as a quantitative property of text, with measurement methodology. [Link](https://arxiv.org/html/2509.19163v1)
- **arXiv: Towards Understanding Sycophancy in Language Models (Anthropic)** — The canonical paper on RLHF-induced sycophancy. Documents how reward models train obsequiousness across Claude and other LLMs. [Link](https://arxiv.org/pdf/2310.13548)
- **PLOS One: Distinguishing ChatGPT from human writing via Japanese stylometry** — Achieves ~99.8% classifier accuracy across 7 LLMs using stylometric features. Shows all models cluster tightly while humans spread broadly. [Link](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0288453)
- **Nature: Stylometric comparisons of human vs AI creative writing** — Cross-corpus stylometric analysis confirming model fingerprint clustering. [Link](https://www.nature.com/articles/s41599-025-05986-3)
- **SciRP: Hedging Devices in AI vs Human Essays** — Measures hedge frequency and hedge stacking in AI vs human writing samples. Foundation for the hedge-stacking pattern. [Link](https://www.scirp.org/journal/paperinformation?paperid=145708)

---

## 2. Canonical / community-maintained references

- **Wikipedia: Signs of AI writing** — The canonical community-maintained list. Updated regularly as models change. Explicit on the limitation: "Not all text featuring these indicators is AI-generated." Treats em dashes as contested post-GPT-5.1 (Nov 2025). [Link](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- **Wikipedia: AI slop** — Definitions and broader context for the AI-slop phenomenon. [Link](https://en.wikipedia.org/wiki/AI_slop)

---

## 3. Detector vendors (methodology pages)

These document what features classifiers actually use. Often candid about the limits of their own detectors.

- **GPTZero: Perplexity and burstiness explained** — Foundational explainer of the two metrics. Humans cluster 0.6-1.2 burstiness; LLMs 0.2-0.4. [Link](https://gptzero.me/news/perplexity-and-burstiness-what-is-it/)
- **GPTZero: Top 10 most common AI vocabulary** — Frequency data: "play a significant role in shaping" appears 182x more in AI; "today's fast-paced world" 107x; etc. [Link](https://gptzero.me/news/most-common-ai-vocabulary/)
- **Pangram Labs: Comprehensive guide to AI writing patterns** — 24 core LLM patterns with examples. Documents copula avoidance, present-participle tails, fabricated case studies. [Link](https://www.pangram.com/blog/comprehensive-guide-to-spotting-ai-writing-patterns)
- **Pangram: Why perplexity and burstiness fail** — Critique of older detection metrics; explains why prompt-engineered prose evades them. [Link](https://www.pangram.com/blog/why-perplexity-and-burstiness-fail-to-detect-ai)
- **Originality.ai: Most obvious ChatGPT sayings** — Practitioner blacklist with frequency-based ranking. Includes knowledge-cutoff disclaimer leakage. [Link](https://originality.ai/blog/obvious-chatgpt-sayings)
- **DeGPT: 50+ ChatGPT tells** — Comprehensive phrase-level catalog including sycophancy openers/closers, pedagogical voice, throat-clearing. [Link](https://www.degpt.app/blog/chatgpt-tells-phrases-list)
- **Quillbot: Burstiness and perplexity** — Vendor explainer with similar themes. [Link](https://quillbot.com/blog/ai-writing-tools/burstiness-and-perplexity/)

---

## 4. Practitioner literature

Writers, editors, and structured catalogs. Softer evidence individually, but agreement across sources strengthens any individual tell.

- **tropes.fyi: AI writing tropes directory** — Comprehensive structured catalog of LLM tropes with examples. Source for many less-famous patterns (magic adverbs, invented concept labels, dead-metaphor repetition). [Link](https://tropes.fyi/directory)
- **tropes.fyi: full markdown reference** — Complete catalog in markdown format. [Link](https://tropes.fyi/tropes-md)
- **agentkit AI tropes (sentence-structure)** — Reference list of sentence-level AI tells; source for anaphora abuse and dramatic countdown. [Link](https://github.com/joshuadavidthomas/agentkit/blob/main/skills/ai-writing-tropes/references/sentence-structure.md)
- **avoid-ai-writing skill (36 patterns)** — Conor Bronsdon's catalog of patterns to avoid in AI prose. [Link](https://github.com/conorbronsdon/avoid-ai-writing)
- **Beutler Ink: How to spot AI writing** — Practitioner guide; coined "compulsive summary" terminology. [Link](https://www.beutlerink.com/blog/how-to-spot-ai-writing)
- **Olivia Cal: 17 AI writing tells** — Editorial perspective on common giveaways. [Link](https://www.oliviacal.com/post/ai-writing-tells)
- **Hyacinth.ai: 42 phrases AI bots can't resist** — Phrase-level catalog with examples. [Link](https://hyacinth.ai/spot-ai-written-content-phrases/)
- **GoWinston: Most common ChatGPT words** — Frequency analysis of ChatGPT-favored vocabulary. [Link](https://gowinston.ai/most-common-chatgpt-words/)
- **Embryo: AI overuse list** — Practitioner blacklist with replacement suggestions. [Link](https://embryo.com/blog/list-words-ai-overuses/)
- **Content Beta: 300+ AI words** — Larger blacklist; useful for "While X, Y" opener documentation. [Link](https://www.contentbeta.com/blog/list-of-words-overused-by-ai/)
- **Twixify: 124+ overused words** — Frequency-ranked catalog. [Link](https://www.twixify.com/post/most-overused-words-by-chatgpt)
- **Kraabel: 200+ overused words** — Extended blacklist. [Link](https://www.kraabel.net/200-overused-words-and-phrases-in-ai-generated-content/)
- **Hanalarock: 10 ChatGPT-isms** — Editor's perspective on rhetorical tics including both-sides-ism. [Link](https://www.hanalarockwriting.com/post/10-common-chatgpt-isms-what-to-watch-out-for-when-writing-content-with-ai-infographics)
- **WriteWithAI: 10 dead giveaways** — Self-posed rhetorical question and crafted closer documentation. [Link](https://writewithai.substack.com/p/10-dead-giveaways-your-content-screams)
- **Hastewire: Linguistic patterns of AI writing** — Sentence-level pattern analysis. [Link](https://hastewire.com/blog/uncover-linguistic-patterns-of-ai-writing-key-tells)
- **STRYNG: Common AI sentence structures** — Top-six AI sentence-pattern analysis (false range, whether-or, present-participle tail). [Link](https://stryng.io/common-sentence-structures-in-ai-writing/)
- **Blake Stockton: Don't write like AI series** — Detailed per-pattern series; especially good on negation reversals. [Link](https://www.blakestockton.com/dont-write-like-ai-1-101-negation/)
- **Blake Stockton: Red flag words** — Vocabulary blacklist. [Link](https://www.blakestockton.com/red-flag-words/)
- **Augmented Educator: 10 telltale signs** — Education-context AI detection. [Link](https://www.theaugmentededucator.com/p/the-ten-telltale-signs-of-ai-generated)
- **aiphrasefinder: 100 common ChatGPT phrases** — Phrase-frequency catalog. [Link](https://aiphrasefinder.com/common-chatgpt-phrases/)
- **Atlas: Top 10 AI clichés** — High-frequency phrase ranking; documents "objective study aimed" 269x ratio. [Link](https://www.atlas.org/blog/artificial-intelligence/top-10-cliches-in-ai-generated-text)
- **Grammarly: Hedging language guide** — Foundation for hedge-stacking and hedged-superlative patterns. [Link](https://www.grammarly.com/blog/writing-techniques/hedging-language/)
- **Hemingway App: Fix adverbs and toggle highlights** — General writing guidance on adverb minimization that compounds with AI's adverb overuse. [Link](https://hemingwayapp.com/blog/posts/20240624-fix-adverbs-and-toggle-highlights)
- **GRC Health: Predictable rhetoric of AI** — Documents copula avoidance with specific examples. [Link](https://www.grc-health.com/knowledge-centre/the-predictable-rhetoric-of-ai-generated-text-overused-stylistic-devices)
- **Sai Gaddam Medium: It isn't just X, it's Y** — Deep analysis of the negation reversal pattern. [Link](https://saigaddam.medium.com/it-isnt-just-x-it-s-y-54cb403d61a8)
- **Ruben Hassid Substack: It's not X, it's Y** — Companion piece on the same pattern. [Link](https://ruben.substack.com/p/its-not-x-its-y)
- **Storylab.ai: Blog title generator analysis** — Documents the "X: A Comprehensive Guide" title pattern. [Link](https://storylab.ai/blog-title-generator/)
- **Hunting the Muse: How to tell if writing is AI** — Practitioner guide on title and structural patterns. [Link](https://huntingthemuse.net/library/how-to-tell-if-writing-is-ai)

---

## 5. Viral takedowns / popular press / commentary

Cultural-moment documentation. Useful for understanding which tells went viral and when (which informs the sanding-off problem).

- **Rolling Stone: ChatGPT em dash giveaway** — The viral em-dash takedown. Pre-dates GPT-5.1's opt-out. [Link](https://www.rollingstone.com/culture/culture-features/chatgpt-hypen-em-dash-ai-writing-1235314945/)
- **TechRadar: Em dash era is over** — Post-GPT-5.1 reassessment of the em dash as a tell. Important for the contested-tell calibration. [Link](https://www.techradar.com/ai-platforms-assistants/chatgpt/the-days-of-the-em-dash-being-a-chatgpt-giveaway-are-over-its-time-to-bring-it-back)
- **LitHub: Handy guide to spotting AI** — Editor's catalog including servile-positivity and tone-uplift patterns. [Link](https://lithub.com/heres-a-handy-guide-to-help-you-spot-ai-writing/)
- **Scientific American: ChatGPT and Gemini have unique writing styles** — Source for model-fingerprint analysis (GPT vs Claude vs Gemini). [Link](https://www.scientificamerican.com/article/chatgpt-and-gemini-ai-have-uniquely-different-writing-styles/)
- **Type.ai: Claude vs GPT comparison** — Practitioner-level comparison of model voices. [Link](https://blog.type.ai/post/claude-vs-gpt)
- **The Conversation: AI's "it's not X, it's Y" stylistic negation** — Academic-flavored analysis of the negation pattern with cognitive-psych grounding. [Link](https://theconversation.com/slanguage-why-ais-stylistic-negation-its-not-x-its-y-is-both-annoying-and-doesnt-work-278967)
- **The Decoder: Reddit users compile ChatGPT phrase list** — Coverage of the community-sourced phrase blacklist. [Link](https://the-decoder.com/reddit-users-compile-list-of-words-and-phrases-that-unmask-chatgpts-writing-style/)
- **The Ignorance Field Guide to AI Slop** — Cultural commentary on the slop phenomenon. [Link](https://www.ignorance.ai/p/the-field-guide-to-ai-slop)
- **Influence Intelligence: AI vocabulary of the internet** — Documents how AI-favored vocabulary spreads through the web. [Link](https://influenceintelligence.substack.com/p/slop-and-signal-the-new-vocabulary)
- **Dead Language Society: Why ChatGPT writes like that** — Colin Gorrie's rhetorical analysis; foundation for tricolon-abuse documentation. [Link](https://www.deadlanguagesociety.com/p/rhetorical-analysis-ai)
- **LessWrong: Why do LLMs say "It's not X, it's Y"** — Technical analysis of the RLHF mechanism. [Link](https://www.lesswrong.com/posts/RzPXywNbsRCss3Swy/why-do-llms-so-often-say-it-s-not-an-x-it-s-a-y)
- **LessWrong: Demands are all you need** — Prompt-imperativeness research relevant to hedge stacking. [Link](https://www.lesswrong.com/posts/vBDupg8iPqgdwhFzz/demands-are-all-you-need-prompt-imperativeness-drastically)
- **Sean Goedecke: Sycophancy as the first LLM dark pattern** — Engineer's perspective on RLHF-induced sycophancy. [Link](https://www.seangoedecke.com/ai-sycophancy/)
- **The Batch: OpenAI pulls GPT-4o update after sycophancy** — News coverage of the April 2025 GPT-4o sycophancy scare. [Link](https://www.deeplearning.ai/the-batch/openai-pulls-gpt-4o-update-after-users-report-sycophantic-behavior/)
- **Cory Doctorow: Writing vs AI** — Author commentary on AI writing, including em-dash defense. [Link](https://pluralistic.net/2026/01/07/delicious-pizza/)
- **SFU Library: Writing conclusions** — Pre-AI but relevant to compulsive-summary documentation. [Link](https://www.lib.sfu.ca/about/branches-depts/slc/writing/organization/conclusions)
- **aiproductivity.ai: The negation pattern** — Practitioner-level analysis of "It's not X, it's Y" as a marker. [Link](https://aiproductivity.ai/news/ai-writing-pattern-its-not-x-its-y-negation/)
- **trySight: SEO content generation** — Documents the "Comprehensive Guide" title pattern in SEO contexts. [Link](https://www.trysight.ai/blog/seo-content-generation-for-beginners)

---

---

## 6. Comprehension axis — readability formulas (primary literature)

The eight metrics in `readability-metrics.md` come from this body of work. Treat formula scores as diagnostic, not decisive — every primary source notes domain-specific limits.

- **Flesch (1948): A new readability yardstick** — *Journal of Applied Psychology* 32(3). The original Flesch Reading Ease formula (206.835 − 1.015 ASL − 84.6 ASW). Validated on news, business, and government writing. [DOI](https://doi.org/10.1037/h0057532)
- **Kincaid, Fishburne, Rogers, Chissom (1975): Derivation of new readability formulas** — Naval Technical Training, Research Branch Report 8-75. Source for the Flesch-Kincaid Grade Level formula used by US federal documents and Microsoft Word. [PDF](https://stars.library.ucf.edu/istlibrary/56/)
- **McLaughlin (1969): SMOG grading — A new readability formula** — *Journal of Reading* 12(8). Polysyllable-count formula stable above ~30 sentences. [JSTOR](https://www.jstor.org/stable/40011226)
- **Coleman & Liau (1975): A computer readability formula** — *Journal of Applied Psychology* 60(2). Letters-per-100-words and sentences-per-100-words formula; deliberately avoids syllable counting. [DOI](https://doi.org/10.1037/h0076540)
- **Dale & Chall (1948, revised 1995): A formula for predicting readability** — *Educational Research Bulletin* 27(1). Uses a curated 3,000-word "easy" wordlist. The 1995 revision is the canonical version. [Original](https://www.jstor.org/stable/1473669)
- **DuBay (2004): The principles of readability** — Comprehensive review of 200+ readability formulas, their derivation, and validation. Best single overview of the field's history and limits. [PDF](https://files.eric.ed.gov/fulltext/ED490073.pdf)
- **Halliday & Hasan (1976): Cohesion in English** — Longman. Foundation for lexical density measurement (content words ÷ total words). The original definition that automated tools approximate. [Worldcat](https://www.worldcat.org/title/cohesion-in-english/oclc/1947985)
- **Ure (1971): Lexical density and register differentiation** — In *Applications of Linguistics*. Empirical study showing 40–55% lexical density for spoken/casual prose, 55–65% for written/academic. Source for our audience targets. [Citation](https://scholar.google.com/scholar?q=Ure+1971+lexical+density)
- **Bormuth (1969): Cloze readability procedure** — *Reading Research Quarterly*. Establishes the cloze test as the validation gold-standard for readability formulas. [JSTOR](https://www.jstor.org/stable/747084)

---

## 7. Comprehension axis — cognitive psychology (working memory, load, and processing)

These papers ground the "why" — *why* dense acronyms or run-on sentences cause comprehension failure, not just style preference.

- **Miller (1956): The magical number seven, plus or minus two** — *Psychological Review* 63(2). The classic working-memory paper. Foundation for chunking thresholds in our F-group patterns. [DOI](https://doi.org/10.1037/h0043158)
- **Cowan (2001): The magical number 4 in short-term memory** — *Behavioral and Brain Sciences* 24(1). Modern revision of Miller's number. The 4-chunk limit drives our acronym and named-entity density caps. [DOI](https://doi.org/10.1017/S0140525X01003922)
- **Baddeley (2000): The episodic buffer — A new component of working memory?** — *Trends in Cognitive Sciences* 4(11). Explains why integrating new entities while parsing syntax is so costly. [DOI](https://doi.org/10.1016/S1364-6613(00)01538-2)
- **Sweller (1988): Cognitive load during problem solving** — *Cognitive Science* 12(2). Original cognitive load theory. Distinguishes intrinsic, extraneous, and germane load — extraneous load is what bad prose imposes. [DOI](https://doi.org/10.1207/s15516709cog1202_4)
- **Sweller, van Merriënboer, Paas (1998): Cognitive architecture and instructional design** — *Educational Psychology Review* 10(3). Foundational for the "split-attention effect" — relevant to our forward-reference and undefined-acronym patterns. [DOI](https://doi.org/10.1023/A:1022193728205)
- **Just & Carpenter (1992): A capacity theory of comprehension** — *Psychological Review* 99(1). Demonstrates working-memory capacity as the bottleneck for sentence comprehension. [DOI](https://doi.org/10.1037/0033-295X.99.1.122)
- **Gibson (1998): Linguistic complexity — Locality of syntactic dependencies** — *Cognition* 68(1). The Dependency Locality Theory: long syntactic dependencies (subject-verb separation, embedded clauses) tax working memory. Drives the run-on and long-sentence patterns. [DOI](https://doi.org/10.1016/S0010-0277(98)00034-1)
- **Pinker (2014): The Sense of Style** — Viking. Source for "curse of knowledge" framing — experts forget what was hard to learn. Drives the H-group audience-assumption patterns. [Worldcat](https://www.worldcat.org/title/sense-of-style/oclc/872364305)
- **Chase & Simon (1973): Perception in chess** — *Cognitive Psychology* 4(1). Original chunking-by-expertise study. Why writers in their own field cannot judge a fresh reader's comprehension. [DOI](https://doi.org/10.1016/0010-0285(73)90004-2)

---

## 8. Comprehension axis — plain-language standards and government style guides

Empirical and policy-driven thresholds. These are what real public-facing institutions enforce.

- **Plain Writing Act of 2010 (US Public Law 111-274)** — Federal law requiring agencies to use plain language. Implementation guidance recommends 8th-grade reading level. [Text](https://www.govinfo.gov/app/details/PLAW-111publ274)
- **plainlanguage.gov: Federal plain language guidelines** — The US federal style guide for plain writing. Active voice, short sentences, 8th-grade target. [Site](https://www.plainlanguage.gov/guidelines/)
- **GOV.UK: Content design — Style and tone** — UK government style guide. Hard targets: 9-year-old reading age for most content. Strict on jargon and acronyms. [Site](https://www.gov.uk/guidance/content-design/writing-for-gov-uk)
- **GOV.UK: Service Manual — Writing for users** — Companion guide for service designers. Source of the "explain on first use, abbreviate on second" rule. [Site](https://www.gov.uk/service-manual/design/writing-for-user-interfaces)
- **WCAG 2.1 Success Criterion 3.1.5 (Reading Level)** — W3C accessibility standard. AAA-conformant content must not exceed lower-secondary reading ability (~9th grade) or provide a supplemental version. [Spec](https://www.w3.org/TR/WCAG21/#reading-level)
- **WCAG 2.1 Success Criterion 3.1.3 (Unusual Words)** — AAA: provide definition mechanism for jargon, idioms, and abbreviations. Source for our undefined-acronym threshold. [Spec](https://www.w3.org/TR/WCAG21/#unusual-words)
- **WCAG 2.1 Success Criterion 3.1.4 (Abbreviations)** — AAA: provide expansion mechanism for abbreviations. [Spec](https://www.w3.org/TR/WCAG21/#abbreviations)
- **CDC: Clear Communication Index** — US Centers for Disease Control framework with 4-question scoring system for health-communication content. Strong on numeric framing (which informs our stat-bombing pattern). [PDF](https://www.cdc.gov/ccindex/pdf/full-index.pdf)
- **NIH: Clear and simple — Developing effective print materials for low-literate readers** — National Institutes of Health guide; source for plain-language thresholds in healthcare audience. [Archive](https://www.cancer.gov/publications/health-communication/clear-and-simple)
- **EU: Joint Practical Guide for the drafting of EU legislation** — Codifies plain-drafting rules across 24 EU languages. Notable for explicit caps on sentence length in legal text. [PDF](https://eur-lex.europa.eu/content/techleg/EN-legislative-drafting-guide.pdf)
- **Center for Plain Language: 2024 Federal Plain Language Report Card** — Annual audit of US federal agency compliance with plain-writing rules. Data on which patterns reliably tank scores. [Site](https://centerforplainlanguage.org/2024-federal-plain-language-report-card/)
- **Australian Government Style Manual** — Modern reference for government writing; particularly clear on the difference between "writing simply" and "writing simplistically." [Site](https://www.stylemanual.gov.au/)

---

## 9. Comprehension axis — web reading research and information architecture

How people actually read on screens. Drives the I-group structural patterns (no skim layer, hierarchy collapse, wall-of-text).

- **Nielsen (1997): How users read on the web** — Nielsen Norman Group. The original eye-tracking finding: 79% of users scan, only 16% read word-for-word. [Article](https://www.nngroup.com/articles/how-users-read-on-the-web/)
- **Nielsen (2006): F-shaped pattern for reading web content** — NN/g. The classic eye-tracking heatmap study showing horizontal-then-vertical scanning. Foundation for the "no skim layer" pattern. [Article](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/)
- **Pernice (2017): F-pattern reading on the web debunked?** — NN/g follow-up confirming the F-pattern still applies but is interrupted by good visual hierarchy (headings, lists, emphasis). [Article](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content-discovered/)
- **Nielsen (2008): How little do users read?** — Empirical study showing readers absorb only ~20% of text on a typical page. Justifies our short-paragraph and skim-layer thresholds. [Article](https://www.nngroup.com/articles/how-little-do-users-read/)
- **Loranger & Nielsen (2013): Plain language is for everyone, even experts** — NN/g. Demonstrates that even subject-matter experts prefer simpler prose for fast scanning. Counters the "my audience can handle complexity" defense. [Article](https://www.nngroup.com/articles/plain-language-experts/)
- **Krug (2014): Don't Make Me Think (3rd ed.)** — New Riders. Canonical book on web usability. Foundation for "scannability over readability" framing. [Worldcat](https://www.worldcat.org/title/dont-make-me-think-revisited/oclc/879583144)
- **Wilkinson, Payne, Heinz, Stoops (2011): Online reading vs paper reading** — *Journal of Computing in Higher Education* 23(2). Shows comprehension drops 20–30% when the same text is read on screen vs paper. [DOI](https://doi.org/10.1007/s12528-011-9050-y)
- **Mangen, Walgermo, Brønnick (2013): Reading linear text on paper vs computer screen** — *International Journal of Educational Research* 58. Key finding: hypertext and on-screen formats fragment reading. [DOI](https://doi.org/10.1016/j.ijer.2012.12.002)
- **GOV.UK Design System: Typography** — Codifies a 75-character measure (line length) cap based on legibility research. Relevant to wall-of-text and paragraph-length patterns. [Site](https://design-system.service.gov.uk/styles/typography/)

---

## 10. Comprehension axis — writing-craft canon and editorial practice

Writers and editors are the practical authority on what creates and removes friction. These overlap with section 4 (practitioner AI-slop sources) but focus specifically on comprehension and clarity.

- **Strunk & White (1959): The Elements of Style** — Macmillan. The classic. Source for "omit needless words," "use the active voice," and the active-vs-passive heuristics. [Worldcat](https://www.worldcat.org/title/elements-of-style/oclc/796366)
- **Williams & Bizup (2017): Style — Lessons in Clarity and Grace (12th ed.)** — Pearson. The most rigorous modern style guide. Source for nominalization detection ("zombie nouns") and old-information-first principle. [Worldcat](https://www.worldcat.org/title/style-lessons-in-clarity-and-grace/oclc/968707437)
- **Pinker (2014): Why academic writing stinks** — *Chronicle of Higher Education*. Companion essay to *The Sense of Style*. Key on "curse of knowledge" and metadiscourse. [Article](https://www.chronicle.com/article/why-academics-stink-at-writing/)
- **Sword (2012): Stylish Academic Writing** — Harvard University Press. Empirical study of 1,000 published academic articles. Documents which patterns predict reader engagement. [Worldcat](https://www.worldcat.org/title/stylish-academic-writing/oclc/766957322)
- **Sword: The Writer's Diet** — Online tool implementing Sword's friction-detection heuristics: be-verbs, abstract nouns, prepositions, "it/this/that," waste words. Algorithmic precursor to several of our J-group patterns. [Site](https://www.writersdiet.com/test.php)
- **Hemingway Editor: Method documentation** — Web tool that flags adverbs, passive voice, complex sentences, hard-to-read sentences. Direct ancestor of our long-sentence and decorative-qualifier patterns. [Site](https://hemingwayapp.com/)
- **Garner (2016): Garner's Modern English Usage (4th ed.)** — Oxford. Exhaustive reference on usage; particularly strong on bureaucratic prose. Source for several telegraphic-colon and parallelism-failure patterns. [Worldcat](https://www.worldcat.org/title/garners-modern-english-usage/oclc/930506586)
- **Zinsser (2006): On Writing Well (30th ann. ed.)** — Harper. Practical canon. Foundation for the "every sentence should pull its own weight" heuristic embedded in our density scoring. [Worldcat](https://www.worldcat.org/title/on-writing-well/oclc/61362317)
- **Lanham (2006): Revising Prose (5th ed.)** — Pearson. Introduces the "Paramedic Method" for sentence revision: circle prepositions, find "is," find action, kick the doer back to the front. Algorithmic source for several J-group patterns. [Worldcat](https://www.worldcat.org/title/revising-prose/oclc/61130601)
- **Provost (1985): 100 Ways to Improve Your Writing** — Mentor. Pithy practitioner reference. Source for paragraph-rhythm and sentence-length-variance heuristics that complement our burstiness measure. [Worldcat](https://www.worldcat.org/title/100-ways-to-improve-your-writing/oclc/13109293)
- **Klare (1976): A second look at the validity of readability formulas** — *Journal of Reading Behavior* 8(2). Critical review showing that formulas predict difficulty but not comprehension; backs our "metrics calibrate, patterns score" architecture. [DOI](https://doi.org/10.1080/10862967609547179)
- **Bailin & Grafstein (2016): Readability — Text and Context** — Palgrave Macmillan. Modern critique of readability formulas; argues for context-sensitive measurement. Strongest argument for our audience-calibration approach. [Worldcat](https://www.worldcat.org/title/readability-text-and-context/oclc/953461103)
- **Chartered Institute of Editing and Proofreading: Editorial Style Guide** — UK professional standards body. Practical authority on what editors actually correct. [Site](https://www.ciep.uk/standards/)

---

## How to use this file

The reference files cite specific sources for specific claims. Each axis has its own catalog and citation conventions:

- **AI-Slop axis**: `patterns.md`, `vocabulary.md`, `formatting-tells.md` cite sections 1–5 above.
- **Comprehension axis**: `comprehension.md` and `readability-metrics.md` cite sections 6–10 above.
- **`calibration.md`**: cross-references both axes.

When you see a source name in a reference file, this file is the master index — find it here for full title and link.

Three pillars of evidence:

1. **Peer-reviewed linguistics** (Section 1) — strongest. These papers measure spike frequencies against pre-2022 baselines, run stylometric classifiers, or analyze corpora.
2. **Wikipedia: Signs of AI writing** (Section 2) — the canonical community-maintained list. Updated regularly as models change. Treats em dashes as contested post-GPT-5.1.
3. **Practitioner / vendor / popular press** (Sections 3-5) — softer evidence individually, but agreement across sources strengthens any individual tell.

When sources contradict each other (em dashes are the main case — peer-reviewed work flags them; popular press post-Nov 2025 reports the era ending), `calibration.md` documents the contestation rather than picking a side.

Coverage gaps to flag:

- Most sources are English-language and US/UK-oriented. Multilingual AI tells likely have different signatures.
- Older sources (2023, early 2024) document the v1 vocabulary list (delve, tapestry). Sophisticated authors prompt-engineer around these. Newer sources (late 2024, 2025) document the post-sanding tells (copula avoidance, present-participle tails, hedge stacking).
- Detection itself is an evolving target. The catalog will need updating as models, RLHF objectives, and writer-side prompt engineering co-evolve.
