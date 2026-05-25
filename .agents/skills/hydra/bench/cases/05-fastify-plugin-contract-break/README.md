# Case 05 — Fastify Plugin Contract Break

The diff converts a callback-style `onRequest` hook to an `async` function
while keeping the `done` parameter in the signature. In Fastify, if `done`
is declared as a parameter the framework expects it to be called; when it
is not, Fastify waits indefinitely, hanging every incoming request. The
misleading comment in the diff ("done() must not be called") creates a
false sense of correctness while violating the plugin contract.

**Ground truth:** 1 MODERATE finding (`api_break`).
**Category:** api.
**Expected position:** CONCERN.
