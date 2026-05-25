# Case 01 — Axios Header Injection

A trusted HTTP client forwards the caller's `Authorization` header
verbatim to a downstream service without validating the scheme or
confirming the caller is entitled to forward credentials.

**Ground truth:** 1 SERIOUS finding (`auth_bypass`).
**Category:** security.
**Expected position:** REJECT.
