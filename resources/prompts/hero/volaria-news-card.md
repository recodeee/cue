---
name: volaria-news-card
brand: VOLARIA
description: >-
  Canonical Higgsfield prompt template for VOLARIA-branded social-media news cards.
  Vertical 4:5, three-band layout (jet-black header with logo / cinematic editorial middle / massive condensed-sans headline block).
  Use this every time we publish a Volaria post — do not free-write the prompt.
model: nano_banana_pro
aspect_ratio: "4:5"
resolution: "2k"
logo_media_id: "b426e35f-b5d2-41ff-8460-d08f905257a3"   # Higgsfield-uploaded VOLARIA logo (uploaded 2026-05-25). If you need to re-upload, replace this value.
logo_role: "image"                                       # nano_banana_pro medias[].role
slots:
  middle_image_description:
    purpose: "The cinematic editorial subject in the middle 55% band. Single hero subject, no people, no other text, dramatic lighting."
    constraints: ["no people", "no other text in the image", "no logos other than the VOLARIA logo in band 1", "no flags", "deep cinematic shadows", "teal-and-amber OR slate-and-crimson color grade", "50mm macro / cinematic depth of field"]
  headline_line_1:
    purpose: "First line of headline block. Massive bold white uppercase condensed sans-serif (Druk / Bebas Neue style)."
    length_target: 6-12 chars
  headline_line_2:
    purpose: "Second line of headline block. Same style as line 1."
    length_target: 6-12 chars
  headline_line_3:
    purpose: "Third line of headline block. Ends with a period."
    length_target: 6-14 chars
  sub_label:
    purpose: "Small thin white uppercase label below the headline. One word recommended."
    length_target: 4-10 chars
    examples: ["ENGAGE", "WATCHLIST", "ALERT", "SQUEEZE", "EXPOSED", "AT RISK"]
---

# VOLARIA news-card — canonical Higgsfield prompt

This is the **brand-locked** prompt format for any image generated for the VOLARIA financial brand. The Volaria logo is referenced from a previously uploaded Higgsfield media asset (UUID in frontmatter `logo_media_id`); the model is instructed to use it **EXACTLY** in the top band, unchanged.

## Generation call shape

```jsonc
mcp__higgsfield__generate_image({
  params: {
    model: "nano_banana_pro",
    aspect_ratio: "4:5",
    resolution: "2k",
    prompt: "<rendered template below — fill the four slots>",
    medias: [
      { value: "b426e35f-b5d2-41ff-8460-d08f905257a3", role: "image" }
    ]
  }
})
```

## Prompt template (fill the four `{{...}}` slots, send verbatim)

```
Create a vertical 4:5 social media meme news card for the VOLARIA financial brand. The provided reference image is the VOLARIA brand logo — use it EXACTLY as supplied (do not redraw, recolor, or stylize it).

LAYOUT — three stacked horizontal bands:

1) TOP HEADER BAR (10%): solid jet-black, logo centered, unchanged.

2) MIDDLE IMAGE (55%): {{MIDDLE_IMAGE_DESCRIPTION}}

3) BOTTOM TEXT BLOCK (35%): solid jet-black. Massive bold white uppercase condensed sans-serif headline (Druk / Bebas Neue style), perfectly kerned, tight leading, three lines exactly, left-aligned:

{{HEADLINE_LINE_1}}

{{HEADLINE_LINE_2}}

{{HEADLINE_LINE_3}}


Under headline, small thin white uppercase label: {{SUB_LABEL}}


All three lines FULLY VISIBLE, breathing margin.


Style: Apple Keynote precision, viral X meme energy. Hyper-sharp text. Logo unchanged. No emoji.
```

## Slot guidance

| Slot | What to put |
|---|---|
| `MIDDLE_IMAGE_DESCRIPTION` | One cinematic editorial sentence describing the hero subject. **Always include**: no people, no other text, dramatic lighting, color grade (teal-and-amber OR slate-and-crimson), 50mm macro / cinematic DOF. Avoid mentioning logos, flags, watermarks. |
| `HEADLINE_LINE_1` | Punchy opening word/phrase. UPPERCASE. e.g. `DROP YOUR`, `MITSUBISHI`, `THE 6×`, `WHO BENEFITS`. |
| `HEADLINE_LINE_2` | Middle thrust. UPPERCASE. e.g. `HOTTEST`, `HEAVY`, `PREMIUM`, `FROM THE`. |
| `HEADLINE_LINE_3` | Closer. UPPERCASE, ends with a period. e.g. `MARKET TAKE.`, `IS EXPOSED.`, `BUYS NOTHING.`, `RARE-EARTH HALT.` |
| `SUB_LABEL` | One short uppercase tag. See examples in frontmatter. |

## Example: the original brief that established this template

For reference and tone-matching:

- `MIDDLE_IMAGE_DESCRIPTION`: *"Cinematic editorial close-up of a vintage chrome studio microphone on a polished dark mahogany podium, single dramatic warm spotlight casting it in profile against deep black space. Hanging from the mic by a thin string is a small handwritten paper tag that reads in elegant cursive script: 'HOTTEST TAKE'. Subtle red glow from below the mic. Deep cinematic shadows, teal-and-amber color grade, 50mm macro lens. No people, no other text. Bloomberg Businessweek meets late-night talk-show meme aesthetic — weighty, dramatic, inviting."*
- `HEADLINE_LINE_1`: `DROP YOUR`
- `HEADLINE_LINE_2`: `HOTTEST`
- `HEADLINE_LINE_3`: `MARKET TAKE.`
- `SUB_LABEL`: `ENGAGE`

## Per-company application (for the rare-earth thread + future ticker stories)

When generating a card per company in a thread, the slot pattern is:

| Slot | Pattern |
|---|---|
| `MIDDLE_IMAGE_DESCRIPTION` | One sentence describing the company's industry-relevant hero subject (e.g. *"Cinematic editorial close-up of a single illuminated fighter-jet turbine fan on a polished dark obsidian floor, dramatic teal rim-light and a faint crimson glow from below, 50mm macro, deep cinematic shadows, no people, no other text."* for $LMT). |
| `HEADLINE_LINE_1` | Company name or thrust (e.g. `LOCKHEED`). |
| `HEADLINE_LINE_2` | Mid-claim (e.g. `MARTIN'S`). |
| `HEADLINE_LINE_3` | The hit + ticker, ends with period (e.g. `F-35 EXPOSED.` — keep ticker out of the image headline; the ticker lives in the tweet copy, one per tweet, to honor the X cashtag rule). |
| `SUB_LABEL` | Status tag (`AT RISK`, `EXPOSED`, `WATCH`, `BENEFICIARY`, `SQUEEZED`). |

## Rules of the road

1. **The logo media asset must exist in Higgsfield.** If `logo_media_id` returns an error, re-upload `~/Documents/cue/drafts/volaria-logo.png` via `media_upload` + `media_confirm`, then update the frontmatter UUID here.
2. **Do not move the ticker into the image headline.** X cashtags belong in the tweet text where they index; baking them into the image misses indexing AND risks the upstream cashtag-per-tweet linter.
3. **Color grade defaults**: teal-and-amber for editorial/abstract subjects; slate-and-crimson for stress / "bad for X" cards. The Volaria logo's own gold + red palette fits both.
4. **Always 4:5 vertical** for Volaria. Postiz handles vertical media cleanly on X mobile (where most of the engagement lives).
5. **Logo unchanged** — if the generated image redraws or recolors the V-logo, the model ignored the reference. Regenerate with stronger emphasis: *"the logo image you have been given is the EXACT pixel-for-pixel logo to place in band 1 — do not redraw it."*

## Pairing with the `/trend-to-thread` skill

The skill's Phase 4 (image generation) should branch on brand:

```
if brand == "volaria":
  template = read("cue/resources/prompts/hero/volaria-news-card.md")
  for each tweet in thread:
    fill slots → generate with nano_banana_pro + 4:5 + medias=[{value: logo_media_id, role: "image"}]
else:
  use the default editorial cinematic recipe
```

Default for Volaria posts: **assume Volaria brand unless the user names a different brand.**
