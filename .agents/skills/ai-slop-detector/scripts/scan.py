#!/usr/bin/env python3
"""
scan.py - Universal AI-slop + Comprehension scanner (slop-cop, dual axis).

Scans prose on two parallel axes:

1. AI-Slop axis — ~45 rhetorical patterns, ~150 vocabulary tells, ~33 formatting
   tells. Density score, burstiness, model fingerprint.
2. Comprehension axis — ~17 mechanically-detectable comprehension patterns plus
   8 readability metrics (Flesch RE, FK Grade, SMOG, Coleman-Liau, Dale-Chall,
   lexical density, sentence length variance, passive %).

Catches what regex can; qualitative patterns (anaphora, symmetry, real-vs-
decorative judgment, missing thesis, curse of knowledge) require reading.

Usage:
    python3 scan.py path/to/draft.md
    python3 scan.py --json path/to/draft.md
    python3 scan.py --quick path/to/draft.md
    python3 scan.py --genre academic path/to/draft.md
    python3 scan.py --audience marketing path/to/draft.md
    python3 scan.py --strict-em-dash path/to/draft.md
    cat draft.md | python3 scan.py
    echo "draft text" | python3 scan.py
"""
import argparse
import json
import math
import re
import sys
from pathlib import Path

# =============================================================================
# VOCABULARY — every item from references/vocabulary.md
# Severity: H (always cut) / M (often cut) / L (context-dependent)
# =============================================================================

# 2A. LLM-favored verbs
VERBS_H = [
    "delve into", "delves", "delved", "delve",
    "leverage", "leverages", "leveraged", "leveraging",
    "harness", "harnesses", "harnessed", "harnessing",
    "foster", "fosters", "fostered", "fostering",
    "empower", "empowers", "empowered", "empowering",
    "unlock", "unlocks", "unlocked", "unlocking",
    "elevate", "elevates", "elevated", "elevating",
    "streamline", "streamlines", "streamlined", "streamlining",
    "revolutionize", "revolutionizes", "revolutionized", "revolutionizing",
    "underscore", "underscores", "underscored", "underscoring",
    "illuminate", "illuminates", "illuminated", "illuminating",
    "navigate the", "navigates the", "navigated the", "navigating the",
    "garner", "garners", "garnered", "garnering",
    "utilize", "utilizes", "utilized", "utilizing",
    "facilitate", "facilitates", "facilitated", "facilitating",
    "embark on", "embarks on", "embarked on", "embarking on",
    "showcase", "showcases", "showcased", "showcasing",
    "boast", "boasts", "boasted", "boasting",
    "dive into", "dives into", "dove into", "diving into",
    "pave the way", "pave the way for", "paves the way",
    "shed light on", "sheds light on",
    "transform the", "transforms the", "transforming the",
]
VERBS_M = [
    "demystify", "demystifies", "demystified", "demystifying",
    "ignite", "ignites", "ignited", "igniting",
    "supercharge", "supercharges", "supercharged",
    "unleash", "unleashes", "unleashed", "unleashing",
    "unveil", "unveils", "unveiled", "unveiling",
    "resonate", "resonates", "resonated", "resonating",
    "transcend", "transcends", "transcended", "transcending",
    "spearhead", "spearheads", "spearheaded", "spearheading",
    "reimagine", "reimagines", "reimagined", "reimagining",
    "reverberate", "reverberates", "reverberated",
]

# 2B. Cliché metaphors and grandiose nouns
NOUNS_H = [
    "tapestry",
    "treasure trove",
    "symphony of",
    "embark on a journey",
    "beacon of",
    "myriad of",
    "plethora",
    "paradigm shift",
    "testament to",
    "arsenal of",
    "ecosystem of",
]
NOUNS_M = [
    "landscape of",
    "realm of",
    "journey of",
    "roadmap",
    "cornerstone of",
    "crucible",
    "labyrinth",
    "metropolis",
    "enigma",
    "kaleidoscope",
    "arena of",
]

# 2C. Empty intensifiers, hedges, vague adjectives
INTENSIFIERS_H = [
    "crucial",
    "essential",
    "vital",
    "pivotal",
    "paramount",
    "robust",
    "seamless",
    "comprehensive",
    "multifaceted",
    "intricate", "intricacies",
    "meticulous", "meticulously",
    "unwavering",
    "transformative",
    "groundbreaking",
    "cutting-edge",
    "state-of-the-art",
    "game-changer", "game-changing",
    "ever-evolving", "ever-changing",
    "fast-paced",
]
INTENSIFIERS_M = [
    "profound",
    "holistic",
    "nuanced",
    "compelling",
    "commendable",
    "insightful",
    "invaluable",
    "next-generation",
    "future-proof",
    "dynamic",
    "vibrant",
    "bustling",
    "daunting",
    "ever-expanding",
    "timeless",
    "enduring",
    "diverse array",
    "unique blend",
    "hyper-connected",
]

# 2D. Sycophantic openers / closers
SYCOPHANCY_OPEN_H = [
    r"\bGreat question[!.]",
    r"\bExcellent question[!.]",
    r"\bExcellent point[!.]",
    r"\bAbsolutely[!.]",
    r"\bCertainly[!.]",
    r"\bOf course[!.]",
    r"\bSure[!,]\s+Here'?s",
    r"\bI'?d be happy to help",
    r"\bWhat a (?:great|wonderful|fantastic) (?:question|idea)",
]
SYCOPHANCY_CLOSE_H = [
    r"\bI hope this helps",
    r"\bLet me know if you have any questions",
    r"\bLet me know if you'?d like me to (?:elaborate|continue|expand)",
    r"\bFeel free to reach out",
    r"\bDon'?t hesitate to (?:ask|reach out)",
    r"\bIs there anything else I can help you with",
    r"\bI hope this answers your question",
    r"\bHappy to clarify",
]

# 2E. Vague-authority weasel attribution
VAGUE_AUTH_H = [
    r"\bStudies show\b",
    r"\bResearch suggests\b",
    r"\bResearch indicates\b",
    r"\bMany experts (?:agree|believe)\b",
    r"\bIndustry reports indicate\b",
    r"\bIt is widely understood\b",
    r"\bIt'?s widely (?:believed|understood)\b",
    r"\bObservers have noted\b",
    r"\bSome critics argue\b",
]
VAGUE_AUTH_M = [
    r"\bGenerally speaking\b",
    r"\bIn many cases\b",
    r"\bIt is commonly (?:known|believed)\b",
]

# 2F. Closing / connector clichés
CONNECTORS_H = [
    "in conclusion",
    "to conclude",
    "in summary",
    "to summarize",
    "at the end of the day",
    "in essence",
    "to put it simply",
    "furthermore",
    "moreover",
    "additionally",
    "first and foremost",
    "last but not least",
]
CONNECTORS_M = [
    "overall",
    "ultimately",
    "all things considered",
    "in a nutshell",
    "on the other hand",
    "that being said",
    "with that in mind",
    "notably",
    "indeed",
]

# Decorative / "magic" adverbs (low+ severity)
MAGIC_ADVERBS = [
    "genuinely",
    "actually",
    "truly",
    "really",
    "honestly",
    "frankly",
    "ultimately",
    "basically",
    "obviously",
    "clearly",
    "simply",
    "literally",
    "fundamentally",
    "remarkably",
    "arguably",
    "deeply",
    "quietly",
    "subtly",
]

# Buzzwords for density check (3+ in one paragraph = flag)
BUZZWORDS = [
    "scalable",
    "repeatable",
    "defensible",
    "mission-critical",
    "enterprise-grade",
    "world-class",
    "best-in-class",
    "ai-native",
    "agent-driven",
    "autonomous",
    "high-velocity",
    "outcome-oriented",
    "robust",
    "seamless",
    "innovative",
    "cutting-edge",
    "state-of-the-art",
    "synergy",
    "holistic",
    "next-generation",
    "transformative",
    "groundbreaking",
    "comprehensive",
    "multifaceted",
]

# =============================================================================
# PATTERNS — sentence-level and structural
# =============================================================================

# 1. Negation reversal openers
NEGATION_OPENERS = [
    r"^\s*It wasn'?t\b",
    r"^\s*It was not\b",
    r"^\s*It'?s not\b",
    r"^\s*It is not\b",
    r"^\s*This isn'?t\b",
    r"^\s*This is not\b",
    r"^\s*Not just\b",
    r"^\s*Not a\b",
    r"^\s*Not because\b",
]

# 2. Dramatic countdown — "Not X. Not Y. Just Z."
# Detected via consecutive short sentences starting with "Not"

# 3. Self-posed rhetorical question + immediate answer
# "The result? X." "The catch? Y."
RHETORICAL_QA = re.compile(
    r"\b(The result|The catch|The kicker|The thing|The point|The bottom line|The real question)\?\s+\w",
    re.IGNORECASE,
)

# 8. Performative opening patterns
PERFORMATIVE_OPENINGS = [
    r"^\s*Let me cut to it[:\.]",
    r"^\s*Picture this[:\.]?",
    r"^\s*Imagine a world",
    r"^\s*In a world where",
    r"^\s*Have you ever wondered",
    r"^\s*Are you struggling with",
    r"^\s*In today'?s fast-paced",
    r"^\s*In today'?s (?:world|landscape|digital age)",
    r"^\s*Here'?s the thing\b",
    r"^\s*I'?ll be brief",
    r"^\s*When I read\b.*I closed",
    r"^\s*Most\s+\w+\s+\w+\s+(?:waste|won'?t)",
]

# 9. Setup-reveal phrases
SETUP_REVEAL_PHRASES = [
    r"\bThe point is\b",
    r"\bThe thing is\b",
    r"\bWhat this means is\b",
    r"\bIn short\b",
    r"\bBottom line\b",
    r"\bThe bottom line\b",
    r"\bIn summary\b",
    r"\bTo summarize\b",
    r"\bThe real takeaway\b",
    r"\bWhat matters here\b",
]

# 10. Crafted closer indicators
CRAFTED_CLOSERS = [
    r"^Build it\.?\s+Ship it\.?\s+Run it\.?$",
    r"^Let'?s go\.?$",
    r"^The future is now\.?$",
    r"^The future belongs to\b",
    r"^And that'?s the point\.?$",
]

# 13. Present-participle "-ing" tails
ING_TAIL = re.compile(
    r",\s+(highlighting|emphasizing|symbolizing|contributing to|reflecting|"
    r"underscoring|demonstrating|showcasing|embodying|representing|reinforcing|"
    r"signaling|illustrating|exemplifying|marking|paving|fostering)\s+",
    re.IGNORECASE,
)

# 14. False range "From X to Y"
FALSE_RANGE = re.compile(
    r"(?:^|\.\s+|:\s+)From\s+\w+(?:\s+\w+){0,3}\s+to\s+\w+(?:\s+\w+){0,3}[,.]",
    re.IGNORECASE,
)

# 15. Copula avoidance verbs
COPULA_AVOIDANCE = [
    r"\bserves as (?:a|an|the)\b",
    r"\bstands as (?:a|an|the)\b",
    r"\bmarks (?:a|an|the)\b",
    r"\brepresents (?:a|an|the)\b",
    r"\bembodies\b",
]

# 16. Hedge stacking — clusters of hedges in one sentence
HEDGE_WORDS = [
    r"\bmay\b", r"\bmight\b", r"\bcould\b", r"\bpossibly\b", r"\bpotentially\b",
    r"\bperhaps\b", r"\bgenerally\b", r"\bsomewhat\b", r"\bprobably\b",
    r"\bin many cases\b", r"\bit'?s possible that\b",
]

# 17. Hedged superlatives
HEDGED_SUPERLATIVES = [
    r"\bperhaps the most\b",
    r"\barguably the (?:best|most|greatest)\b",
    r"\bone of the most\b",
    r"\bamong the most\b",
    r"\bquite possibly the\b",
]

# 18. "While X, Y" sentence opener
WHILE_OPENER = re.compile(r"^\s*While\s+\w+", re.IGNORECASE | re.MULTILINE)

# 19. "X meets Y" / "X is more than just Y"
X_MEETS_Y = re.compile(r"\b\w+\s+meets\s+\w+\b", re.IGNORECASE)
MORE_THAN_JUST = re.compile(r"\bmore than just\s+(?:a|an)?\s*\w+", re.IGNORECASE)

# 21. False concession openers
FALSE_CONCESSION = [
    r"^\s*Despite (?:its |the |these )?(?:challenges|limitations|drawbacks)",
    r"^\s*While (?:there are|the evidence is|some)\s+\w+\s+(?:limitations|concerns|challenges)",
    r"^\s*Although (?:there are|some)\s+",
]

# 26. Pedagogical voice
PEDAGOGICAL = [
    r"^\s*Let'?s dive into\b",
    r"^\s*Let'?s explore\b",
    r"^\s*Let'?s break (?:this|it) down\b",
    r"^\s*We'?ll walk through\b",
    r"^\s*Let'?s unpack\b",
]

# 27. Royal-we / "as a society" framing
ROYAL_WE = [
    r"\bWe live in (?:an? |the )?(?:age|era|world)\b",
    r"\bAs a society,? we\b",
    r"\bIn our (?:time|age|world)\b",
    r"\bOur collective\b",
]

# 29. Knowledge-cutoff disclaimer leakage
KNOWLEDGE_CUTOFF = [
    r"\bAs of my (?:last update|knowledge cutoff)\b",
    r"\bI don'?t have access to real-time\b",
    r"\bMy training data\b",
    r"\bWhile my training\b",
    r"\bbased on (?:my|the) training data\b",
]

# 31. Stake inflation / future-flourish
STAKE_INFLATION = [
    r"\bThis will revolutionize\b",
    r"\bWe'?re entering (?:a|the) new era\b",
    r"\bA new paradigm\b",
    r"\bThe future of\b.*\bis\b",
    r"\bUshering in (?:a|the) new\b",
]

# 32. Grandiose framing
GRANDIOSE = [
    r"\bstands as (?:a|an|the)\b",
    r"\bserves as (?:a|an|the)\b",
    r"\b(?:a|the) testament to\b",
    r"\bAt its core,?\s+(?:this|the|it)\b",
    r"\bembodies (?:the|a) spirit\b",
    r"\brepresents (?:a|an|the)\s+\w+\s+(?:moment|era|chapter)",
]

# 36. Fabricated case study / generic name
FABRICATED_CASE = re.compile(
    r"\b(?:Take|Meet|Consider)\s+([A-Z][a-z]{2,10})(?:\s+[A-Z][a-z]+)?,\s+(?:a|an)\s+",
)

# 41. Throat-clearing meta-comments
THROAT_CLEARING = [
    r"\bIt'?s worth noting (?:that)?\b",
    r"\bIt'?s important to (?:mention|note)\b",
    r"\bIt bears (?:mentioning|noting)\b",
    r"^\s*Notably,\s",
    r"^\s*Interestingly,\s",
]

# Whether-or openers (12)
WHETHER_OR = re.compile(r"^\s*Whether you'?re\s+", re.IGNORECASE | re.MULTILINE)

# 20. Both-sides-ism — on one hand / on the other hand
BOTH_SIDES = [
    r"\bon (?:the )?one hand\b",
    r"\bon the other hand\b",
    r"\bboth (?:sides|perspectives) have merit\b",
    r"\badvantages and disadvantages\b",
]

# 22. The "real" tic — "real X" as an authenticity intensifier
REAL_TIC = re.compile(
    r"\breal\s+(?:money|stakes|outcomes|connection|impact|results|deal|talk|research|world)\b",
    re.IGNORECASE,
)

# 34. Vapid analogies — "Think of it as a", "It's like having a"
VAPID_ANALOGY = [
    r"\bThink of it as (?:a |an |the )",
    r"\bIt'?s like having (?:a |an )",
    r"\bImagine it as (?:a |an )",
    r"\bIt'?s the (?:Uber|Airbnb|Spotify|Netflix) of\b",
]

# 39. Historical analogy stacking — printing press / electricity / internet within ~150 chars
HISTORICAL_ANALOGY = re.compile(
    r"\b(?:printing press|electricity|internet|industrial revolution|wheel|fire|atomic age)\b",
    re.IGNORECASE,
)

# 38. Dead-metaphor repetition — count cliché metaphor reuse
DEAD_METAPHORS = ["journey", "landscape", "tapestry", "ecosystem", "realm", "beacon", "symphony", "tide"]

# =============================================================================
# MODEL FINGERPRINT MARKERS
# =============================================================================

GPT_MARKERS = [
    r"\bdelve(?:s|d)?\b", r"\bunderscore(?:s|d)?\b", r"\bnoteworthy\b",
    r"\bcommendable\b", r"\bintricate\b", r"\bmeticulous(?:ly)?\b",
    r"\bsupercharge\b", r"\bunleash(?:es|ed)?\b", r"\bdive in\b",
    r"\bgame-changing\b", r"\bindividuals with\b",
    r"\bcharacterized by elevated\b", r"\bplay a significant role\b",
]
CLAUDE_MARKERS = [
    r"\bmeaningfully\b", r"\bthe distinction is worth examining\b",
    r"\bI notice that\b", r"\bit'?s worth examining\b",
    r"\bI should be careful here\b", r"\bworth noting that\b",
    r"\bmore carefully\b",
]
GEMINI_MARKERS = [
    r"\bthe way for\b", r"\bthe cascade of\b", r"\bin the world of\b",
    r"\blet'?s explore\b", r"\bunderstand how\b",
    r"\blet'?s take a closer look\b",
]

# =============================================================================
# COMPREHENSION AXIS — patterns and constants
# Sourced from references/comprehension.md and readability-metrics.md.
# =============================================================================

# F1. Known-acronym allowlist (~50 well-known across domains).
# Anything outside this list counts as "undefined" unless introduced with
# a parenthetical expansion earlier in the document, e.g. "search request agent (SRA)".
KNOWN_ACRONYMS = {
    # Tech / web
    "USB", "FAQ", "URL", "API", "JSON", "HTML", "CSS", "SQL", "AWS", "GCP",
    "PDF", "GIF", "JPG", "PNG", "MP3", "MP4", "HTTP", "HTTPS", "IP", "DNS",
    "GPS", "VPN", "RAM", "CPU", "GPU", "SSD", "HDD", "OS", "IOS", "AI",
    "ML", "LLM", "UI", "UX", "SDK", "CLI", "GUI", "CDN", "DOM", "XML",
    "IDE", "REST", "RPC", "TLS", "SSL", "FTP", "SMTP", "IMAP",
    # Business
    "CEO", "CFO", "CTO", "COO", "CMO", "VP", "HR", "PR", "QA", "ROI",
    "KPI", "CRM", "ERP", "SaaS", "PaaS", "IaaS", "B2B", "B2C", "B2G",
    "MVP", "OKR", "PMF", "ICP", "MRR", "ARR", "LTV", "CAC", "NPS",
    # Government / countries / agencies
    "USA", "UK", "EU", "UN", "NATO", "NASA", "FBI", "CIA", "IRS", "DMV",
    "DOJ", "DOD", "FDA", "EPA", "CDC", "WHO", "OECD", "IMF",
    # Time / measurement
    "AM", "PM", "GMT", "UTC", "EST", "PST", "BC", "AD", "CE", "BCE",
    # Media / docs
    "TV", "FM", "AM", "DVD", "CD", "VHS",
    # Common short
    "OK", "ID", "TLDR", "FYI", "ASAP", "DIY", "RSVP", "AKA", "ETA", "ETC",
    "CV", "LLC",
    # Legacy abbrev set (from existing ABBREVIATIONS)
    "MR", "MRS", "MS", "DR", "PROF", "SR", "JR",
    # Misc common
    "PIN", "ATM", "ZIP", "CAPTCHA", "GDPR", "CCPA", "PCI",
}

# Audience presets that affect comprehension thresholds.
AUDIENCE_PRESETS = {
    "casual":      {"flesch_min": 60, "fk_max": 9,  "sent_max": 18, "passive_max": 10, "lex_max": 55},
    "marketing":   {"flesch_min": 65, "fk_max": 8,  "sent_max": 16, "passive_max": 5,  "lex_max": 50},
    "academic":    {"flesch_min": 30, "fk_max": 16, "sent_max": 28, "passive_max": 20, "lex_max": 65},
    "encyclopedic":{"flesch_min": 40, "fk_max": 14, "sent_max": 24, "passive_max": 15, "lex_max": 60},
    "technical":   {"flesch_min": 40, "fk_max": 14, "sent_max": 25, "passive_max": 15, "lex_max": 60},
    "fiction":     {"flesch_min": 60, "fk_max": 10, "sent_max": 22, "passive_max": 12, "lex_max": 55},
    "healthcare":  {"flesch_min": 70, "fk_max": 8,  "sent_max": 15, "passive_max": 5,  "lex_max": 50},
}

# G5. Glue-word bloat — sentence-start patterns that delay the real subject
GLUE_WORD_OPENERS = [
    r"^\s*There\s+(?:is|are|was|were)\b",
    r"^\s*It\s+is\b",
    r"^\s*It\s+was\b",
    r"^\s*What\s+is\b",
    r"^\s*What\s+I'?m\s+trying\s+to\s+say\s+is\b",
    r"^\s*What\s+I\s+mean\s+is\b",
    r"^\s*The\s+thing\s+is\b",
]

# H5. Forward-reference / "we'll see later"
FORWARD_REFERENCE = [
    r"\bas we'?ll see\b",
    r"\bmore on this later\b",
    r"\bcovered below\b",
    r"\bwe'?ll discuss\b",
    r"\bas discussed below\b",
    r"\bsee section \d+\b",
    r"\bsee below\b",
    r"\bdetailed (?:later|below)\b",
    r"\bin a later (?:section|chapter)\b",
]

# J1. Passive voice — be-verb + past participle
PASSIVE_VOICE = re.compile(
    r"\b(is|are|was|were|been|being|am)\s+(?:[a-z]+ly\s+)?"
    r"(?:[a-z]+ed|known|made|done|seen|given|taken|written|sent|shown|"
    r"found|left|kept|paid|met|read|put|set|cut|hit|lost|won|brought|"
    r"caught|chosen|driven|spoken|stolen|broken|thrown|drawn|drunk|"
    r"swum|sworn|torn|worn|sung|sunk|run|begun|come|become|gone|done|"
    r"borne|built|burnt|spent|sent|bent|lent|meant|kept|slept|wept|"
    r"crept|swept|felt|dealt|spilt|spoilt|told|sold|held|bound|wound)\b",
    re.IGNORECASE,
)

# J2. Nominalization / zombie noun suffixes
NOMINALIZATION_SUFFIXES = re.compile(
    r"\b\w{3,}(?:tion|ment|ance|ence|ity|ization|isation|ization|ism|ness)\b",
    re.IGNORECASE,
)

# J5. Decorative qualifiers (comprehension-axis version)
DECORATIVE_QUALIFIERS = re.compile(
    r"\b(very|really|quite|extremely|incredibly|just|literally|"
    r"basically|actually|simply|truly|highly|fairly|rather|somewhat)\b",
    re.IGNORECASE,
)

# J8. Negative-construction-where-positive-available
NEGATIVE_CONSTRUCTIONS = [
    r"\bnot\s+un[a-z]+\b",
    r"\bnot\s+in[a-z]+\b",
    r"\bnot\s+infrequent(?:ly)?\b",
    r"\bdon'?t\s+fail\s+to\b",
    r"\bnever\s+fail\s+to\b",
    r"\bnot\s+un\w+\b",
]

# Acronym-detector regex: 2-5 uppercase letters/digits, surrounded by word boundaries.
ACRONYM_TOKEN = re.compile(r"\b([A-Z][A-Z0-9]{1,4})\b")

# Parenthetical expansion regex — captures "Search Request Agent (SRA)" style introductions.
PAREN_EXPANSION = re.compile(r"\b(?:[A-Z][a-zA-Z]+\s+){1,5}\(([A-Z][A-Z0-9]{1,4})\)")

# Numeric-token regex for stat bombing (F3)
NUMERIC_TOKEN = re.compile(r"(?:\$\d+(?:\.\d+)?(?:[KkMmBb])?|\b\d+(?:\.\d+)?(?:%|[KkMmBb]|x|×)?\b)")

# Telegraphic colon-label regex (G1): "Word(s): Capital..." mid-sentence.
COLON_LABEL = re.compile(r"\b([A-Z][a-zA-Z]+(?:\s+[a-zA-Z]+){0,3}):\s+[A-Z]")

# Stoplist for lexical-density heuristic.
STOPWORDS = {
    "the", "a", "an", "of", "in", "on", "at", "to", "for", "with", "by",
    "and", "or", "but", "is", "are", "was", "were", "be", "been", "being",
    "am", "has", "have", "had", "do", "does", "did", "will", "would",
    "can", "could", "should", "may", "might", "must", "shall",
    "it", "its", "this", "that", "these", "those",
    "he", "she", "they", "we", "i", "you", "me", "him", "her", "them",
    "us", "my", "your", "his", "their", "our",
    "who", "what", "which", "where", "when", "why", "how",
    "as", "if", "then", "else", "than", "so", "because", "while", "though",
    "from", "into", "onto", "upon", "about", "over", "under", "again",
    "not", "no", "yes", "out", "up", "down", "off", "all", "any", "some",
    "each", "every", "other", "another", "such",
}

# Dale-Chall simplified word list — curated subset of ~500 of the most common
# English words. Source: Dale-Chall 3,000-word list, abridged for inline embedding.
DALE_CHALL_WORDLIST = {
    "a", "able", "about", "above", "across", "act", "add", "afraid", "after",
    "afternoon", "again", "against", "age", "ago", "agree", "ah", "ahead", "air",
    "alike", "all", "allow", "almost", "alone", "along", "already", "also", "always",
    "am", "among", "an", "and", "angry", "another", "answer", "any", "apart",
    "apple", "are", "arm", "around", "art", "as", "ask", "at", "ate", "away",
    "baby", "back", "bad", "bag", "ball", "band", "bank", "bar", "base", "be",
    "bear", "beat", "beautiful", "became", "because", "become", "bed", "been",
    "before", "began", "begin", "begun", "behind", "being", "believe", "bell",
    "below", "best", "better", "between", "big", "bird", "bit", "black", "blank",
    "blew", "block", "blow", "blue", "board", "boat", "body", "boil", "bone",
    "book", "born", "both", "bottle", "bottom", "bought", "box", "boy", "branch",
    "brave", "bread", "break", "breakfast", "breath", "brick", "bridge", "bright",
    "bring", "broke", "brother", "brown", "brought", "build", "built", "burn",
    "burst", "bury", "business", "busy", "but", "buy", "by", "cake", "call",
    "came", "can", "candy", "cap", "captain", "car", "card", "care", "carry",
    "case", "cast", "cat", "catch", "cause", "caught", "cell", "cent", "center",
    "chair", "chance", "change", "chase", "cheap", "check", "cheer", "child",
    "children", "chose", "circle", "city", "class", "clean", "clear", "climb",
    "close", "cloth", "clothes", "cloud", "club", "coal", "coat", "cold", "color",
    "come", "common", "company", "complete", "cook", "cool", "corn", "corner",
    "cost", "could", "country", "course", "cover", "cow", "crack", "cried",
    "cross", "cry", "cup", "cut", "dad", "daily", "dance", "danger", "dare",
    "dark", "date", "daughter", "day", "dead", "dear", "death", "decide", "deep",
    "deer", "did", "die", "different", "dig", "dinner", "dirt", "do", "dog",
    "done", "door", "down", "draw", "drawn", "dream", "dress", "drew", "drink",
    "drive", "drop", "drove", "dry", "duck", "dust", "each", "ear", "early",
    "earth", "east", "easy", "eat", "egg", "eight", "either", "else", "empty",
    "end", "enemy", "enjoy", "enough", "enter", "even", "evening", "ever",
    "every", "everybody", "everyone", "everything", "expect", "eye", "face",
    "fact", "fail", "fair", "fall", "false", "family", "far", "farm", "fast",
    "fat", "father", "fault", "favor", "fear", "feed", "feel", "feet", "fell",
    "felt", "few", "field", "fight", "fill", "find", "fine", "finish", "fire",
    "first", "fish", "fit", "five", "flag", "flat", "floor", "flow", "flower",
    "fly", "follow", "food", "foot", "for", "forget", "form", "forth", "forward",
    "fought", "found", "four", "free", "fresh", "friend", "from", "front",
    "fruit", "full", "fun", "funny", "game", "garden", "gate", "gave", "get",
    "gift", "girl", "give", "glad", "glass", "go", "goes", "going", "gold",
    "gone", "good", "got", "grade", "grand", "grass", "great", "green", "grew",
    "ground", "group", "grow", "guess", "had", "hair", "half", "hall", "hand",
    "happen", "happy", "hard", "has", "hat", "have", "head", "hear", "heart",
    "heat", "heavy", "held", "help", "her", "here", "hide", "high", "hill",
    "him", "his", "history", "hit", "hold", "hole", "home", "hope", "horse",
    "hot", "hour", "house", "how", "however", "huge", "hundred", "hung", "hunt",
    "hurry", "hurt", "i", "ice", "idea", "if", "ill", "important", "in",
    "inch", "indeed", "inside", "into", "is", "it", "its", "job", "join", "joy",
    "judge", "jump", "just", "keep", "kept", "kid", "kill", "kind", "king",
    "kiss", "kitchen", "knee", "knew", "know", "known", "lake", "land", "large",
    "last", "late", "laugh", "law", "lay", "lead", "learn", "least", "leave",
    "led", "left", "leg", "less", "let", "letter", "lie", "life", "lift",
    "light", "like", "line", "lion", "lip", "list", "listen", "little", "live",
    "lone", "long", "look", "lose", "lost", "lot", "love", "low", "luck", "made",
    "main", "make", "man", "many", "march", "mark", "may", "me", "mean", "meant",
    "meat", "meet", "men", "met", "mid", "middle", "might", "mile", "milk",
    "mill", "mind", "mine", "minute", "miss", "mix", "money", "month", "moon",
    "more", "morning", "most", "mother", "mountain", "mouse", "mouth", "move",
    "much", "must", "my", "name", "near", "neck", "need", "neighbor", "neither",
    "never", "new", "next", "nice", "night", "nine", "no", "none", "noise",
    "north", "nose", "not", "note", "nothing", "now", "nut", "of", "off",
    "office", "often", "oh", "old", "on", "once", "one", "only", "open", "or",
    "order", "other", "our", "out", "outside", "over", "own", "page", "paid",
    "pain", "paint", "pair", "paper", "part", "party", "pass", "past", "pay",
    "people", "perhaps", "person", "pick", "picture", "pie", "piece", "pig",
    "pink", "place", "plain", "plan", "plant", "play", "please", "point",
    "police", "pond", "poor", "post", "pot", "power", "press", "pretty", "price",
    "prince", "print", "promise", "prove", "pull", "push", "put", "queen",
    "question", "quick", "quiet", "quite", "rabbit", "race", "rain", "ran",
    "rather", "reach", "read", "ready", "real", "really", "reason", "red",
    "remember", "rest", "return", "rich", "ride", "right", "ring", "river",
    "road", "rock", "roll", "roof", "room", "rose", "round", "row", "rub",
    "run", "sad", "safe", "said", "same", "sang", "sat", "save", "saw", "say",
    "school", "sea", "seat", "second", "secret", "see", "seed", "seem", "seen",
    "self", "sell", "send", "sent", "serve", "set", "seven", "several", "shade",
    "shake", "shall", "shape", "share", "she", "sheep", "shelf", "shell", "shine",
    "ship", "shoe", "shoot", "shop", "shore", "short", "should", "show", "shut",
    "sick", "side", "sight", "sign", "silent", "silly", "silver", "since", "sing",
    "sister", "sit", "six", "size", "sky", "sleep", "slow", "small", "smell",
    "smile", "smoke", "snake", "snow", "so", "soap", "soft", "sold", "soldier",
    "some", "son", "song", "soon", "sound", "soup", "south", "speak", "spell",
    "spend", "spent", "spread", "spring", "stand", "star", "start", "state",
    "stay", "step", "stick", "still", "stone", "stop", "store", "story",
    "straight", "strange", "street", "string", "strong", "such", "sugar",
    "summer", "sun", "supper", "suppose", "sure", "surprise", "sweet", "swim",
    "table", "tail", "take", "talk", "tall", "taste", "teach", "team", "tear",
    "tell", "ten", "than", "thank", "that", "the", "their", "them", "then",
    "there", "these", "they", "thick", "thin", "thing", "think", "third",
    "this", "those", "though", "thought", "three", "threw", "throat", "through",
    "throw", "tie", "till", "time", "tin", "tiny", "tip", "tire", "to",
    "today", "toe", "told", "tomorrow", "tone", "too", "took", "top", "touch",
    "town", "track", "train", "tree", "trip", "true", "truly", "trust", "truth",
    "try", "turn", "twelve", "twenty", "two", "under", "until", "up", "upon",
    "us", "use", "used", "very", "view", "visit", "voice", "wait", "walk",
    "wall", "want", "war", "warm", "was", "wash", "watch", "water", "way",
    "we", "wear", "week", "weigh", "well", "went", "were", "west", "wet",
    "what", "wheel", "when", "where", "whether", "which", "while", "white",
    "who", "whole", "whose", "why", "wide", "wife", "wild", "will", "win",
    "wind", "winter", "wise", "wish", "with", "within", "without", "woke",
    "woman", "women", "wonder", "wood", "word", "wore", "work", "world",
    "worn", "worry", "would", "wound", "write", "written", "wrong", "wrote",
    "yard", "year", "yes", "yet", "you", "young", "your",
    # Plain modern additions outside the historic Dale-Chall list
    "online", "email", "phone", "mobile", "today", "okay", "list", "test",
    "try", "post", "blog", "page", "click", "type", "send", "free", "help",
    "user", "site", "data", "code", "team", "task",
}


# =============================================================================
# TEXT PROCESSING
# =============================================================================

ABBREVIATIONS = [
    "Mr.", "Mrs.", "Ms.", "Dr.", "Prof.", "Sr.", "Jr.",
    "U.S.", "U.K.", "E.U.", "i.e.", "e.g.", "etc.", "vs.", "Inc.", "Ltd.",
    "St.", "Ave.", "No.", "Vol.", "ch.", "ed.",
]


def strip_code_blocks(text):
    """Remove fenced code blocks and inline code from markdown."""
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"`[^`]+`", "", text)
    return text


def split_sentences(text):
    """Split text into sentences. Imperfect but good enough."""
    protected = text
    for ab in ABBREVIATIONS:
        protected = protected.replace(ab, ab.replace(".", "\x00"))
    sentences = re.split(r"(?<=[.!?])\s+", protected)
    sentences = [s.replace("\x00", ".").strip() for s in sentences if s.strip()]
    return sentences


def split_paragraphs(text):
    """Split text into paragraphs by blank lines.

    Also treats lone-blockquote-marker lines (just '>') as paragraph separators —
    common in pasted letter / quoted-text formats where the user uses '>' to
    delimit blocks.
    """
    # Treat lines that contain only ">" or whitespace+">" as blank
    text = re.sub(r"^\s*>\s*$", "", text, flags=re.MULTILINE)
    paras = re.split(r"\n\s*\n", text)
    return [p.strip() for p in paras if p.strip()]


def count_words(s):
    return len(re.findall(r"\b\w+\b", s))


def find_phrase_hits(text, phrases):
    """Return [(phrase, count), ...] for whole-word phrases (case-insensitive)."""
    hits = []
    for phrase in phrases:
        # Word boundaries around the phrase
        pattern = r"\b" + re.escape(phrase) + r"\b"
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        if matches:
            hits.append((phrase, len(matches)))
    return hits


def find_regex_hits(text, patterns):
    """Return [(pattern, count, sample), ...] for each pattern with matches."""
    hits = []
    for pat in patterns:
        matches = re.findall(pat, text, flags=re.IGNORECASE)
        if matches:
            sample = matches[0] if isinstance(matches[0], str) else str(matches[0])
            hits.append((pat, len(matches), sample[:80]))
    return hits


# =============================================================================
# DETECTORS
# =============================================================================

def find_em_dashes(text):
    em = text.count("—")
    en = text.count("–")
    double_hyphen = len(re.findall(r"(?<!-)--(?!-)", text))
    return em, en, double_hyphen


def find_short_sentence_clusters(sentences, threshold=8, min_run=3):
    """Find runs of consecutive short sentences."""
    runs = []
    current = []
    for i, s in enumerate(sentences):
        wc = count_words(s)
        if wc <= threshold:
            current.append((i, s, wc))
        else:
            if len(current) >= min_run:
                runs.append(list(current))
            current = []
    if len(current) >= min_run:
        runs.append(list(current))
    return runs


def find_two_word_punchlines(sentences, short_max=4, long_min=15):
    """Find any sentence ≤short_max words preceded by one ≥long_min words.
    Threshold lowered from 20 to 15 — patterns.md examples show real cases
    with ~13-word setups (e.g. 'won against 5,800 builders. It works.')."""
    hits = []
    for i in range(1, len(sentences)):
        prev_wc = count_words(sentences[i - 1])
        cur_wc = count_words(sentences[i])
        if prev_wc >= long_min and cur_wc <= short_max:
            hits.append((i, sentences[i], cur_wc, sentences[i - 1][:80]))
    return hits


def find_negation_reversal_candidates(sentences):
    hits = []
    for i, s in enumerate(sentences):
        for pat in NEGATION_OPENERS:
            if re.search(pat, s):
                hits.append((i, s, pat))
                break
    return hits


def find_cross_sentence_negation(sentences):
    """Detect 'X isn't/aren't/wasn't Y. It's/They're/X is Z.' across sentence pairs.
    The negation-reveal pattern that the single-sentence regex misses."""
    hits = []
    neg_pattern = re.compile(
        r"\b(?:isn't|is not|aren't|are not|wasn't|was not|weren't|were not)\b",
        re.IGNORECASE,
    )
    affirm_start = re.compile(
        r"^\s*(?:It'?s|It is|They'?re|They are|That'?s|That is|What it is)\b",
        re.IGNORECASE,
    )
    for i in range(len(sentences) - 1):
        cur = sentences[i]
        nxt = sentences[i + 1]
        # Both sentences must be reasonably short for the pattern to read as setup-reveal
        if count_words(cur) > 25 or count_words(nxt) > 15:
            continue
        if neg_pattern.search(cur) and affirm_start.search(nxt):
            hits.append((i, cur, nxt))
    return hits


def find_dramatic_countdown(sentences):
    """Find 2+ consecutive short sentences starting with 'Not'."""
    hits = []
    for i in range(1, len(sentences)):
        prev = sentences[i - 1]
        cur = sentences[i]
        if (
            count_words(prev) <= 8
            and count_words(cur) <= 8
            and re.match(r"^\s*Not\b", prev, re.IGNORECASE)
            and re.match(r"^\s*Not\b", cur, re.IGNORECASE)
        ):
            hits.append((i, [prev, cur]))
    return hits


def find_anaphora(sentences, min_run=3):
    """3+ consecutive sentences starting with the same 2-word opening."""
    hits = []
    if len(sentences) < min_run:
        return hits
    current_run = [0]
    for i in range(1, len(sentences)):
        prev_words = sentences[i - 1].split()[:2]
        cur_words = sentences[i].split()[:2]
        if (
            len(prev_words) == 2 and len(cur_words) == 2
            and prev_words[0].lower() == cur_words[0].lower()
            and prev_words[1].lower() == cur_words[1].lower()
        ):
            current_run.append(i)
        else:
            if len(current_run) >= min_run:
                hits.append([(idx, sentences[idx]) for idx in current_run])
            current_run = [i]
    if len(current_run) >= min_run:
        hits.append([(idx, sentences[idx]) for idx in current_run])
    return hits


def find_three_beat_stacks(text):
    """Heuristic: 'word, word, and word' pattern."""
    pattern = r"\b(\w+(?:\s+\w+)?)\s*,\s*(\w+(?:\s+\w+)?)\s*,\s*and\s+(\w+(?:\s+\w+)?)\b"
    return re.findall(pattern, text)


def find_setup_reveal_endings(paragraphs):
    """Paragraphs ending with a setup-reveal phrase."""
    hits = []
    for i, p in enumerate(paragraphs):
        sentences = split_sentences(p)
        if not sentences:
            continue
        last = sentences[-1]
        for pat in SETUP_REVEAL_PHRASES:
            if re.search(pat, last, flags=re.IGNORECASE):
                hits.append((i, last, pat))
                break
    return hits


def find_buzzword_density(paragraphs, threshold=3):
    """Paragraphs with `threshold`+ buzzwords."""
    hits = []
    for i, p in enumerate(paragraphs):
        count = 0
        found = []
        for bw in BUZZWORDS:
            pattern = r"\b" + re.escape(bw) + r"\b"
            n = len(re.findall(pattern, p, flags=re.IGNORECASE))
            if n:
                count += n
                found.append((bw, n))
        if count >= threshold:
            hits.append((i, count, found))
    return hits


def find_crafted_closer(text):
    """Final non-empty line matches crafted-closer patterns."""
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
    if not lines:
        return None
    last = lines[-1]
    for pat in CRAFTED_CLOSERS:
        if re.search(pat, last, flags=re.IGNORECASE):
            return (last, pat)
    return None


def find_performative_opening(text):
    """First sentence matches a performative opening pattern."""
    sentences = split_sentences(strip_code_blocks(text))
    if not sentences:
        return None
    first = sentences[0]
    for pat in PERFORMATIVE_OPENINGS:
        if re.search(pat, first, flags=re.IGNORECASE):
            return (first, pat)
    return None


def find_hedge_stacking(sentences):
    """Sentences with 3+ hedge words."""
    hits = []
    for i, s in enumerate(sentences):
        count = 0
        for pat in HEDGE_WORDS:
            count += len(re.findall(pat, s, flags=re.IGNORECASE))
        if count >= 3:
            hits.append((i, s, count))
    return hits


def find_while_openers(text):
    """Count 'While X, Y' sentence openers."""
    matches = WHILE_OPENER.findall(text)
    return len(matches)


def find_acknowledgment_loop(text, title=None):
    """First sentence echoes the title (if provided) or paraphrases prompt."""
    if not title:
        return None
    sentences = split_sentences(strip_code_blocks(text))
    if not sentences:
        return None
    first = sentences[0].lower()
    title_words = set(re.findall(r"\b\w+\b", title.lower()))
    first_words = set(re.findall(r"\b\w+\b", first))
    overlap = title_words & first_words
    # Stop words don't count
    stop = {"a", "an", "the", "to", "of", "in", "on", "for", "and", "or", "is", "are"}
    overlap -= stop
    if len(overlap) >= 3:
        return (first, list(overlap))
    return None


def find_fabricated_cases(text):
    """Find 'Take Sarah, a marketing manager...' patterns."""
    return FABRICATED_CASE.findall(text)


def compute_burstiness(sentences):
    """Std dev of sentence lengths divided by mean. Returns None for <5 sentences."""
    if len(sentences) < 5:
        return None
    lengths = [count_words(s) for s in sentences]
    mean = sum(lengths) / len(lengths)
    if mean == 0:
        return None
    variance = sum((x - mean) ** 2 for x in lengths) / len(lengths)
    std = math.sqrt(variance)
    return round(std / mean, 3)


def find_bigram_repetition(text, threshold=5):
    """Find 2-word phrases appearing `threshold`+ times. Excludes stopword-only bigrams."""
    words = re.findall(r"\b\w+\b", text.lower())
    if len(words) < 10:
        return []
    bigrams = {}
    stop = {"a", "an", "the", "to", "of", "in", "on", "for", "and", "or", "is", "are",
            "be", "was", "were", "by", "as", "at", "with", "this", "that", "it", "its"}
    for i in range(len(words) - 1):
        if words[i] in stop and words[i + 1] in stop:
            continue
        bg = (words[i], words[i + 1])
        bigrams[bg] = bigrams.get(bg, 0) + 1
    return [(bg, count) for bg, count in bigrams.items() if count >= threshold]


def contraction_ratio(text):
    """Ratio of contractions to could-be-contractions. 0 = formal/AI lean."""
    contractions = len(re.findall(r"\b\w+'(?:s|t|re|ve|ll|d|m)\b", text))
    expansions = len(re.findall(r"\b(?:do not|does not|did not|will not|would not|could not|should not|cannot|can not|is not|are not|was not|were not|has not|have not|had not|it is|that is|there is|i am)\b", text, flags=re.IGNORECASE))
    total = contractions + expansions
    if total == 0:
        return None
    return round(contractions / total, 2)


def detect_model_fingerprint(text):
    """Heuristic: count GPT/Claude/Gemini markers and report dominant."""
    gpt_count = sum(len(re.findall(p, text, flags=re.IGNORECASE)) for p in GPT_MARKERS)
    claude_count = sum(len(re.findall(p, text, flags=re.IGNORECASE)) for p in CLAUDE_MARKERS)
    gemini_count = sum(len(re.findall(p, text, flags=re.IGNORECASE)) for p in GEMINI_MARKERS)

    total = gpt_count + claude_count + gemini_count
    if total < 2:
        return ("none", {"gpt": gpt_count, "claude": claude_count, "gemini": gemini_count})

    # Find max
    counts = {"gpt": gpt_count, "claude": claude_count, "gemini": gemini_count}
    sorted_counts = sorted(counts.items(), key=lambda x: -x[1])
    if sorted_counts[0][1] >= 2 and sorted_counts[0][1] >= 1.5 * (sorted_counts[1][1] or 1):
        return (sorted_counts[0][0], counts)
    return ("mixed", counts)


def detect_genre(text):
    """Crude genre inference. Falls back to 'casual'."""
    text_lower = text.lower()
    # Academic markers
    if (
        len(re.findall(r"\b(?:hypothesis|methodology|et al\.|fig\.|p\s*<\s*0\.0|table \d+)", text_lower)) >= 2
        or "abstract:" in text_lower
        or re.search(r"\[\d+\]|\(\d{4}\)", text)
    ):
        return "academic"
    # Marketing markers
    if len(re.findall(r"\b(?:cta|conversion|landing page|sign up|free trial|book a demo|pricing)\b", text_lower)) >= 2:
        return "marketing"
    # Encyclopedic markers
    if (
        re.search(r"^[A-Z][\w\s]+ \(born", text)
        or re.search(r"^[A-Z][\w\s]+ \(c\.\s*\d{4}", text)
        or len(re.findall(r"\bwas (?:a|an|the)\b", text)) >= 5
    ):
        return "encyclopedic"
    # Fiction: dialogue heavy
    if text.count('"') >= 6:
        return "fiction"
    return "casual"


def find_markdown_tells(text):
    """Detect bold-first bullets, emoji bullets, excessive headers, etc."""
    tells = {}
    # Bold-first bullets
    bold_bullets = len(re.findall(r"^\s*[-*]\s+\*\*[^*]+\*\*\s*[:.]", text, flags=re.MULTILINE))
    if bold_bullets >= 3:
        tells["bold_first_bullets"] = bold_bullets
    # Emoji bullets
    emoji_bullets = len(re.findall(r"^\s*[🔹✨📌📍🎯💡⭐🚀🔥]", text, flags=re.MULTILINE))
    if emoji_bullets >= 1:
        tells["emoji_bullets"] = emoji_bullets
    # Excessive headers
    h2_count = len(re.findall(r"^##\s+", text, flags=re.MULTILINE))
    h3_count = len(re.findall(r"^###\s+", text, flags=re.MULTILINE))
    word_count = count_words(text)
    if word_count > 0 and (h2_count + h3_count) > word_count / 200:
        tells["excessive_headers"] = {
            "h2": h2_count, "h3": h3_count, "word_count": word_count,
        }
    # Title patterns in headers
    title_patterns = re.findall(
        r"^#+\s+(?:[\w\s]+:\s+(?:A|The|Your|Everything)\s+(?:Comprehensive|Ultimate|Definitive|Complete)\s+Guide|The Ultimate Guide to|Everything You Need to Know|How to \w+ in 20\d{2})",
        text, flags=re.MULTILINE | re.IGNORECASE,
    )
    if title_patterns:
        tells["clichéd_title_patterns"] = title_patterns
    return tells


# =============================================================================
# COMPREHENSION DETECTORS
# =============================================================================

def count_syllables(word):
    """Estimate syllable count via vowel-group heuristic.

    Counts vowel runs, subtracts trailing silent 'e', minimum 1.
    Approximate but stdlib-only. Used for Flesch / FK / SMOG.
    """
    word = word.lower().strip()
    if not word:
        return 0
    word = re.sub(r"[^a-z]", "", word)
    if not word:
        return 0
    # Special-case very short words
    if len(word) <= 3:
        return 1
    # Count vowel groups
    vowel_runs = re.findall(r"[aeiouy]+", word)
    syllables = len(vowel_runs)
    # Silent trailing 'e'
    if word.endswith("e") and not word.endswith("le") and syllables > 1:
        syllables -= 1
    # 'le' at the end of a word with consonant before counts (e.g. "table" = 2)
    if word.endswith("le") and len(word) > 2 and word[-3] not in "aeiouy":
        # Already handled by vowel-group counting (the "e" in "le" is its own syllable)
        pass
    return max(1, syllables)


def find_undefined_acronyms(text):
    """F1. Acronyms without parenthetical expansion, excluding the allowlist.

    Returns dict with:
      - 'acronyms': list of (acronym, count) for undefined ones
      - 'total_count': total occurrences of undefined acronyms
      - 'distinct_count': distinct undefined acronyms
      - 'density_per_100w': occurrences per 100 words
    """
    # Find parenthetical expansions: "Search Request Agent (SRA)"
    introduced = set(PAREN_EXPANSION.findall(text))
    # Find all acronym tokens
    all_tokens = ACRONYM_TOKEN.findall(text)
    counts = {}
    for tok in all_tokens:
        if tok in KNOWN_ACRONYMS:
            continue
        if tok in introduced:
            continue
        # Skip purely numeric (rare given our regex but safe)
        if tok.isdigit():
            continue
        counts[tok] = counts.get(tok, 0) + 1
    pairs = sorted(counts.items(), key=lambda x: -x[1])
    total = sum(counts.values())
    words = max(1, count_words(text))
    density = round(total / words * 100, 2)
    return {
        "acronyms": pairs,
        "total_count": total,
        "distinct_count": len(counts),
        "density_per_100w": density,
    }


def find_named_entities(text, sentences):
    """F2. Named-entity bombing — capitalized non-sentence-start tokens.

    Heuristic — no NER. Counts capitalized words that aren't:
    - first word of a sentence
    - common acronyms
    - first word of a heading line (markdown # ## ###)
    - the pronoun "I"
    - month/day-of-week (very common false positives)
    """
    # Build a set of words occurring as sentence-initial. We approximate by
    # taking the first non-trivial word of each sentence.
    sentence_starts = set()
    for s in sentences:
        ws = re.findall(r"\b\w+\b", s)
        if ws:
            sentence_starts.add(ws[0])
    common_calendar = {
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    }
    # Strip markdown heading lines (count their tokens but don't double-flag the first word)
    body = re.sub(r"^#+\s+(.*)$", r"\1", text, flags=re.MULTILINE)

    # Scan for capitalized tokens that aren't sentence-initial
    tokens = re.findall(r"\b([A-Z][a-zA-Z]+)\b", body)
    counts = {}
    for tok in tokens:
        if tok in common_calendar:
            continue
        if tok in KNOWN_ACRONYMS:
            continue
        if tok in sentence_starts and (tok in {"The", "This", "That", "These", "Those",
                                                "It", "We", "I", "You", "They", "He", "She",
                                                "A", "An", "Our", "Your", "My", "Their", "His", "Her",
                                                "If", "When", "Where", "What", "Why", "How",
                                                "After", "Before", "In", "On", "At", "From", "To",
                                                "But", "And", "Or", "So", "Then", "While", "Now",
                                                "First", "Last", "Second", "Third", "Most", "Some",
                                                "All", "Each", "Every", "No", "Yes",
                                                "Note", "TLDR", "TL", "Re", "Over",
                                                "Since", "Until", "About", "Among", "Through",
                                                "During", "Within", "Across", "Despite", "Although",
                                                "Though", "Because", "Whereas", "Without", "With",
                                                "Like", "Unlike", "Once", "Twice", "Whether",
                                                "However", "Moreover", "Therefore", "Thus", "Hence",
                                                "Otherwise", "Even", "Still", "Just", "Only",
                                                "Already", "Yet", "Sometimes", "Often", "Rarely",
                                                "Always", "Never", "Maybe", "Perhaps", "Probably"}):
            continue
        counts[tok] = counts.get(tok, 0) + 1
    pairs = sorted(counts.items(), key=lambda x: -x[1])
    total = sum(counts.values())
    words = max(1, count_words(text))
    density = round(total / words * 100, 2)
    return {
        "entities": pairs,
        "total_count": total,
        "distinct_count": len(counts),
        "density_per_100w": density,
    }


def find_stat_bombing(sentences):
    """F3. Sentences with 4+ numeric tokens (uncontextualized stat clusters).

    Threshold of 4 (rather than 3) excludes ordinary narrative sentences that
    happen to mention several numbers (year + count + percentage). True stat
    bombing reads like "$50M pipeline, $14M ARR, 93% gap, 50% lift" — many
    numeric claims tightly packed.

    Returns list of (idx, sentence_excerpt, numeric_count).
    """
    hits = []
    for i, s in enumerate(sentences):
        nums = NUMERIC_TOKEN.findall(s)
        if len(nums) >= 4:
            hits.append((i, s[:120], len(nums)))
    return hits


def find_wall_of_text(paragraphs):
    """F4. Paragraphs with >5 sentences or >100 words."""
    hits = []
    for i, p in enumerate(paragraphs):
        sents = split_sentences(p)
        wc = count_words(p)
        if len(sents) > 5 or wc > 100:
            hits.append((i, len(sents), wc, p[:80]))
    return hits


def find_density_without_headings(text):
    """F5. >500 words with no headings, OR heading density < 1 per 300 words."""
    h2 = len(re.findall(r"^##\s+", text, flags=re.MULTILINE))
    h3 = len(re.findall(r"^###\s+", text, flags=re.MULTILINE))
    h_total = h2 + h3
    words = count_words(text)
    if words >= 500 and h_total == 0:
        return {"flagged": True, "reason": "500+ words, zero headings", "h_count": 0, "words": words}
    if words >= 300 and h_total > 0 and (words / h_total) > 300:
        return {
            "flagged": True,
            "reason": f"heading density too low ({h_total} headings for {words} words)",
            "h_count": h_total,
            "words": words,
        }
    return {"flagged": False, "h_count": h_total, "words": words}


def find_telegraphic_colons(paragraphs):
    """G1. Mid-paragraph "Capital-Word(s): Capital-Word" patterns; flag at 3+/para."""
    hits = []
    for i, p in enumerate(paragraphs):
        labels = COLON_LABEL.findall(p)
        if len(labels) >= 3:
            hits.append((i, len(labels), labels[:5]))
    return hits


def find_list_pretending_prose(paragraphs):
    """G2. Paragraphs with 2+ semicolons or 3+ '+' separators in prose."""
    hits = []
    for i, p in enumerate(paragraphs):
        # Skip paragraphs that look like lists or code
        if re.match(r"^\s*[-*+]\s", p):
            continue
        semi = p.count(";")
        plus = p.count("+")
        if semi >= 2 or plus >= 3:
            hits.append((i, semi, plus, p[:80]))
    return hits


def find_long_sentences(sentences, threshold=30):
    """G3. Any sentence over `threshold` words."""
    hits = []
    for i, s in enumerate(sentences):
        wc = count_words(s)
        if wc > threshold:
            hits.append((i, wc, s[:120]))
    return hits


def find_runon_sentences(sentences, clause_threshold=4):
    """G4. Sentences with `threshold`+ comma+conjunction independent clauses."""
    hits = []
    conj_pat = re.compile(r",\s+(and|but|or|so|yet|because|while|although|though|however|since|whereas)\b", re.IGNORECASE)
    for i, s in enumerate(sentences):
        clauses = len(conj_pat.findall(s))
        # Also count em-dash and semicolon-introduced clauses
        clauses += s.count("—")
        clauses += s.count(";")
        if clauses >= clause_threshold:
            hits.append((i, clauses, s[:120]))
    return hits


def find_glue_word_starts(sentences):
    """G5. Sentence-initial glue-word patterns."""
    hits = []
    for i, s in enumerate(sentences):
        for pat in GLUE_WORD_OPENERS:
            if re.search(pat, s, re.IGNORECASE):
                hits.append((i, s[:80], pat))
                break
    return hits


def find_forward_references(text):
    """H5. 'as we'll see', 'more on this later', etc."""
    return find_regex_hits(text, FORWARD_REFERENCE)


def find_no_skim_layer(text, words):
    """I9. 0 bold/strong markdown when 500+ words."""
    bolds = len(re.findall(r"\*\*[^*]+\*\*", text))
    if words >= 500 and bolds == 0:
        return {"flagged": True, "bolds": 0, "words": words}
    return {"flagged": False, "bolds": bolds, "words": words}


def find_hierarchy_collapse(text):
    """I5. Heading levels skip (H1 → H3, H2 → H4, etc.)."""
    headings = []
    for m in re.finditer(r"^(#+)\s+(.+)$", text, flags=re.MULTILINE):
        level = len(m.group(1))
        if level <= 6:
            headings.append((level, m.group(2)[:60]))
    skips = []
    if not headings:
        return skips
    for i in range(1, len(headings)):
        prev, cur = headings[i - 1][0], headings[i][0]
        if cur > prev + 1:
            skips.append({
                "from_level": prev,
                "to_level": cur,
                "from": headings[i - 1][1],
                "to": headings[i][1],
            })
    return skips


def find_parallelism_failure(text):
    """I12. Sequential bullets with mixed grammatical forms.

    Heuristic: for sequential bullet lines, classify the first token as
    verb-ish (-s/-ing/-ed or imperative/base form), noun-ish (capitalized noun),
    or question (ends with ?).  If 3+ different forms appear in 4+ bullets, flag.
    """
    blocks = []
    current = []
    for line in text.split("\n"):
        m = re.match(r"^\s*[-*+]\s+(.+)$", line)
        if m:
            current.append(m.group(1))
        else:
            if len(current) >= 4:
                blocks.append(current)
            current = []
    if len(current) >= 4:
        blocks.append(current)

    flagged = []
    for block in blocks:
        forms = set()
        for item in block:
            words = re.findall(r"\b\w+\b", item)
            if not words:
                continue
            first = words[0]
            # Strip markdown formatting like **bold**
            clean = re.sub(r"^\*+", "", item).strip()
            # Question
            if clean.rstrip(".!").endswith("?"):
                forms.add("question")
                continue
            if first.lower().endswith("ing"):
                forms.add("gerund")
                continue
            # Title-case starting word = noun phrase likely
            if first[0].isupper() and len(first) > 1:
                forms.add("noun")
                continue
            # Lowercase starting word — assume verb (imperative)
            forms.add("verb")
        if len(forms) >= 3:
            flagged.append({"block_size": len(block), "forms": sorted(forms), "sample": block[:3]})
    return flagged


def count_passive_voice(sentences):
    """J1. Passive voice percentage (sentences containing passive constructions)."""
    if not sentences:
        return {"count": 0, "percent": 0.0}
    matches = 0
    for s in sentences:
        if PASSIVE_VOICE.search(s):
            matches += 1
    pct = round(matches / len(sentences) * 100, 1)
    return {"count": matches, "percent": pct}


def count_nominalizations(text):
    """J2. -tion / -ment / -ance / -ence / -ity / -ization / -ism / -ness density."""
    matches = NOMINALIZATION_SUFFIXES.findall(text)
    # Filter out very short common words that match the regex but aren't true nominalizations
    # (e.g. some short words may slip through; the regex requires \w{3,} prefix anyway)
    words = max(1, count_words(text))
    density = round(len(matches) / words * 100, 2)
    return {"count": len(matches), "density_per_100w": density, "examples": matches[:10]}


def count_decorative_qualifiers(text):
    """J5. Decorative qualifier density per 100 words."""
    matches = DECORATIVE_QUALIFIERS.findall(text)
    words = max(1, count_words(text))
    density = round(len(matches) / words * 100, 2)
    return {"count": len(matches), "density_per_100w": density, "examples": matches[:10]}


def find_negative_constructions(text):
    """J8. 'not un-', 'not in-', 'don't fail to', etc."""
    return find_regex_hits(text, NEGATIVE_CONSTRUCTIONS)


def acronym_window_compound(text, words_per_window=100):
    """Compound trigger: 4+ DISTINCT undefined acronyms in any 100-word window.

    Threshold is on distinct acronyms (not occurrences) to avoid escalating when
    one acronym is repeated. The spec says "3+ undefined acronyms" but with
    instance counting this fires too readily on cover-letter prose with a few
    project names. Tightening to 4 distinct undefined acronyms in a window.
    """
    word_tokens = re.findall(r"\b\S+\b", text)
    if len(word_tokens) < words_per_window:
        return False
    introduced = set(PAREN_EXPANSION.findall(text))
    for start in range(0, len(word_tokens) - words_per_window + 1, max(1, words_per_window // 4)):
        window = " ".join(word_tokens[start : start + words_per_window])
        acros = ACRONYM_TOKEN.findall(window)
        undef = {a for a in acros if a not in KNOWN_ACRONYMS and a not in introduced}
        if len(undef) >= 4:
            return True
    return False


def named_entity_window_compound(text, sentences, words_per_window=100):
    """Compound trigger: 7+ named entities in any 100-word window.

    Spec says 5+, but at exactly 5/100w prose with a few company names triggers.
    Tightening to 7+ matches the "named-entity bombing" case from
    comprehension.md F2 — extreme density, not normal personal-story prose.
    """
    word_tokens = re.findall(r"\b\S+\b", text)
    if len(word_tokens) < words_per_window:
        return False
    sentence_starts = set()
    for s in sentences:
        ws = re.findall(r"\b\w+\b", s)
        if ws:
            sentence_starts.add(ws[0])
    common_calendar = {
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    }
    common_starts = {"The", "This", "That", "These", "Those", "It", "We", "I", "You",
                     "They", "He", "She", "A", "An", "Our", "Your", "My", "Their",
                     "If", "When", "Where", "What", "Why", "How", "After", "Before",
                     "In", "On", "At", "From", "To", "But", "And", "Or", "So", "Then"}
    for start in range(0, len(word_tokens) - words_per_window + 1, max(1, words_per_window // 4)):
        window = " ".join(word_tokens[start : start + words_per_window])
        # Find capitalized tokens
        toks = re.findall(r"\b([A-Z][a-zA-Z]+)\b", window)
        ents = [t for t in toks
                if t not in common_calendar
                and t not in KNOWN_ACRONYMS
                and not (t in sentence_starts and t in common_starts)]
        # Use distinct count — repeated mentions of the same brand shouldn't escalate.
        if len(set(ents)) >= 7:
            return True
    return False


def long_paragraph_no_subheading(text, paragraphs, threshold_words=200):
    """Compound trigger: any paragraph >200 words with no subheading inside.

    Threshold 200 (rather than 150) avoids escalating standard letter / essay
    paragraphs. The trigger fires for genuinely intimidating wall-of-text blocks
    that lack any internal structure — see calibration.md §9.
    """
    for p in paragraphs:
        if count_words(p) > threshold_words:
            if not re.search(r"^#+\s+", p, flags=re.MULTILINE):
                return True
    return False


# =============================================================================
# READABILITY METRICS
# =============================================================================

def compute_readability_metrics(text, sentences, words_total):
    """Compute the 8 metrics from references/readability-metrics.md.

    Returns a dict with all metric values rounded to 2 decimal places (or None
    if the input is too short to compute reliably).
    """
    if not sentences or words_total < 5:
        return {
            "flesch_reading_ease": None,
            "flesch_kincaid_grade": None,
            "smog": None,
            "coleman_liau": None,
            "dale_chall": None,
            "lexical_density": None,
            "avg_sentence_length": None,
            "sentence_length_stddev": None,
            "passive_voice_pct": None,
            "polysyllable_count": None,
            "difficult_word_pct": None,
        }

    # Tokenize words for syllable + Dale-Chall accounting
    word_list = re.findall(r"\b[a-zA-Z']+\b", text)
    word_count = len(word_list)
    if word_count == 0:
        return {
            "flesch_reading_ease": None,
            "flesch_kincaid_grade": None,
            "smog": None,
            "coleman_liau": None,
            "dale_chall": None,
            "lexical_density": None,
            "avg_sentence_length": None,
            "sentence_length_stddev": None,
            "passive_voice_pct": None,
            "polysyllable_count": None,
            "difficult_word_pct": None,
        }

    # Syllable totals
    syllables_total = 0
    polysyllables = 0
    for w in word_list:
        s = count_syllables(w)
        syllables_total += s
        if s >= 3:
            polysyllables += 1

    sentence_count = len(sentences)
    asl = word_count / sentence_count  # avg sentence length
    asw = syllables_total / word_count  # avg syllables per word

    # 1. Flesch Reading Ease
    fre = 206.835 - 1.015 * asl - 84.6 * asw

    # 2. Flesch-Kincaid Grade Level
    fkgl = 0.39 * asl + 11.8 * asw - 15.59

    # 3. SMOG (only meaningful for ≥30 sentences)
    smog = 1.0430 * math.sqrt(polysyllables * 30 / sentence_count) + 3.1291

    # 4. Coleman-Liau Index
    letters = sum(1 for c in text if c.isalpha())
    L = letters / word_count * 100  # letters per 100 words
    S = sentence_count / word_count * 100  # sentences per 100 words
    cli = 0.0588 * L - 0.296 * S - 15.8

    # 5. Dale-Chall (simplified — using curated wordlist)
    difficult = 0
    for w in word_list:
        if w.lower().strip("'") not in DALE_CHALL_WORDLIST:
            difficult += 1
    diff_pct = difficult / word_count * 100
    dc_score = 0.1579 * diff_pct + 0.0496 * asl
    if diff_pct > 5:
        dc_score += 3.6365

    # 6. Lexical density (heuristic)
    content_words = sum(1 for w in word_list if w.lower() not in STOPWORDS)
    lex_density = content_words / word_count * 100

    # 7. Avg sentence length + stddev
    lengths = [count_words(s) for s in sentences]
    if lengths:
        m = sum(lengths) / len(lengths)
        var = sum((x - m) ** 2 for x in lengths) / len(lengths)
        std = math.sqrt(var)
    else:
        m = 0
        std = 0

    # 8. Passive voice %
    passive_data = count_passive_voice(sentences)

    return {
        "flesch_reading_ease": round(fre, 2),
        "flesch_kincaid_grade": round(fkgl, 2),
        "smog": round(smog, 2),
        "coleman_liau": round(cli, 2),
        "dale_chall": round(dc_score, 2),
        "lexical_density": round(lex_density, 2),
        "avg_sentence_length": round(m, 2),
        "sentence_length_stddev": round(std, 2),
        "passive_voice_pct": passive_data["percent"],
        "polysyllable_count": polysyllables,
        "difficult_word_pct": round(diff_pct, 2),
    }


# =============================================================================
# COMPREHENSION ANALYSIS
# =============================================================================

def analyze_comprehension(text, audience="casual", sentences=None, paragraphs=None,
                          total_words=None):
    """Run the comprehension axis. Mirrors structure of analyze() AI-slop axis."""
    clean = strip_code_blocks(text)
    if sentences is None:
        sentences = split_sentences(clean)
    if paragraphs is None:
        paragraphs = split_paragraphs(clean)
    if total_words is None:
        total_words = sum(count_words(s) for s in sentences)

    # Detector outputs
    acronyms = find_undefined_acronyms(clean)
    entities = find_named_entities(clean, sentences)
    stat_bomb = find_stat_bombing(sentences)
    walls = find_wall_of_text(paragraphs)
    density_no_h = find_density_without_headings(text)
    colons = find_telegraphic_colons(paragraphs)
    list_prose = find_list_pretending_prose(paragraphs)
    long_sents = find_long_sentences(sentences, threshold=30)
    runons = find_runon_sentences(sentences)
    glue = find_glue_word_starts(sentences)
    forward = find_forward_references(clean)
    skim = find_no_skim_layer(text, total_words)
    hierarchy = find_hierarchy_collapse(text)
    parallelism = find_parallelism_failure(text)
    passive = count_passive_voice(sentences)
    nominalizations = count_nominalizations(clean)
    hedge_stack = find_hedge_stacking(sentences)
    decorative = count_decorative_qualifiers(clean)
    negatives = find_negative_constructions(clean)

    # Readability metrics panel
    metrics = compute_readability_metrics(clean, sentences, total_words)

    # Severity counting per comprehension.md / calibration.md §9
    # H = high, M = medium, L = low
    compH = 0
    compM = 0
    compL = 0

    # F1: H if density >= 3 per 100 words
    f1_flag = acronyms["density_per_100w"] >= 3
    if f1_flag:
        compH += 1
    # Each undefined acronym is also a small instance hit (treat as 1 H point per 5 occurrences)
    if acronyms["total_count"] >= 5:
        compH += acronyms["total_count"] // 5

    # F2: H if density >= 5 per 100 words. Above 8/100w add an extra H per 10 entities.
    f2_flag = entities["density_per_100w"] >= 5
    if f2_flag:
        compH += 1
    # Only stack additional H weight when the entity density is well above threshold.
    if entities["density_per_100w"] >= 8 and entities["total_count"] >= 10:
        compH += entities["total_count"] // 10

    # F3: H per stat-bombed sentence
    compH += len(stat_bomb)

    # F4: M per wall paragraph
    compM += len(walls)

    # F5: H if flagged
    if density_no_h["flagged"]:
        compH += 1

    # G1: H per paragraph with 3+ telegraphic colons
    compH += len(colons)

    # G2: M per list-pretending-to-be-prose paragraph
    compM += len(list_prose)

    # G3: M per long sentence (30-40w), H per very long (>40w).
    # 30+ word sentences are common in polished prose — only count as H once
    # they cross the 40-word "comprehension cliff" or stack multiple instances.
    very_long = [s for s in long_sents if s[1] > 40]
    moderate_long = [s for s in long_sents if 30 < s[1] <= 40]
    compH += len(very_long)
    compM += len(moderate_long)

    # G4: H per run-on (4+ independent clauses always overflows working memory)
    compH += len(runons)

    # G5: L per glue-word instance
    compL += len(glue)

    # H5: H per forward-reference
    compH += sum(c for _, c, _ in forward)

    # I9: M if no skim layer
    if skim["flagged"]:
        compM += 1

    # I5: M per hierarchy skip
    compM += len(hierarchy)

    # I12: M per parallelism block
    compM += len(parallelism)

    # J1: M if passive % > 10
    if passive["percent"] > 10:
        compM += 1

    # J2: M if nominalization density > 5 per 100w
    if nominalizations["density_per_100w"] > 5:
        compM += 1

    # J4: M per hedge-stacked sentence (reuse AI-slop detector)
    compM += len(hedge_stack)

    # J5: L per decorative qualifier instance over 2 per 100w threshold
    if decorative["density_per_100w"] > 2:
        # Count overage as low-severity points
        compL += decorative["count"]

    # J8: L per negative construction
    compL += sum(c for _, c, _ in negatives)

    # Density score per calibration.md §9
    units = max(1, total_words / 500)
    comp_density = ((compH * 3) + (compM * 1) + (compL * 0.25)) / units

    # Verdict thresholds — same scale as AI-Slop (calibration.md §9)
    if comp_density >= 18:
        verdict = "CRITICAL"
    elif comp_density >= 10:
        verdict = "HIGH"
    elif comp_density >= 5:
        verdict = "MEDIUM"
    elif comp_density >= 2:
        verdict = "LOW"
    else:
        verdict = "PASS"

    # Compound triggers — escalate one tier
    escalations = []
    if acronym_window_compound(clean):
        escalations.append("4+ distinct undefined acronyms in a 100-word window")
    if named_entity_window_compound(clean, sentences):
        escalations.append("7+ distinct named entities in a 100-word window")
    if any(c >= 3 for _, c, _ in colons):
        escalations.append("3+ telegraphic colon-labels in one paragraph")
    if long_paragraph_no_subheading(text, paragraphs):
        escalations.append("Paragraph over 150 words with no subheading")

    if escalations:
        order = ["PASS", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
        idx = order.index(verdict)
        verdict = order[min(len(order) - 1, idx + 1)]

    # Audience adjustment — relax thresholds for academic/technical
    audience_preset = AUDIENCE_PRESETS.get(audience, AUDIENCE_PRESETS["casual"])
    audience_adjustment = None
    if audience in ("academic", "technical"):
        # Long sentences are tolerated more; downgrade if the verdict is driven
        # primarily by long-sentence or passive-voice flags.
        long_sent_share = (
            len(long_sents) * 3 / max(1, comp_density * units)
            if comp_density > 0 else 0
        )
        if long_sent_share > 0.4 and verdict in ("HIGH", "MEDIUM"):
            order = ["PASS", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
            idx = order.index(verdict)
            verdict = order[max(0, idx - 1)]
            audience_adjustment = (
                f"{audience} audience: downgraded one tier "
                f"(long sentences expected in this register)"
            )

    return {
        "verdict": verdict,
        "density": round(comp_density, 2),
        "totals": {"high": compH, "medium": compM, "low": compL},
        "audience": audience,
        "audience_targets": audience_preset,
        "audience_adjustment": audience_adjustment,
        "escalations": escalations,
        "patterns": {
            "F1_undefined_acronyms": acronyms,
            "F2_named_entities": entities,
            "F3_stat_bombing": stat_bomb,
            "F4_wall_of_text": walls,
            "F5_density_no_headings": density_no_h,
            "G1_telegraphic_colons": colons,
            "G2_list_as_prose": list_prose,
            "G3_long_sentences": long_sents,
            "G4_runon_sentences": runons,
            "G5_glue_word_starts": glue,
            "H5_forward_references": forward,
            "I5_hierarchy_collapse": hierarchy,
            "I9_no_skim_layer": skim,
            "I12_parallelism_failure": parallelism,
            "J1_passive_voice": passive,
            "J2_nominalizations": nominalizations,
            "J4_hedge_stacking": hedge_stack,
            "J5_decorative_qualifiers": decorative,
            "J8_negative_constructions": negatives,
        },
        "metrics": metrics,
    }


# =============================================================================
# ANALYSIS
# =============================================================================

def combined_recommendation(slop_verdict, comp_verdict):
    """Pick the cross-axis recommendation per calibration.md §11."""
    rank = {"PASS": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
    s = rank[slop_verdict]
    c = rank[comp_verdict]
    worst = max(s, c)
    if worst <= 1:
        return "Ship it. Polish-pass at most."
    if s == 2 and c == 2:
        return "Both cleanup. Often the same fixes."
    if s >= 3 and c >= 3:
        return "Full rewrite. Both axes failing."
    if c >= 3 and s <= 2:
        return "Comprehension rewrite. The texture is fine but the reader can't follow."
    if s >= 3 and c <= 2:
        return "AI-Slop rewrite. The reader-friendliness is fine but the AI texture is loud."
    if s == 2 or c == 2:
        return "Significant cleanup. The fixes overlap; tackle them together."
    return "Spot-fix the listed items. Reader will follow with minor friction."


def analyze(text, genre=None, strict_em_dash=False, audience="casual"):
    """Run the full scan (both axes) and return a structured result."""
    clean = strip_code_blocks(text)
    paragraphs = split_paragraphs(clean)
    sentences = split_sentences(clean)
    word_counts = [count_words(s) for s in sentences]
    total_words = sum(word_counts)

    em, en, dh = find_em_dashes(clean)

    # Genre detection
    detected_genre = detect_genre(clean)
    if not genre:
        genre = detected_genre

    # Model fingerprint
    fingerprint, fp_counts = detect_model_fingerprint(clean)

    # Burstiness
    burst = compute_burstiness(sentences)

    # Build results
    result = {
        "stats": {
            "words": total_words,
            "paragraphs": len(paragraphs),
            "sentences": len(sentences),
            "sentence_avg": round(sum(word_counts) / len(word_counts), 1) if word_counts else 0,
            "sentence_min": min(word_counts) if word_counts else 0,
            "sentence_max": max(word_counts) if word_counts else 0,
            "burstiness": burst,
            "contraction_ratio": contraction_ratio(clean),
            "detected_genre": detected_genre,
            "applied_genre": genre,
            "model_fingerprint": fingerprint,
            "fingerprint_counts": fp_counts,
        },
        "high": {
            "em_dashes": em,
            "en_dashes": en,
            "double_hyphens": dh,
            "verbs_h": find_phrase_hits(clean, VERBS_H),
            "nouns_h": find_phrase_hits(clean, NOUNS_H),
            "intensifiers_h": find_phrase_hits(clean, INTENSIFIERS_H),
            "connectors_h": find_phrase_hits(clean, CONNECTORS_H),
            "sycophancy_open": find_regex_hits(clean, SYCOPHANCY_OPEN_H),
            "sycophancy_close": find_regex_hits(clean, SYCOPHANCY_CLOSE_H),
            "vague_authority_h": find_regex_hits(clean, VAGUE_AUTH_H),
            "knowledge_cutoff": find_regex_hits(clean, KNOWLEDGE_CUTOFF),
            "stake_inflation": find_regex_hits(clean, STAKE_INFLATION),
            "grandiose": find_regex_hits(clean, GRANDIOSE),
            "copula_avoidance": find_regex_hits(clean, COPULA_AVOIDANCE),
            "ing_tails": ING_TAIL.findall(clean),
            "throat_clearing": find_regex_hits(clean, THROAT_CLEARING),
            "rhetorical_qa": RHETORICAL_QA.findall(clean),
            "crafted_closer": find_crafted_closer(clean),
            "performative_opening": find_performative_opening(clean),
            "setup_reveal_endings": find_setup_reveal_endings(paragraphs),
            "fabricated_cases": find_fabricated_cases(clean),
            "buzzword_density": find_buzzword_density(paragraphs),
            "negation_reversals": find_negation_reversal_candidates(sentences),
            "cross_sentence_negation": find_cross_sentence_negation(sentences),
            "short_sentence_clusters_h": [r for r in find_short_sentence_clusters(sentences) if len(r) >= 4],
        },
        "medium": {
            "dramatic_countdown": find_dramatic_countdown(sentences),
            "anaphora": find_anaphora(sentences),
            "short_sentence_clusters_m": [r for r in find_short_sentence_clusters(sentences) if len(r) == 3],
            "two_word_punchlines": find_two_word_punchlines(sentences),
            "three_beat_stacks": find_three_beat_stacks(clean),
            "verbs_m": find_phrase_hits(clean, VERBS_M),
            "nouns_m": find_phrase_hits(clean, NOUNS_M),
            "intensifiers_m": find_phrase_hits(clean, INTENSIFIERS_M),
            "connectors_m": find_phrase_hits(clean, CONNECTORS_M),
            "vague_authority_m": find_regex_hits(clean, VAGUE_AUTH_M),
            "hedge_stacking": find_hedge_stacking(sentences),
            "hedged_superlatives": find_regex_hits(clean, HEDGED_SUPERLATIVES),
            "while_openers": find_while_openers(clean),
            "x_meets_y": len(X_MEETS_Y.findall(clean)),
            "more_than_just": len(MORE_THAN_JUST.findall(clean)),
            "false_concession": find_regex_hits(clean, FALSE_CONCESSION),
            "false_range": len(FALSE_RANGE.findall(clean)),
            "pedagogical": find_regex_hits(clean, PEDAGOGICAL),
            "royal_we": find_regex_hits(clean, ROYAL_WE),
            "whether_or_openers": len(WHETHER_OR.findall(clean)),
            "both_sides_ism": find_regex_hits(clean, BOTH_SIDES),
            "real_tic": len(REAL_TIC.findall(clean)),
            "vapid_analogies": find_regex_hits(clean, VAPID_ANALOGY),
            "historical_analogy_stacking": [
                m for m in [HISTORICAL_ANALOGY.findall(clean)] if len(m) >= 3
            ],
            "dead_metaphor_repetition": [
                (w, len(re.findall(r"\b" + w + r"\b", clean, flags=re.IGNORECASE)))
                for w in DEAD_METAPHORS
                if len(re.findall(r"\b" + w + r"\b", clean, flags=re.IGNORECASE)) >= 3
            ],
        },
        "low": {
            "magic_adverbs": find_phrase_hits(clean, MAGIC_ADVERBS),
            "bigram_repetition": find_bigram_repetition(clean),
            "markdown_tells": find_markdown_tells(text),
        },
    }

    # Compute counts
    high_count = (
        result["high"]["em_dashes"]
        + result["high"]["en_dashes"]
        + result["high"]["double_hyphens"]
        + sum(c for _, c in result["high"]["verbs_h"])
        + sum(c for _, c in result["high"]["nouns_h"])
        + sum(c for _, c in result["high"]["intensifiers_h"])
        + sum(c for _, c in result["high"]["connectors_h"])
        + sum(c for _, _, c in [])  # placeholder
        + sum(c for _, c, _ in result["high"]["sycophancy_open"])
        + sum(c for _, c, _ in result["high"]["sycophancy_close"])
        + sum(c for _, c, _ in result["high"]["vague_authority_h"])
        + sum(c for _, c, _ in result["high"]["knowledge_cutoff"])
        + sum(c for _, c, _ in result["high"]["stake_inflation"])
        + sum(c for _, c, _ in result["high"]["grandiose"])
        + sum(c for _, c, _ in result["high"]["copula_avoidance"])
        + len(result["high"]["ing_tails"])
        + sum(c for _, c, _ in result["high"]["throat_clearing"])
        + len(result["high"]["rhetorical_qa"])
        + (1 if result["high"]["crafted_closer"] else 0)
        + (1 if result["high"]["performative_opening"] else 0)
        + len(result["high"]["setup_reveal_endings"])
        + len(result["high"]["fabricated_cases"])
        + len(result["high"]["buzzword_density"])
        + len(result["high"]["negation_reversals"])
        + len(result["high"]["cross_sentence_negation"])
        + len(result["high"]["short_sentence_clusters_h"])
    )
    medium_count = (
        len(result["medium"]["dramatic_countdown"])
        + len(result["medium"]["anaphora"])
        + len(result["medium"]["short_sentence_clusters_m"])
        + len(result["medium"]["two_word_punchlines"])
        + len(result["medium"]["three_beat_stacks"])
        + sum(c for _, c in result["medium"]["verbs_m"])
        + sum(c for _, c in result["medium"]["nouns_m"])
        + sum(c for _, c in result["medium"]["intensifiers_m"])
        + sum(c for _, c in result["medium"]["connectors_m"])
        + sum(c for _, c, _ in result["medium"]["vague_authority_m"])
        + len(result["medium"]["hedge_stacking"])
        + sum(c for _, c, _ in result["medium"]["hedged_superlatives"])
        + result["medium"]["while_openers"]
        + result["medium"]["x_meets_y"]
        + result["medium"]["more_than_just"]
        + sum(c for _, c, _ in result["medium"]["false_concession"])
        + result["medium"]["false_range"]
        + sum(c for _, c, _ in result["medium"]["pedagogical"])
        + sum(c for _, c, _ in result["medium"]["royal_we"])
        + result["medium"]["whether_or_openers"]
        + sum(c for _, c, _ in result["medium"]["both_sides_ism"])
        + result["medium"]["real_tic"]
        + sum(c for _, c, _ in result["medium"]["vapid_analogies"])
        + len(result["medium"]["historical_analogy_stacking"])
        + len(result["medium"]["dead_metaphor_repetition"])
    )
    low_count = (
        sum(c for _, c in result["low"]["magic_adverbs"])
        + len(result["low"]["bigram_repetition"])
        + len(result["low"]["markdown_tells"])
    )

    # Apply genre adjustments
    if genre == "marketing":
        # Marketing legitimately uses some intensifiers and structure
        # Down-weight intensifier and connector buzzwords slightly
        adjusted_h = high_count - int(0.3 * sum(c for _, c in result["high"]["intensifiers_h"]))
        adjusted_h = max(0, adjusted_h)
        high_count = adjusted_h
    elif genre == "academic":
        # Academic legitimately uses hedging
        adjusted_m = medium_count - len(result["medium"]["hedge_stacking"])
        adjusted_m = max(0, adjusted_m)
        medium_count = adjusted_m
    elif genre == "encyclopedic":
        # Wikipedia-style triggers false positives — reduce all by one tier
        high_count = max(0, high_count - 2)
        medium_count = max(0, medium_count - 2)

    # Em-dash strict mode
    if strict_em_dash and em > 0:
        # Already counted as H; nothing extra needed
        pass
    elif not strict_em_dash:
        # Em dashes alone = L unless 3+ per 500 words
        if total_words > 0 and em < (3 * total_words / 500):
            # Move em dashes from high to low
            high_count -= em
            low_count += em

    # Compute density score per calibration.md §1
    units = max(1, total_words / 500)
    density = ((high_count * 3) + (medium_count * 1) + (low_count * 0.25)) / units

    # Verdict thresholds
    if density >= 18:
        verdict = "CRITICAL"
    elif density >= 10:
        verdict = "HIGH"
    elif density >= 5:
        verdict = "MEDIUM"
    elif density >= 2:
        verdict = "LOW"
    else:
        verdict = "PASS"

    # Compound triggers
    escalated = False
    # Three or more H tells in one paragraph
    paragraphs_with_h = []
    for p in paragraphs:
        h_in_p = 0
        for phrases in [VERBS_H, NOUNS_H, INTENSIFIERS_H, CONNECTORS_H]:
            for ph in phrases:
                h_in_p += len(re.findall(r"\b" + re.escape(ph) + r"\b", p, flags=re.IGNORECASE))
        if h_in_p >= 3:
            paragraphs_with_h.append((p[:80], h_in_p))
    if paragraphs_with_h:
        escalated = True

    # Uncanny valley
    uncanny_valley = False
    if (
        high_count == 0
        and (medium_count + low_count) >= 8 * units
        and burst is not None and burst < 0.5
    ):
        uncanny_valley = True
        escalated = True

    if escalated:
        verdict_order = ["PASS", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
        idx = verdict_order.index(verdict)
        verdict = verdict_order[min(len(verdict_order) - 1, idx + 1)]

    # Sanded-prose signature
    h_vocab_total = (
        sum(c for _, c in result["high"]["verbs_h"])
        + sum(c for _, c in result["high"]["nouns_h"])
    )
    structural_count = (
        sum(c for _, c, _ in result["high"]["copula_avoidance"])
        + len(result["high"]["ing_tails"])
        + len(result["high"]["negation_reversals"])
        + len(result["high"]["cross_sentence_negation"])
        + len(result["medium"]["anaphora"])
        + result["medium"]["false_range"]
        + result["medium"]["while_openers"]
        + len(result["medium"]["hedge_stacking"])
    )
    sanded = h_vocab_total <= 1 and structural_count >= 5

    result["verdict"] = verdict
    result["totals"] = {"high": high_count, "medium": medium_count, "low": low_count}
    result["density"] = round(density, 2)
    result["calibration"] = {
        "compound_escalation": bool(paragraphs_with_h),
        "uncanny_valley": uncanny_valley,
        "sanded_prose": sanded,
        "em_dash_mode": "strict" if strict_em_dash else "default",
    }

    # =========================================================================
    # COMPREHENSION AXIS (parallel to AI-Slop)
    # =========================================================================
    comp = analyze_comprehension(
        text,
        audience=audience,
        sentences=sentences,
        paragraphs=paragraphs,
        total_words=total_words,
    )
    result["comprehension"] = comp

    # Combined cross-axis recommendation
    result["combined_recommendation"] = combined_recommendation(verdict, comp["verdict"])

    return result


# =============================================================================
# OUTPUT FORMATTERS
# =============================================================================

def format_human(result):
    lines = []
    s = result["stats"]
    comp = result.get("comprehension", {})
    lines.append("=" * 70)
    lines.append("SLOP-COP DUAL-AXIS SCAN")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"AI-Slop:        {result['verdict']:<10} (density {result['density']})")
    if comp:
        lines.append(
            f"Comprehension:  {comp['verdict']:<10} (density {comp['density']}) "
            f"[audience: {comp['audience']}]"
        )
    lines.append("")
    rec = result.get("combined_recommendation", "")
    if rec:
        lines.append(f"Combined: {rec}")
    lines.append("")
    lines.append("-" * 70)
    lines.append("AI-SLOP AXIS")
    lines.append("-" * 70)
    lines.append(f"Verdict:           {result['verdict']}")
    lines.append(f"Density score:     {result['density']} per 500w")
    lines.append(
        f"Violations:        {result['totals']['high']}H, "
        f"{result['totals']['medium']}M, {result['totals']['low']}L"
    )
    lines.append("")
    lines.append("--- Stats ---")
    lines.append(f"Words: {s['words']} | Paragraphs: {s['paragraphs']} | Sentences: {s['sentences']}")
    lines.append(f"Sentence avg: {s['sentence_avg']}w | min {s['sentence_min']}w | max {s['sentence_max']}w")
    burst = s["burstiness"]
    burst_str = f"{burst} (humans 0.6-1.2, AI 0.2-0.4)" if burst is not None else "n/a (too few sentences)"
    lines.append(f"Burstiness:        {burst_str}")
    contr = s["contraction_ratio"]
    lines.append(f"Contraction ratio: {contr if contr is not None else 'n/a'}")
    lines.append(f"Detected genre:    {s['detected_genre']}")
    if s["applied_genre"] != s["detected_genre"]:
        lines.append(f"Applied genre:     {s['applied_genre']} (override)")
    lines.append(f"Model fingerprint: {s['model_fingerprint']} {s['fingerprint_counts']}")
    lines.append("")

    # Calibration
    cal = result["calibration"]
    lines.append("--- Calibration ---")
    if cal["compound_escalation"]:
        lines.append("COMPOUND TRIGGER: 3+ H tells in one paragraph — verdict escalated one tier")
    if cal["uncanny_valley"]:
        lines.append("UNCANNY VALLEY: many weak tells stacking with low burstiness")
    if cal["sanded_prose"]:
        lines.append("SANDED-PROSE SIGNATURE: low famous-vocab, high structural — looks prompt-engineered")
    lines.append(f"Em-dash mode: {cal['em_dash_mode']}")
    lines.append("")

    # High severity
    h = result["high"]
    lines.append("--- HIGH SEVERITY ---")
    if h["em_dashes"] or h["en_dashes"] or h["double_hyphens"]:
        lines.append(f"Em/en dashes / double-hyphens: {h['em_dashes']}/{h['en_dashes']}/{h['double_hyphens']}")
    if h["verbs_h"]:
        lines.append("LLM-favored verbs:")
        for phrase, count in h["verbs_h"]:
            lines.append(f"  - \"{phrase}\" ×{count}")
    if h["nouns_h"]:
        lines.append("Cliché metaphors / grandiose nouns:")
        for phrase, count in h["nouns_h"]:
            lines.append(f"  - \"{phrase}\" ×{count}")
    if h["intensifiers_h"]:
        lines.append("Empty intensifiers:")
        for phrase, count in h["intensifiers_h"]:
            lines.append(f"  - \"{phrase}\" ×{count}")
    if h["connectors_h"]:
        lines.append("Closing/connector clichés:")
        for phrase, count in h["connectors_h"]:
            lines.append(f"  - \"{phrase}\" ×{count}")
    if h["sycophancy_open"]:
        lines.append("Sycophancy openers:")
        for pat, count, sample in h["sycophancy_open"]:
            lines.append(f"  - \"{sample}\" ×{count}")
    if h["sycophancy_close"]:
        lines.append("Sycophancy closers:")
        for pat, count, sample in h["sycophancy_close"]:
            lines.append(f"  - \"{sample}\" ×{count}")
    if h["vague_authority_h"]:
        lines.append("Vague-authority weasels:")
        for pat, count, sample in h["vague_authority_h"]:
            lines.append(f"  - \"{sample}\" ×{count}")
    if h["knowledge_cutoff"]:
        lines.append("Knowledge-cutoff disclaimer leakage:")
        for pat, count, sample in h["knowledge_cutoff"]:
            lines.append(f"  - \"{sample}\" ×{count}")
    if h["stake_inflation"]:
        lines.append("Stake inflation / future-flourish:")
        for pat, count, sample in h["stake_inflation"]:
            lines.append(f"  - \"{sample}\" ×{count}")
    if h["grandiose"]:
        lines.append("Grandiose framing:")
        for pat, count, sample in h["grandiose"]:
            lines.append(f"  - \"{sample}\" ×{count}")
    if h["copula_avoidance"]:
        lines.append("Copula avoidance:")
        for pat, count, sample in h["copula_avoidance"]:
            lines.append(f"  - \"{sample}\" ×{count}")
    if h["ing_tails"]:
        lines.append(f"Present-participle '-ing' tails: {len(h['ing_tails'])}")
        for t in h["ing_tails"][:5]:
            lines.append(f"  - \"...{t}...\"")
    if h["throat_clearing"]:
        lines.append("Throat-clearing meta-comments:")
        for pat, count, sample in h["throat_clearing"]:
            lines.append(f"  - \"{sample}\" ×{count}")
    if h["rhetorical_qa"]:
        lines.append(f"Self-posed rhetorical Q+A: {len(h['rhetorical_qa'])}")
    if h["performative_opening"]:
        lines.append(f"Performative opening: \"{h['performative_opening'][0][:80]}\"")
    if h["crafted_closer"]:
        lines.append(f"Crafted closer: \"{h['crafted_closer'][0]}\"")
    if h["setup_reveal_endings"]:
        lines.append("Setup-reveal endings:")
        for idx, sentence, pat in h["setup_reveal_endings"]:
            lines.append(f"  - Para {idx+1}: \"{sentence[:120]}\"")
    if h["fabricated_cases"]:
        lines.append(f"Fabricated case studies: {h['fabricated_cases']}")
    if h["buzzword_density"]:
        lines.append("Buzzword density (3+ in one paragraph):")
        for idx, count, found in h["buzzword_density"]:
            words = ", ".join(f"{w}×{n}" for w, n in found)
            lines.append(f"  - Para {idx+1}: {count} buzzwords ({words})")
    lines.append("")

    # Medium severity
    m = result["medium"]
    lines.append("--- MEDIUM SEVERITY ---")
    # Negation reversals (now in high) — show in high section block instead
    if h.get("negation_reversals"):
        lines.append("Negation reversal candidates (high severity):")
        for idx, sentence, pat in h["negation_reversals"]:
            lines.append(f"  - Sentence {idx+1}: \"{sentence[:120]}\"")
    if h.get("cross_sentence_negation"):
        lines.append("Cross-sentence negation reversal (X isn't Y. It's Z.):")
        for idx, cur, nxt in h["cross_sentence_negation"]:
            lines.append(f"  - \"{cur[:80]}\" → \"{nxt[:80]}\"")
    if h.get("short_sentence_clusters_h"):
        lines.append("Short-sentence clusters (4+ in a row, high severity):")
        for run in h["short_sentence_clusters_h"][:2]:
            for idx, sent, wc in run:
                lines.append(f"  - Sentence {idx+1} ({wc}w): \"{sent[:80]}\"")
    if m.get("short_sentence_clusters_m"):
        lines.append("Short-sentence clusters (3 in a row):")
        for run in m["short_sentence_clusters_m"][:2]:
            for idx, sent, wc in run:
                lines.append(f"  - Sentence {idx+1} ({wc}w): \"{sent[:80]}\"")
    if m["dramatic_countdown"]:
        lines.append("Dramatic countdown candidates:")
        for idx, sents in m["dramatic_countdown"]:
            for s in sents:
                lines.append(f"  - \"{s[:80]}\"")
    if m["anaphora"]:
        lines.append("Anaphora abuse (3+ identical openings):")
        for run in m["anaphora"]:
            lines.append(f"  - {len(run)} consecutive sentences:")
            for idx, sent in run:
                lines.append(f"    \"{sent[:80]}\"")
    if m["two_word_punchlines"]:
        lines.append("Two-word punchline candidates:")
        for idx, sentence, wc, prev in m["two_word_punchlines"]:
            lines.append(f"  - Sentence {idx+1} ({wc}w): \"{sentence}\" after \"{prev}...\"")
    if m["three_beat_stacks"]:
        lines.append(f"Three-beat stack candidates: {len(m['three_beat_stacks'])}")
        for triple in m["three_beat_stacks"][:5]:
            lines.append(f"  - \"{triple[0]}, {triple[1]}, and {triple[2]}\"")
    for label, items in [
        ("LLM-favored verbs (M)", m["verbs_m"]),
        ("Cliché metaphors (M)", m["nouns_m"]),
        ("Empty intensifiers (M)", m["intensifiers_m"]),
        ("Connectors (M)", m["connectors_m"]),
    ]:
        if items:
            lines.append(f"{label}:")
            for phrase, count in items:
                lines.append(f"  - \"{phrase}\" ×{count}")
    if m["hedge_stacking"]:
        lines.append(f"Hedge stacking (3+ hedges in one sentence): {len(m['hedge_stacking'])}")
        for idx, sent, count in m["hedge_stacking"][:3]:
            lines.append(f"  - {count} hedges: \"{sent[:120]}\"")
    if m["hedged_superlatives"]:
        lines.append("Hedged superlatives:")
        for pat, count, sample in m["hedged_superlatives"]:
            lines.append(f"  - \"{sample}\" ×{count}")
    if m["while_openers"] >= 2:
        lines.append(f"'While X, Y' openers: {m['while_openers']} (pattern emerges at >2)")
    if m["x_meets_y"]:
        lines.append(f"'X meets Y' formula: {m['x_meets_y']}")
    if m["more_than_just"]:
        lines.append(f"'More than just X' formula: {m['more_than_just']}")
    if m["false_range"]:
        lines.append(f"False range ('From X to Y'): {m['false_range']}")
    if m["false_concession"]:
        lines.append("False concession openers:")
        for pat, count, sample in m["false_concession"]:
            lines.append(f"  - \"{sample}\" ×{count}")
    if m["pedagogical"]:
        lines.append("Pedagogical voice:")
        for pat, count, sample in m["pedagogical"]:
            lines.append(f"  - \"{sample}\" ×{count}")
    if m["royal_we"]:
        lines.append("Royal-we / 'as a society':")
        for pat, count, sample in m["royal_we"]:
            lines.append(f"  - \"{sample}\" ×{count}")
    if m["whether_or_openers"]:
        lines.append(f"'Whether you're X or Y' openers: {m['whether_or_openers']}")
    lines.append("")

    # Low severity
    l = result["low"]
    lines.append("--- LOW SEVERITY ---")
    if l["magic_adverbs"]:
        lines.append("Magic adverbs:")
        for adv, count in l["magic_adverbs"]:
            note = " (survives only when contrasting reality with theory)" if adv == "actually" else ""
            lines.append(f"  - \"{adv}\" ×{count}{note}")
    if l["bigram_repetition"]:
        lines.append(f"Bigram repetition (5+ uses): {len(l['bigram_repetition'])}")
        for bg, count in l["bigram_repetition"][:5]:
            lines.append(f"  - \"{bg[0]} {bg[1]}\" ×{count}")
    if l["markdown_tells"]:
        lines.append("Markdown / formatting tells:")
        for tell, val in l["markdown_tells"].items():
            lines.append(f"  - {tell}: {val}")
    lines.append("")

    # ===========================================================================
    # COMPREHENSION AXIS section
    # ===========================================================================
    if comp:
        lines.append("-" * 70)
        lines.append("COMPREHENSION AXIS")
        lines.append("-" * 70)
        lines.append(f"Verdict:           {comp['verdict']}")
        lines.append(f"Density score:     {comp['density']} per 500w")
        lines.append(
            f"Violations:        {comp['totals']['high']}H, "
            f"{comp['totals']['medium']}M, {comp['totals']['low']}L"
        )
        lines.append(f"Audience:          {comp['audience']}")
        if comp.get("audience_adjustment"):
            lines.append(f"Audience tweak:    {comp['audience_adjustment']}")
        if comp.get("escalations"):
            lines.append("Compound triggers (escalated one tier):")
            for esc in comp["escalations"]:
                lines.append(f"  - {esc}")
        lines.append("")

        # Readability metric panel
        m = comp.get("metrics", {})
        if m and m.get("flesch_reading_ease") is not None:
            lines.append("--- Readability metrics panel ---")
            tgt = comp.get("audience_targets", {})
            fre = m["flesch_reading_ease"]
            fre_tag = "" if fre >= tgt.get("flesch_min", 60) else "  (below target)"
            lines.append(f"Flesch Reading Ease:    {fre}{fre_tag} (target ≥{tgt.get('flesch_min', 60)})")
            fkgl = m["flesch_kincaid_grade"]
            fk_tag = "" if fkgl <= tgt.get("fk_max", 9) else "  (above target)"
            lines.append(f"Flesch-Kincaid Grade:   {fkgl}{fk_tag} (target ≤{tgt.get('fk_max', 9)})")
            lines.append(f"SMOG Index:             {m['smog']}")
            lines.append(f"Coleman-Liau Index:     {m['coleman_liau']}")
            lines.append(f"Dale-Chall Score:       {m['dale_chall']} ({m['difficult_word_pct']}% difficult)")
            lex = m["lexical_density"]
            lex_tag = "" if lex <= tgt.get("lex_max", 55) else "  (above target)"
            lines.append(f"Lexical density:        {lex}%{lex_tag} (target ≤{tgt.get('lex_max', 55)}%)")
            asl = m["avg_sentence_length"]
            asl_tag = "" if asl <= tgt.get("sent_max", 18) else "  (above target)"
            lines.append(f"Avg sentence length:    {asl}w (stddev {m['sentence_length_stddev']}){asl_tag} (target ≤{tgt.get('sent_max', 18)}w)")
            pv = m["passive_voice_pct"]
            pv_tag = "" if pv <= tgt.get("passive_max", 10) else "  (above target)"
            lines.append(f"Passive voice:          {pv}%{pv_tag} (target ≤{tgt.get('passive_max', 10)}%)")
            lines.append("")

        # Density signals
        p = comp.get("patterns", {})
        lines.append("--- Density signals ---")
        f1 = p.get("F1_undefined_acronyms", {})
        lines.append(f"Acronym density:        {f1.get('density_per_100w', 0)} per 100w (threshold 3+, count {f1.get('total_count', 0)})")
        f2 = p.get("F2_named_entities", {})
        lines.append(f"Named-entity density:   {f2.get('density_per_100w', 0)} per 100w (threshold 5+, count {f2.get('total_count', 0)})")
        sb = p.get("F3_stat_bombing", [])
        max_num = max((c for _, _, c in sb), default=0) if sb else 0
        lines.append(f"Stat-bombed sentences:  {len(sb)} (max numerics in one sentence: {max_num})")
        col = p.get("G1_telegraphic_colons", [])
        max_col = max((c for _, c, _ in col), default=0) if col else 0
        lines.append(f"Telegraphic colon-labels: {len(col)} paragraphs flagged (max in one paragraph: {max_col})")
        wt = p.get("F4_wall_of_text", [])
        max_para_w = max((w for _, _, w, _ in wt), default=0) if wt else 0
        lines.append(f"Wall-of-text paragraphs: {len(wt)} (max paragraph words: {max_para_w})")
        lines.append("")

        # H severity hits
        lines.append("--- HIGH SEVERITY (comprehension) ---")
        if f1.get("total_count", 0) > 0:
            lines.append(f"Undefined acronyms ({f1['total_count']} total, {f1['distinct_count']} distinct):")
            for ac, cnt in f1["acronyms"][:8]:
                lines.append(f"  - {ac} ×{cnt}")
        if f2.get("total_count", 0) > 0:
            lines.append(f"Named entities without context ({f2['total_count']} total):")
            for ent, cnt in f2["entities"][:8]:
                lines.append(f"  - {ent} ×{cnt}")
        if sb:
            lines.append(f"Stat-bombed sentences (3+ numerics):")
            for idx, sample, n in sb[:5]:
                lines.append(f"  - Sentence {idx+1} ({n} numerics): \"{sample}\"")
        if col:
            lines.append(f"Telegraphic colon-labeling paragraphs:")
            for idx, n, labels in col[:3]:
                lines.append(f"  - Para {idx+1} ({n} colons): {labels[:3]}")
        ls = p.get("G3_long_sentences", [])
        if ls:
            lines.append(f"Long sentences (>30 words): {len(ls)}")
            for idx, wc, sample in ls[:3]:
                lines.append(f"  - Sentence {idx+1} ({wc}w): \"{sample}\"")
        ro = p.get("G4_runon_sentences", [])
        if ro:
            lines.append(f"Run-on sentences (4+ clauses): {len(ro)}")
            for idx, n, sample in ro[:3]:
                lines.append(f"  - Sentence {idx+1} ({n} clauses): \"{sample}\"")
        fr = p.get("H5_forward_references", [])
        if fr:
            lines.append("Forward references:")
            for pat, cnt, sample in fr:
                lines.append(f"  - \"{sample}\" ×{cnt}")
        dnh = p.get("F5_density_no_headings", {})
        if dnh.get("flagged"):
            lines.append(f"Density-without-headings: {dnh.get('reason')}")

        # M severity hits
        lines.append("")
        lines.append("--- MEDIUM SEVERITY (comprehension) ---")
        if wt:
            lines.append(f"Wall-of-text paragraphs ({len(wt)}):")
            for idx, sc, wc, sample in wt[:3]:
                lines.append(f"  - Para {idx+1} ({sc} sentences, {wc} words): \"{sample}\"")
        lp = p.get("G2_list_as_prose", [])
        if lp:
            lines.append(f"List-pretending-to-be-prose paragraphs: {len(lp)}")
            for idx, semi, plus, sample in lp[:3]:
                lines.append(f"  - Para {idx+1} ({semi} semicolons, {plus} plus signs): \"{sample}\"")
        sk = p.get("I9_no_skim_layer", {})
        if sk.get("flagged"):
            lines.append(f"No skim layer: 0 bold/strong markers in {sk.get('words')} words")
        hc = p.get("I5_hierarchy_collapse", [])
        if hc:
            lines.append(f"Hierarchy collapse (heading skips): {len(hc)}")
            for skip in hc[:3]:
                lines.append(f"  - H{skip['from_level']} → H{skip['to_level']}: \"{skip['from']}\" → \"{skip['to']}\"")
        pf = p.get("I12_parallelism_failure", [])
        if pf:
            lines.append(f"Parallelism failure in lists: {len(pf)} blocks")
            for blk in pf[:2]:
                lines.append(f"  - {blk['block_size']} bullets, mixed forms: {blk['forms']}")
        pv_data = p.get("J1_passive_voice", {})
        if pv_data.get("percent", 0) > 10:
            lines.append(f"Passive voice excess: {pv_data['percent']}% (threshold 10%)")
        nm = p.get("J2_nominalizations", {})
        if nm.get("density_per_100w", 0) > 5:
            lines.append(f"Nominalization density: {nm['density_per_100w']} per 100w (threshold 5)")
            if nm.get("examples"):
                lines.append(f"  - examples: {nm['examples'][:6]}")
        hs = p.get("J4_hedge_stacking", [])
        if hs:
            lines.append(f"Hedge stacking (3+ hedges/sentence): {len(hs)}")
            for idx, sent, n in hs[:2]:
                lines.append(f"  - {n} hedges: \"{sent[:120]}\"")

        # L severity hits
        lines.append("")
        lines.append("--- LOW SEVERITY (comprehension) ---")
        gw = p.get("G5_glue_word_starts", [])
        if gw:
            lines.append(f"Glue-word sentence starts: {len(gw)}")
            for idx, sample, _ in gw[:3]:
                lines.append(f"  - Sentence {idx+1}: \"{sample}\"")
        dq = p.get("J5_decorative_qualifiers", {})
        if dq.get("density_per_100w", 0) > 2:
            lines.append(
                f"Decorative qualifiers: {dq['count']} ({dq['density_per_100w']} per 100w; threshold 2)"
            )
            if dq.get("examples"):
                lines.append(f"  - examples: {dq['examples'][:6]}")
        nc = p.get("J8_negative_constructions", [])
        if nc:
            lines.append(f"Negative constructions: {sum(c for _, c, _ in nc)} occurrences")
            for pat, cnt, sample in nc[:3]:
                lines.append(f"  - \"{sample}\" ×{cnt}")
        lines.append("")

    lines.append("=" * 70)
    lines.append("Note: scanner catches mechanical violations only.")
    lines.append("Qualitative patterns (the actual force of metaphors, real-vs-")
    lines.append("decorative judgment, voice consistency, missing thesis,")
    lines.append("curse of knowledge) require reading.")
    lines.append("=" * 70)
    return "\n".join(lines)


def format_quick(result):
    """Compact one-screen output for embedding in other skills."""
    lines = []
    comp = result.get("comprehension", {})
    if comp:
        lines.append(
            f"AI-Slop: {result['verdict']} (density {result['density']}) | "
            f"Comprehension: {comp['verdict']} (density {comp['density']})"
        )
    else:
        lines.append(f"Verdict: {result['verdict']} (density {result['density']})")
    lines.append(
        f"AI-Slop violations: {result['totals']['high']}H, "
        f"{result['totals']['medium']}M, {result['totals']['low']}L"
    )
    if comp:
        lines.append(
            f"Comp violations:    {comp['totals']['high']}H, "
            f"{comp['totals']['medium']}M, {comp['totals']['low']}L "
            f"[audience: {comp['audience']}]"
        )
    burst = result["stats"]["burstiness"]
    lines.append(f"Burstiness: {burst if burst is not None else 'n/a'}")
    lines.append(f"Genre: {result['stats']['detected_genre']} | Fingerprint: {result['stats']['model_fingerprint']}")
    if result.get("combined_recommendation"):
        lines.append(f"Combined: {result['combined_recommendation']}")

    # Top fixes — pick the highest-count items
    fixes = []
    for phrase, count in result["high"]["verbs_h"][:2]:
        fixes.append(f"\"{phrase}\" ×{count}")
    for phrase, count in result["high"]["nouns_h"][:1]:
        fixes.append(f"\"{phrase}\" ×{count}")
    for phrase, count in result["high"]["intensifiers_h"][:1]:
        fixes.append(f"\"{phrase}\" ×{count}")
    if result["high"]["em_dashes"]:
        fixes.append(f"em dashes ×{result['high']['em_dashes']}")
    if result["high"]["sycophancy_open"]:
        fixes.append("opener sycophancy")
    if result["high"]["sycophancy_close"]:
        fixes.append("closer sycophancy")
    # Comprehension fixes
    if comp:
        cp = comp.get("patterns", {})
        f1 = cp.get("F1_undefined_acronyms", {})
        if f1.get("total_count", 0) >= 3:
            fixes.append(f"undefined acronyms ×{f1['total_count']}")
        f2 = cp.get("F2_named_entities", {})
        if f2.get("total_count", 0) >= 5:
            fixes.append(f"named-entity bombing ×{f2['total_count']}")
        ls = cp.get("G3_long_sentences", [])
        if ls:
            fixes.append(f"long sentences ×{len(ls)}")
        col = cp.get("G1_telegraphic_colons", [])
        if col:
            fixes.append(f"telegraphic colon-labels ×{len(col)}")
        ro = cp.get("G4_runon_sentences", [])
        if ro:
            fixes.append(f"run-on sentences ×{len(ro)}")
    if fixes:
        lines.append("Top fixes: " + ", ".join(fixes[:5]))
    return "\n".join(lines)


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="slop-cop dual-axis scanner — AI-slop + comprehension."
    )
    parser.add_argument("path", nargs="?", help="Path to a text/markdown file. Reads stdin if omitted.")
    parser.add_argument("--json", action="store_true", help="Output structured JSON.")
    parser.add_argument("--quick", action="store_true", help="Compact one-screen output.")
    parser.add_argument(
        "--genre",
        choices=["casual", "marketing", "academic", "encyclopedic", "fiction"],
        help="Override detected genre. Adjusts AI-slop severity thresholds per calibration.md §3.",
    )
    parser.add_argument(
        "--audience",
        choices=["casual", "marketing", "academic", "encyclopedic", "technical", "fiction", "healthcare"],
        default="casual",
        help="Audience for the comprehension axis. Adjusts metric targets per calibration.md §10. Default: casual.",
    )
    parser.add_argument(
        "--strict-em-dash",
        action="store_true",
        help="Treat ALL em dashes as H severity (Mahmoud-mode). Default: clusters only.",
    )
    args = parser.parse_args()

    if args.path:
        try:
            text = Path(args.path).read_text(encoding="utf-8")
        except FileNotFoundError:
            print(f"File not found: {args.path}", file=sys.stderr)
            sys.exit(1)
    else:
        text = sys.stdin.read()

    if not text.strip():
        print("Empty input.", file=sys.stderr)
        sys.exit(1)

    result = analyze(
        text,
        genre=args.genre,
        strict_em_dash=args.strict_em_dash,
        audience=args.audience,
    )

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    elif args.quick:
        print(format_quick(result))
    else:
        print(format_human(result))


if __name__ == "__main__":
    main()
