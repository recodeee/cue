# X (Twitter) — Cashtag Limit

## Rule

**An X tweet may contain at most ONE `$SYMBOL` cashtag.** A second `$` followed by a ticker on the same tweet causes the publish to fail.

Applies to: every single tweet in a thread (the limit is per-tweet, not per-thread). The first tweet, every reply, and the final ticker-shoutout all count separately.

## Why

Upstream X API constraint (v2 `POST /2/tweets`). Postiz surfaces this with:

```
ApplicationFailure: There can be maximum of one cashtag ($SYMBOL) per post
```

The detection lives in `libraries/nestjs-libraries/src/integrations/social/x.provider.ts` → `handleErrors`, matching the substring `'maximum of one cashtag'`. The orchestrator then marks the post `nonRetryable` — automatic retries will NOT recover it; the content must be edited and the workflow re-triggered.

## How to apply

When drafting, scheduling, or editing X posts:

1. **Scan every tweet for `$<TICKER>` patterns.** Count them; if >1 in a single tweet, that tweet will fail.
2. **Prefer plain ticker + one cashtag.** Example:
   - ❌ `Watch $SPY $QQQ today`
   - ✅ `Watch $SPY and QQQ today`  *(only $SPY is a cashtag)*
3. **Or split across thread parts** — one cashtag per tweet:
   - Tweet 4: `… $SPY`
   - Tweet 5: `… $QQQ`
4. **Same constraint applies to scheduled posts in `Post.content`.** Editing a row that already failed needs:
   - Update `content` to remove the extra cashtag
   - Re-trigger via Postiz UI "republish" (the temporal workflow ended `nonRetryable`; DB state alone won't restart it)

## Related

- Same provider's `handleErrors` also catches `'maximum of 4 items'` (media attachment cap) and `'Unsupported Authentication'` (token expiry) — those are separate constraints.
- Cashtag detection is on the X side, not Postiz. Other platforms (LinkedIn, Threads, Bluesky) do not enforce this.
