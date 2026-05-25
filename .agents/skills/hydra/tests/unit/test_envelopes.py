import json

import pytest

from hydra.envelopes import (
    AdvisorFinding,
    Chain,
    GroundingStatus,
    IssueClass,
    Position,
    RunConfig,
    SeedReport,
    Severity,
    StructuralContext,
)


def test_run_config_round_trip() -> None:
    cfg = RunConfig(
        mode="deep",
        profile="quality",
        focus=None,
        allow_broken=False,
        tensions_only=False,
        resolved_models={"cassandra": "claude-opus-4-7"},
        run_nonce="abc123",
        config_hash="sha256:" + "0" * 64,
    )
    blob = cfg.model_dump_json()
    cfg2 = RunConfig.model_validate_json(blob)
    assert cfg == cfg2


def test_seed_report_byte_identical_serialization() -> None:
    sr = SeedReport(
        schema_version="2.0",
        generated_at="2026-04-17T14:30:00Z",
        run_nonce="abc123",
        tool_findings=[],
        echo_findings=[],
        navigator_findings=[],
        structural_context=StructuralContext(file_tree=[], boundaries=[], import_observations=[]),
        skipped_tools=[],
        warnings=[],
    )
    b1 = sr.canonical_json()
    b2 = sr.canonical_json()
    assert b1 == b2
    # sort_keys=True enforced
    parsed = json.loads(b1)
    assert list(parsed.keys()) == sorted(parsed.keys())


def test_advisor_finding_has_required_fields() -> None:
    f = AdvisorFinding(
        id="C-1",
        title="Race in refresh",
        severity=Severity.SERIOUS,
        evidence="VERIFIED",
        position=Position.CONCERN,
        file="auth.ts",
        lines="47-62",
        issue_class=IssueClass.race_condition,
        chain=Chain(
            premise="single concurrent request",
            execution_trace="req1 → refreshToken() → req2 → refreshToken()",
            conclusion="second overwrites first",
        ),
        extends_seed=["T-SEM-3"],
        challenges_seed=[],
        novel=False,
    )
    assert f.grounding == GroundingStatus.UNKNOWN  # default pre-grounding
    assert f.is_tension is False


def test_run_config_rejects_bad_nonce() -> None:
    import pytest
    from pydantic import ValidationError
    with pytest.raises(ValidationError, match="run_nonce"):
        RunConfig(
            mode="deep", profile="quality", focus=None,
            allow_broken=False, tensions_only=False,
            resolved_models={},
            run_nonce="ZZZZZZ",  # not hex
            config_hash="sha256:" + "0" * 64,
        )


def test_run_config_rejects_bad_config_hash() -> None:
    from pydantic import ValidationError
    with pytest.raises(ValidationError, match="config_hash"):
        RunConfig(
            mode="deep", profile="quality", focus=None,
            allow_broken=False, tensions_only=False,
            resolved_models={},
            run_nonce="abcdef",
            config_hash="not-a-hash",
        )


def _make_seed_report(generated_at: str = "2026-01-01T00:00:00Z") -> SeedReport:
    return SeedReport(
        schema_version="2.0",
        generated_at=generated_at,
        run_nonce="abcdef",
        tool_findings=[],
        echo_findings=[],
        navigator_findings=[],
        structural_context=StructuralContext(),
        skipped_tools=[],
        warnings=[],
    )


def test_canonical_json_byte_stable_across_runs_with_different_timestamps() -> None:
    # Spec §4.3.1 L210: "No timestamps / run_ids inside cached blocks; put
    # them in uncached tail." Two SeedReports with identical logical content
    # but different generated_at MUST produce identical canonical bytes,
    # otherwise BP4 cache hit-rate goes to 0% (release-blocker per spec L216).
    sr_old = _make_seed_report(generated_at="2026-01-01T00:00:00Z")
    sr_new = _make_seed_report(generated_at="2099-12-31T23:59:59Z")
    assert sr_old.canonical_json() == sr_new.canonical_json(), (
        "canonical_json must not include generated_at — see A2-F9 finding"
    )


def test_canonical_json_keys_sorted_under_kwargs_reorder() -> None:
    # R3 thought-experiment: a patch silently dropping sort_keys=True would
    # pass every existing test if dict insertion order happens to match
    # alphabetical. Construct with deliberately reversed kwarg order to
    # break that coincidence and force the sort.
    sr = SeedReport(
        warnings=[],
        skipped_tools=[],
        structural_context=StructuralContext(),
        navigator_findings=[],
        echo_findings=[],
        tool_findings=[],
        run_nonce="abcdef",
        generated_at="2026-01-01T00:00:00Z",
        schema_version="2.0",
    )
    parsed = json.loads(sr.canonical_json())
    keys = list(parsed.keys())
    assert keys == sorted(keys), f"canonical_json keys not sorted: {keys}"


def test_canonical_exclude_is_frozenset() -> None:
    """S-N4: prevent runtime mutation that would silently change cache keys."""
    from hydra.envelopes import _CANONICAL_EXCLUDE
    assert isinstance(_CANONICAL_EXCLUDE, frozenset)
    with pytest.raises(AttributeError):
        _CANONICAL_EXCLUDE.add("smuggled_field")  # type: ignore[attr-defined]


def test_canonical_json_idempotent_on_repeated_call() -> None:
    # Sanity check that two calls on the same object return identical bytes.
    # If this ever breaks, the bug is in `model_dump(mode='json')`
    # nondeterminism, not in the F9 timestamp issue.
    sr = _make_seed_report()
    assert sr.canonical_json() == sr.canonical_json()


def test_canonical_json_excludes_generated_at_field() -> None:
    # Defense-in-depth: explicitly assert the excluded field name is NOT in
    # the canonical bytes, even as a substring. Prevents a future refactor
    # that accidentally re-introduces the field via a different code path.
    sr = _make_seed_report(generated_at="2026-04-27T11:42:00Z")
    assert b"generated_at" not in sr.canonical_json()
    assert b"2026-04-27" not in sr.canonical_json()


def test_advisor_finding_rejects_unknown_keys() -> None:
    # M2: extra='forbid' must reject keys that don't match the schema.
    # Defends against advisor (or tampered cached envelope) injection of
    # extra JSON fields that would silently propagate through chairman.
    from pydantic import ValidationError
    payload = {
        "id": "C-1",
        "title": "x",
        "severity": "SERIOUS",
        "evidence": "VERIFIED",
        "position": "CONCERN",
        "chain": {"premise": "", "execution_trace": "", "conclusion": ""},
        "smuggled_key": "evil-payload",  # extra — must be rejected
    }
    with pytest.raises(ValidationError, match="smuggled_key|Extra"):
        AdvisorFinding.model_validate(payload)


def test_seed_report_rejects_unknown_keys() -> None:
    from pydantic import ValidationError
    payload = {
        "schema_version": "2.0",
        "generated_at": "2026-01-01T00:00:00Z",
        "run_nonce": "abcdef",
        "extra_field": "evil",
    }
    with pytest.raises(ValidationError, match="extra_field|Extra"):
        SeedReport.model_validate(payload)


def test_chain_rejects_unknown_keys() -> None:
    # V2 follow-up: pydantic's extra='forbid' on AdvisorFinding does NOT
    # propagate to nested Chain. Without forbid on Chain itself, an attacker
    # controlling cached AdvisorFinding JSON could smuggle keys via
    # {"chain":{...,"smuggled":"x"}} and have them silently accepted.
    from pydantic import ValidationError
    with pytest.raises(ValidationError, match="smuggled|Extra"):
        Chain.model_validate({
            "premise": "p", "execution_trace": "e", "conclusion": "c",
            "smuggled": "evil",
        })


def test_canonical_json_byte_snapshot() -> None:
    # V2 follow-up — regression guard against forgetting to add a newly added
    # volatile field to _CANONICAL_EXCLUDE. Golden bytes-hash for a fixed
    # SeedReport shape; ANY change to canonical_json (new field, removed
    # field, type change, sort_keys drop, generated_at re-included) flips
    # this hash and forces a deliberate update gesture.
    #
    # When this test fails: (1) examine the diff for intent, (2) if a new
    # field is per-run volatile (timestamp / request id / nonce), add it to
    # _CANONICAL_EXCLUDE in envelopes.py BEFORE updating this hash; (3)
    # otherwise update the hash with the new value.
    import hashlib

    sr = SeedReport(
        schema_version="2.0",
        generated_at="2026-04-27T11:42:00Z",  # MUST be excluded from canonical
        run_nonce="deadbe",
        tool_findings=[],
        echo_findings=[],
        navigator_findings=[],
        structural_context=StructuralContext(),
        skipped_tools=[],
        warnings=[],
    )
    from hydra.envelopes import _CANONICAL_EXCLUDE
    actual = hashlib.sha256(sr.canonical_json()).hexdigest()
    expected = "00cf490b07e3a23893d1903f7af11e7033188a48d7a6aae309784c69997f1e5f"
    assert actual == expected, (
        f"canonical_json byte snapshot changed.\n"
        f"  expected:  {expected}\n"
        f"  actual:    {actual}\n"
        f"  bytes:     {sr.canonical_json()!r}\n"
        f"  excludes:  {sorted(_CANONICAL_EXCLUDE)}\n"
        f"To update: paste the `actual` value above into `expected` in this "
        f"test (tests/unit/test_envelopes.py). If you added a new SeedReport "
        f"field that's per-run volatile (timestamp / request id / nonce), add "
        f"it to _CANONICAL_EXCLUDE in envelopes.py BEFORE updating this hash."
    )


def test_run_config_rejects_unknown_keys() -> None:
    from pydantic import ValidationError
    payload = {
        "mode": "deep",
        "profile": "quality",
        "focus": None,
        "allow_broken": False,
        "tensions_only": False,
        "resolved_models": {},
        "run_nonce": "abcdef",
        "config_hash": "sha256:" + "0" * 64,
        "shadow_mode": True,  # extra — must be rejected
    }
    with pytest.raises(ValidationError, match="shadow_mode|Extra"):
        RunConfig.model_validate(payload)
