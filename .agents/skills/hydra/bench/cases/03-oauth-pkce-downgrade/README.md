# Case 03 — OAuth PKCE Downgrade

The diff downgrades `code_challenge_method` from `S256` to `plain` and
removes the local `code_verifier` hash comparison in the callback handler.
With `plain`, the challenge equals the verifier verbatim, so an intercepted
authorization code combined with a guessed or observed verifier lets an
attacker complete the OAuth flow without the original client secret.

**Ground truth:** 1 SERIOUS finding (`auth_bypass`).
**Category:** security.
**Expected position:** REJECT.
