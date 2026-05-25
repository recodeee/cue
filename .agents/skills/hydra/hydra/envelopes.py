"""Dataclasses for inter-phase envelopes (§4.4 of spec)."""
from __future__ import annotations

import enum
import json
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class Severity(enum.StrEnum):
    CATASTROPHIC = "CATASTROPHIC"
    SERIOUS = "SERIOUS"
    MODERATE = "MODERATE"
    MINOR = "MINOR"
    TRIVIAL = "TRIVIAL"


class Position(enum.StrEnum):
    APPROVE = "APPROVE"
    CONCERN = "CONCERN"
    REJECT = "REJECT"


class GroundingStatus(enum.StrEnum):
    UNKNOWN = "UNKNOWN"
    CITATION_PRESENT = "CITATION_PRESENT"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    NO_CITATION = "NO_CITATION"
    FILE_MISSING = "FILE_MISSING"
    RANGE_MISSING = "RANGE_MISSING"
    TOKEN_MISMATCH = "TOKEN_MISMATCH"
    PATH_ESCAPE = "PATH_ESCAPE"


class IssueClass(enum.StrEnum):
    race_condition = "race_condition"
    deadlock = "deadlock"
    null_deref = "null_deref"
    buffer_overflow = "buffer_overflow"
    path_traversal = "path_traversal"
    command_injection = "command_injection"
    sql_injection = "sql_injection"
    xss = "xss"
    xxe = "xxe"
    csrf = "csrf"
    auth_bypass = "auth_bypass"
    session_fixation = "session_fixation"
    crypto_misuse = "crypto_misuse"
    secret_exposure = "secret_exposure"
    logic_error = "logic_error"
    off_by_one = "off_by_one"
    type_confusion = "type_confusion"
    resource_leak = "resource_leak"
    performance_degradation = "performance_degradation"
    api_break = "api_break"
    scope_creep = "scope_creep"
    phantom_helper = "phantom_helper"
    over_engineering = "over_engineering"
    fake_tdd = "fake_tdd"
    drift = "drift"
    comment_bloat = "comment_bloat"
    defensive_theatre = "defensive_theatre"
    readability = "readability"
    architectural_boundary = "architectural_boundary"
    dependency_vulnerability = "dependency_vulnerability"
    test_quality = "test_quality"
    other = "other"


class Chain(BaseModel):
    # extra='forbid' on the nested chain shape too: pydantic does NOT propagate
    # the AdvisorFinding-level forbid to nested models, so without this, a
    # cached AdvisorFinding could smuggle keys via {"chain":{...,"smuggled":"x"}}.
    # Three-field closed schema — no legitimate reason to accept extras.
    model_config = ConfigDict(extra="forbid")

    premise: str = ""
    execution_trace: str = ""
    conclusion: str = ""


class ToolFinding(BaseModel):
    id: str
    source: Literal["semgrep", "osv", "lang_checker"]
    rule_id: str = ""
    file: str | None = None
    lines: str | None = None
    severity: Severity = Severity.MODERATE
    message: str = Field("", max_length=500)


class AdvisorFinding(BaseModel):
    # extra='forbid' is the injection-defense boundary: an advisor (or a
    # tampered cached envelope) producing extra JSON keys must fail validation
    # loudly rather than be silently accepted and propagated through the
    # cached chairman pipeline. Spec §4.3.1 + R1 compound (M2 + cache).
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    severity: Severity
    evidence: Literal["VERIFIED", "HYPOTHESIS_HIGH", "HYPOTHESIS_MEDIUM", "HYPOTHESIS_LOW"]
    position: Position
    file: str | None = None
    lines: str | None = None
    issue_class: IssueClass = IssueClass.other
    chain: Chain
    extends_seed: list[str] = Field(default_factory=list)
    challenges_seed: list[str] = Field(default_factory=list)
    novel: bool = False
    grounding: GroundingStatus = GroundingStatus.UNKNOWN
    is_tension: bool = False
    check_type: str | None = None  # Echo-specific
    pr_desc_quote: str | None = None  # Echo-specific


class StructuralContext(BaseModel):
    file_tree: list[str] = Field(default_factory=list)
    boundaries: list[dict[str, Any]] = Field(default_factory=list)
    import_observations: list[dict[str, Any]] = Field(default_factory=list)


# Fields excluded from canonical_json — must stay byte-stable across runs
# (spec §4.3.1 L210: "No timestamps / run_ids inside cached blocks").
# generated_at is the only volatile field today; add new ones here as they
# appear (e.g., per-run trace IDs). frozenset prevents accidental runtime
# mutation that would silently change the cache key for the whole process.
_CANONICAL_EXCLUDE: frozenset[str] = frozenset({"generated_at"})


class SeedReport(BaseModel):
    # extra='forbid' protects the cached payload (BP4) from key-smuggling
    # injection. See AdvisorFinding for full rationale.
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["2.0"] = "2.0"
    generated_at: str
    run_nonce: str = Field(pattern=r"^[0-9a-f]{6}$")
    tool_findings: list[ToolFinding] = Field(default_factory=list)
    echo_findings: list[AdvisorFinding] = Field(default_factory=list)
    navigator_findings: list[AdvisorFinding] = Field(default_factory=list)
    structural_context: StructuralContext = Field(default_factory=StructuralContext)
    skipped_tools: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    def canonical_json(self) -> bytes:
        """Byte-identical JSON for cache-hygiene (BP4).

        Excludes wall-clock fields per _CANONICAL_EXCLUDE so two runs with
        identical logical content produce identical bytes (spec §4.3.1 L210
        "No timestamps / run_ids inside cached blocks", cache-hit-rate ≥60%
        release-blocker per L216).
        """
        # set() conversion: pydantic's IncEx static type rejects frozenset
        # (runtime accepts it). Construct a fresh set from the immutable
        # source on each call — the frozenset is the source of truth, the
        # in-flight set is a typing concession.
        return json.dumps(
            self.model_dump(mode="json", exclude=set(_CANONICAL_EXCLUDE)),
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")


class RunConfig(BaseModel):
    # extra='forbid' — config_hash freeze must fail loudly if extra fields
    # land in the config blob between mint and verify (P-13 TOCTOU defense).
    model_config = ConfigDict(extra="forbid")

    mode: Literal["standard", "deep"]
    profile: Literal["quality", "balanced", "budget"]
    focus: Literal["security", "perf", "readability", "architecture", "reliability"] | None
    allow_broken: bool
    tensions_only: bool
    resolved_models: dict[str, str]
    run_nonce: str = Field(pattern=r"^[0-9a-f]{6}$")
    config_hash: str = Field(pattern=r"^sha256:[0-9a-f]{64}$")

# GroundedFindings, ChairmanInput, and ChairmanOutput envelopes will be
# (re-)introduced with proper typed shapes (no list[dict[str, Any]] primitive
# obsession) in the same commit that wires up the chairman runner — plan
# Tasks 22 (grounding), 28 (tensions), and 33 (chairman). Do not pre-define
# them as dict-shaped placeholders; that just hides the cache-stability and
# injection-defense work behind false reassurance.

