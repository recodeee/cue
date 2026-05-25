from bench.runner.extract_findings import extract_from_report

SAMPLE_REPORT = """---
hydra_version: "1.0"
severity_counts:
  critical: 0
  serious: 1
  moderate: 0
top_actions:
  - id: A1
    severity: SERIOUS
    file: src/interceptors/auth.ts
    lines: 14-28
    effort: small
    summary: Unvalidated Authorization header forwarded
---

## Verdict
REQUEST CHANGES: one SERIOUS finding unresolved.

## Actions

### A1 — Unvalidated Authorization header forwarded
**What:** Forwarded without validation.
**Severity:** SERIOUS
**File:** src/interceptors/auth.ts:14-28
"""


def test_extract_from_report_yields_top_actions() -> None:
    findings = extract_from_report(SAMPLE_REPORT)
    assert len(findings) == 1
    f = findings[0]
    assert f["file"] == "src/interceptors/auth.ts"
    assert f["lines"] == "14-28"
    assert f["severity"] == "SERIOUS"
    assert "Authorization" in f["title"]
