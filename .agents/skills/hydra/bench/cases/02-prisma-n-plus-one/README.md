# Case 02 — Prisma N+1 Query

A refactor replaces a single `findMany({ include: { posts: true } })` call
with a loop that issues one `prisma.post.findMany()` per user. For N users
this produces N+1 database round trips instead of 1, causing severe
throughput degradation under any meaningful load.

**Ground truth:** 1 MODERATE finding (`performance_degradation`).
**Category:** perf.
**Expected position:** CONCERN.
