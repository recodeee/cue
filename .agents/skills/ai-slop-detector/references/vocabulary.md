# AI Slop Vocabulary — The Cut List

The phrases below trigger AI-detection radar instantly. Each one is documented in published research, AI-detector vendor methodology, or community-sourced lists with high agreement. The mechanical scanner (`scripts/scan.py`) catches every instance; this file is the human-readable reference with replacements and rationale.

Use this as a search-and-destroy list during a final pass. For each hit, ask: does this word survive the context? In almost every case, the answer is no — cut it.

## How severity works

- **H (always cut):** the phrase is essentially never the right choice. Cut without exception unless ironic / scare-quoted.
- **M (usually cut):** the phrase survives in narrow bands. Default is to cut; keep only if doing specific work.
- **L (context-dependent):** weak tell on its own. Note in audit but don't down-score.

Density matters more than individual instances. See `calibration.md`.

---

## 2A. LLM-favored verbs

These are the verbs models reach for first. They sound active and serious without committing to a specific action. Most can be swapped for a one-syllable Anglo-Saxon verb that does the same work with less smell.

| Word/Phrase | Why it's a tell | Replacement | Severity |
|---|---|---|---|
| delve / delve into | "Delves" appeared 6,697%+ more in 2024 PubMed vs 2020 — the flagship AI verb | look at, get into, study | H |
| leverage | Corporate cliche; appears in every blacklist | use | H |
| harness | Rare in human prose, ubiquitous in AI | use, channel | H |
| foster | Corporate-NGO speak | encourage, build | H |
| empower | Marketing fluff | help, give X to | H |
| unlock | "Unlock the potential of" is a top-10 GPT phrase | reveal, find | H |
| elevate | Empty intensifier | raise, lift, improve | H |
| streamline | McKinsey-speak | simplify, cut | H |
| revolutionize | Hyperbole baseline | change | H |
| transform | Same | change, rebuild | H |
| underscore / underscores | 904% spike post-ChatGPT (PubMed study) | show, prove | H |
| illuminate | Decorative academic | clarify, show | H |
| navigate | "Navigate the complexities of" — top-10 cliche | handle, manage, work through | H |
| garner | Spike-word in academic writing studies | get, win, attract | H |
| utilize | Sounds smart, means "use" | use | H |
| facilitate | Same | help | H |
| optimize | Tech-jargon default | improve, tune | H |
| enhance | Generic intensifier verb | improve, sharpen | H |
| embark / embark on | "Embark on a journey" is iconic AI | start | H |
| showcase / showcasing | 9.2x more frequent in AI than human (GPTZero) | show, display | H |
| boast / boasts | Wikipedia-flagged copula avoidance | has | H |
| demystify | LinkedIn cliche | explain | M |
| ignite | Copy-cliche | start, spark | M |
| supercharge | Marketing-speak | speed up | M |
| unleash | Same | release | M |
| unveil | Press-release verb | reveal, show | M |
| explore | Used to fill space ("we'll explore") | look at, go through | M |
| dive into | "Let's dive into" — sycophant cluster | start, look at | H |
| resonate / resonates | Vague impact-word | match, connect | M |
| reverberate | Even more decorative | echo | M |
| transcend / transcends | Often "transcends mere X" | go beyond | M |
| spearhead | Press-release cliche | lead | M |
| reimagine | Tech-deck cliche | redesign | M |
| craft | Overused as a verb | make, write | L |
| pave the way | Cliche metaphor | enable, set up | H |
| shed light on | Cliche | explain, show | H |

**Audit instruction:** any H-tier verb is a hit. For M-tier, replace and re-read; if the sentence is unchanged or sharper, the verb was AI smell. Cut.

---

## 2B. Cliché metaphors and grandiose nouns

These nouns convert a small subject into an epic one. AI defaults to them because metaphor scores well in training data; humans use them sparingly because they sound like a press release.

| Word/Phrase | Why it's a tell | Replacement | Severity |
|---|---|---|---|
| tapestry | Iconic AI metaphor | mix, weave (sparingly), or specific noun | H |
| landscape | "The landscape of X" — top cliche | field, market, world | H |
| realm | Decorative for "area" | area, field | H |
| beacon | "A beacon of X" | example, leader | H |
| treasure trove | Always cut | collection, source | H |
| symphony | Pretentious metaphor | combination, mix | H |
| journey | Especially "embark on a journey" | path, process | H |
| roadmap | Tech-deck cliche | plan, steps | M |
| ecosystem | Tech-cliche for "industry" | industry, network | M |
| paradigm / paradigm shift | Overused | change, shift | H |
| testament | "A testament to" | proof, evidence | H |
| cornerstone | Cliche | basis, anchor | M |
| crucible | Decorative | test, trial | M |
| labyrinth | Decorative | maze, complexity | M |
| metropolis | Travel-guide cliche | city | M |
| enigma | Decorative | mystery, puzzle | M |
| myriad / a myriad of | Inflated "many" | many, lots of | H |
| plethora | Same | lots of, too many | H |
| kaleidoscope | Decorative metaphor | mix, range | M |
| arena | Cliche metaphor | field | M |
| arsenal | Cliche metaphor | toolkit | M |

**Audit instruction:** if you find one of these, ask whether the sentence needs a metaphor at all. Most don't. When the answer is yes, pick a domain-specific image — the model defaulted to the most-trained metaphor; you can do better.

---

## 2C. Empty intensifiers / hedges / vague adjectives

The biggest category by far. These adjectives are all reach and no grip — they assert importance without earning it. Density is what makes them lethal: one "crucial" survives; three in a paragraph guarantees AI.

| Word/Phrase | Why it's a tell | Replacement | Severity |
|---|---|---|---|
| crucial | Top-3 spike word | important, key, or cut | H |
| essential | Same | needed, central | H |
| vital | Same | needed | H |
| pivotal | Same | key, decisive | H |
| paramount | Even more inflated | most important | H |
| profound | "A profound impact" | big, deep | M |
| robust | Tech-cliche | strong, reliable | H |
| seamless | Tech-cliche | smooth | H |
| comprehensive | Used to inflate completeness | full, complete | H |
| holistic | Buzz-word | whole, full | M |
| multifaceted | Always inflated | complex, many-sided | H |
| nuanced | Used as a flex | complex, subtle | M |
| intricate / intricacies | 611% spike post-ChatGPT | complex, detail | H |
| meticulous / meticulously | Top spike word | careful | H |
| compelling | Marketing-cliche | strong, persuasive | M |
| commendable | Pretentious | good, deserving praise | M |
| insightful | Often empty praise | useful, sharp | M |
| invaluable | Hyperbole | useful, important | M |
| unwavering | Always inflated | steady, firm | H |
| transformative | Always inflated | major | H |
| groundbreaking | Always inflated | new, original | H |
| cutting-edge | Cliche | new, current | H |
| state-of-the-art | Same | new, top | H |
| game-changer / game-changing | Cliche | big change | H |
| next-generation | Tech-cliche | new | M |
| future-proof | Tech-cliche | lasting | M |
| dynamic | Vague intensifier | active, fast-changing | M |
| vibrant | Travel-guide cliche | lively, busy | M |
| bustling | Same | busy | M |
| daunting | Cliche | hard, intimidating | M |
| ever-evolving / ever-changing | "In the ever-evolving landscape" | changing, shifting | H |
| ever-expanding | Same family | growing | M |
| timeless | Inflated cliche | lasting | M |
| enduring | Often empty | lasting | M |
| diverse / diverse array of | Empty filler | mixed, varied | M |
| unique blend | Marketing cliche | mix | M |
| fast-paced | "In today's fast-paced..." 107x AI | fast, busy | H |
| hyper-connected | Cliche | connected | M |
| modern / today's | Often filler | now, current | L |

**Audit instruction:** for each instance, try deleting it. If the sentence is fine or stronger without the word, it was filler. If a replacement is needed, prefer the shortest, most concrete word in the column.

---

## 2D. Sycophantic openers / closers

Direct RLHF artifacts. Every one of these is a model performing helpfulness instead of being helpful. Even when they leak into prose meant for publication, they read as machine-trained politeness.

| Phrase | Why it's a tell | Replacement | Severity |
|---|---|---|---|
| Great question! | RLHF flattery | delete | H |
| Excellent question! | Same | delete | H |
| I'd be happy to help | Same | delete and answer | H |
| Absolutely! | Opener flattery | delete | H |
| Certainly! | Same | delete | H |
| Of course! | Same | delete | H |
| Sure! Here's... | Same | delete the opener, keep "Here's" if needed | H |
| I hope this helps! | Closing flattery | delete | H |
| Let me know if you have any questions | Same | delete | H |
| Feel free to reach out | Same | delete | H |
| Don't hesitate to ask | Same | delete | H |
| Is there anything else I can help you with? | Same | delete | H |
| I hope this answers your question | Same | delete | H |
| Happy to clarify | Same | delete | H |
| Let me know if you'd like me to elaborate | Same | delete | H |

**Audit instruction:** every instance is a high-severity violation. Cut without exception. End on the last load-bearing sentence; openers go in the trash.

---

## 2E. Vague-authority phrases

Wikipedia's number-one content-pattern flag. These phrases assert evidence without citing any. AI defaults to them when it lacks specifics; humans either name a source or admit they're guessing.

| Phrase | Why it's a tell | Replacement | Severity |
|---|---|---|---|
| Studies show | Uncited authority claim | name the study or cut | H |
| Research suggests | Same | name the research or cut | H |
| Many experts agree | Same | name the experts or cut | H |
| Industry reports indicate | Same | name the report or cut | H |
| It is widely understood | Wikipedia-flagged weasel | cut or attribute | H |
| Observers have noted | Anonymous authority | name the observer or cut | H |
| Some critics argue | Same | name the critic or cut | H |
| Generally speaking | Hedge filler | cut | M |
| In many cases | Hedge filler | cut or specify | M |
| It is commonly known | Weasel + filler | cut | M |

**Audit instruction:** for each hit, either supply the citation (link, name, source) or cut the claim. "I think" beats "experts say" every time.

---

## 2F. Closing / connector clichés

The signposting words. AI was trained on five-paragraph essays and op-eds; it defaults to scaffolding even in short pieces. Real prose flows; it doesn't announce its turns.

| Phrase | Why it's a tell | Replacement | Severity |
|---|---|---|---|
| In conclusion | Compulsive summary | cut | H |
| To conclude | Same | cut | H |
| In summary | Same | cut | H |
| To summarize | Same | cut | H |
| Overall | Same | cut | H |
| Ultimately | Filler closer | cut | M |
| All things considered | Same | cut | M |
| At the end of the day | Filler | cut | H |
| In essence | Restatement | cut | H |
| To put it simply | Restatement | cut | H |
| In a nutshell | Same | cut | M |
| Furthermore | Stock connector | period or "Also" | H |
| Moreover | Same | period or "Also" | H |
| Additionally | Same | period or "Also" | H |
| First and foremost | Listicle cliche | "First" or cut | H |
| Last but not least | Listicle cliche | "Finally" or cut | H |
| On the other hand | Stock contrast | "But" | M |
| That being said | Stock contrast | "Still" or cut | M |
| With that in mind | Filler transition | cut | M |
| Notably | Throat-clearing | cut | M |
| Indeed | Filler | cut | M |

**Audit instruction:** most of these are deletable. End sentences with periods, not signposts. If a transition is genuinely needed, "But" / "Also" / "Still" carry their weight without smelling AI.

---

## 2G. Academically-validated spike words

These are the highest-confidence subset in the entire vocabulary list. Each one is statistically validated against pre-2022 baselines via published research — the spike is direct evidence that LLMs caused the surge in usage.

| Word/Phrase | Spike data | Source |
|---|---|---|
| delves | 6,697% increase 2020 to 2024 | [arXiv](https://arxiv.org/html/2406.07016v1) |
| underscores | 904% increase | [arXiv](https://arxiv.org/html/2406.07016v1) |
| intricate | 611% increase | [arXiv](https://arxiv.org/html/2406.07016v1) |
| showcasing | r=9.2 ratio AI vs human | [arXiv](https://arxiv.org/html/2406.07016v1) |
| meticulous, meticulously | spike-confirmed | [PubMed](https://www.medrxiv.org/content/10.1101/2024.05.14.24307373v2.full) |
| pivotal | spike-confirmed | [PubMed](https://www.medrxiv.org/content/10.1101/2024.05.14.24307373v2.full) |
| commendable | spike-confirmed | [PubMed](https://www.medrxiv.org/content/10.1101/2024.05.14.24307373v2.full) |
| garnered | top-21 focal word | [arXiv 2412.11385](https://arxiv.org/html/2412.11385v1) |
| boasts | top-21 focal word | [arXiv 2412.11385](https://arxiv.org/html/2412.11385v1) |
| groundbreaking | top-21 focal word | [arXiv 2412.11385](https://arxiv.org/html/2412.11385v1) |
| advancements | top-21 focal word | [arXiv 2412.11385](https://arxiv.org/html/2412.11385v1) |
| aligns / aligns with | 16x more frequent in AI | [GPTZero](https://gptzero.me/news/most-common-ai-vocabulary/) |
| surpassing | 12x more frequent in AI | [GPTZero](https://gptzero.me/news/most-common-ai-vocabulary/) |
| impacting | 11x more frequent in AI | [GPTZero](https://gptzero.me/news/most-common-ai-vocabulary/) |
| play a significant role in shaping | 182x more frequent in AI | [GPTZero](https://gptzero.me/news/most-common-ai-vocabulary/) |
| today's fast-paced world | 107x more frequent in AI | [GPTZero](https://gptzero.me/news/most-common-ai-vocabulary/) |
| notable works include | 120x more frequent in AI | [GPTZero](https://gptzero.me/news/most-common-ai-vocabulary/) |
| aims to explore | 50x more frequent in AI | [GPTZero](https://gptzero.me/news/most-common-ai-vocabulary/) |
| objective study aimed | 269x more frequent in AI | [Atlas](https://www.atlas.org/blog/artificial-intelligence/top-10-cliches-in-ai-generated-text) |
| research needed to understand | 235x more frequent in AI | [Atlas](https://www.atlas.org/blog/artificial-intelligence/top-10-cliches-in-ai-generated-text) |

A 2024 PubMed study estimated **at least 13.5% of 2024 biomedical abstracts were processed with LLMs** based on this excess vocabulary. After viral attention in early 2024, "delve" frequency in arXiv abstracts dropped sharply — confirming the words function as a fingerprint authors can sand off.

**Audit instruction:** any hit in this category is a near-certain AI marker. The data is statistical, not stylistic — these aren't bad words because they sound bad, they're bad because their frequency proves recent LLM authorship. Cut without exception.

---

## How to use this list

1. Run the scanner first — `scripts/scan.py` flags every instance mechanically across all categories.
2. Walk the always-cut items (Severity H) — each hit is a high-severity violation. Cut without exception.
3. Walk the often-cut items (Severity M) — apply judgment. Default is to cut; keep only if doing specific work.
4. Note the context-dependent items (Severity L) — these flag stylistic register but don't down-score the verdict.
5. The list isn't exhaustive. New LLM tells emerge over time. If a phrase reads as engineered, it probably is. The default action is to cut.

The 2G category (academically-validated spike words) is the highest-confidence subset — these are statistically validated against pre-2022 baselines via published research.
