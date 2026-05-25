"""Unit tests for hydra.phase1.tools.semgrep."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from hydra.envelopes import Severity
from hydra.phase1.tools.semgrep import parse_semgrep_json, run_semgrep

# ---------------------------------------------------------------------------
# parse_semgrep_json — severity mapping
# ---------------------------------------------------------------------------


def test_parse_semgrep_error_maps_to_serious(tmp_path: Path) -> None:
    raw: dict[str, Any] = {
        "results": [
            {
                "check_id": "rule.sqli",
                "path": "app/db.py",
                "start": {"line": 10},
                "end": {"line": 12},
                "extra": {"severity": "ERROR", "message": "SQL injection"},
            }
        ]
    }
    findings = parse_semgrep_json(raw, tmp_path)
    assert len(findings) == 1
    assert findings[0].severity == Severity.SERIOUS
    assert findings[0].rule_id == "rule.sqli"
    assert findings[0].file == "app/db.py"
    assert findings[0].lines == "10-12"


def test_parse_semgrep_warning_maps_to_moderate(tmp_path: Path) -> None:
    raw: dict[str, Any] = {
        "results": [
            {
                "check_id": "rule.xss",
                "path": "app/views.py",
                "start": {"line": 5},
                "end": {"line": 5},
                "extra": {"severity": "WARNING", "message": "XSS risk"},
            }
        ]
    }
    findings = parse_semgrep_json(raw, tmp_path)
    assert findings[0].severity == Severity.MODERATE


def test_parse_semgrep_message_truncated_at_500(tmp_path: Path) -> None:
    long_msg = "x" * 600
    raw: dict[str, Any] = {
        "results": [
            {
                "check_id": "rule.long",
                "path": "a.py",
                "start": {"line": 1},
                "end": {"line": 1},
                "extra": {"severity": "WARNING", "message": long_msg},
            }
        ]
    }
    findings = parse_semgrep_json(raw, tmp_path)
    assert len(findings[0].message) <= 500


# ---------------------------------------------------------------------------
# Forward-compat: INFO → MINOR
# ---------------------------------------------------------------------------


def test_parse_semgrep_info_maps_to_minor(tmp_path: Path) -> None:
    raw: dict[str, Any] = {
        "results": [
            {
                "check_id": "x",
                "path": "a.py",
                "start": {"line": 1},
                "end": {"line": 1},
                "extra": {"severity": "INFO", "message": "note"},
            }
        ]
    }
    findings = parse_semgrep_json(raw, tmp_path)
    assert findings[0].severity == Severity.MINOR


# ---------------------------------------------------------------------------
# run_semgrep — graceful degrade on malformed JSON
# ---------------------------------------------------------------------------


def test_run_semgrep_malformed_json_returns_skipped(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("shutil.which", lambda _: "/usr/local/bin/semgrep")
    # Path-validation now requires the file to exist before semgrep is invoked.
    (tmp_path / "a.py").write_text("# fixture")

    def fake_run_tool(*_a: object, **_k: object) -> SimpleNamespace:
        return SimpleNamespace(returncode=0, stdout="not-json", stderr="")

    monkeypatch.setattr("hydra.phase1.tools.semgrep.run_tool", fake_run_tool)
    result = run_semgrep(tmp_path, changed_files=["a.py"])
    assert result.skipped is True
    # First warnings come from path validation (none expected); JSON parse
    # warning is the failure signal.
    assert any("JSON parse failed" in w for w in result.warnings)


# ---------------------------------------------------------------------------
# A3-S1 / A3-S7 — argv injection + emitted-path containment hardening
# ---------------------------------------------------------------------------


def test_run_semgrep_rejects_traversal_in_changed_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A3-S1: src/../../../etc/passwd must not reach semgrep argv."""
    monkeypatch.setattr("shutil.which", lambda _: "/usr/local/bin/semgrep")
    captured_argv: list[list[str]] = []

    def fake_run_tool(argv: list[str], **_k: object) -> SimpleNamespace:
        captured_argv.append(argv)
        return SimpleNamespace(returncode=0, stdout='{"results":[]}', stderr="")

    monkeypatch.setattr("hydra.phase1.tools.semgrep.run_tool", fake_run_tool)
    result = run_semgrep(tmp_path, changed_files=["../../etc/passwd"])
    assert result.skipped is True
    assert any("unsafe/missing path" in w for w in result.warnings)
    assert captured_argv == [], "semgrep must not be invoked when all paths fail validation"


def test_run_semgrep_rejects_option_lookalike_filename_when_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A3-S1 (path 1): an option-lookalike string for a non-existent file is
    rejected by must_exist=True before reaching argv."""
    monkeypatch.setattr("shutil.which", lambda _: "/usr/local/bin/semgrep")
    captured_argv: list[list[str]] = []

    def fake_run_tool(argv: list[str], **_k: object) -> SimpleNamespace:
        captured_argv.append(argv)
        return SimpleNamespace(returncode=0, stdout='{"results":[]}', stderr="")

    monkeypatch.setattr("hydra.phase1.tools.semgrep.run_tool", fake_run_tool)
    result = run_semgrep(tmp_path, changed_files=["--config=http://evil/r"])
    assert result.skipped is True
    assert captured_argv == [], "semgrep must not see missing-file argv"


def test_run_semgrep_dash_dash_neutralises_option_lookalike_real_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A3-S1 (path 2): if an attacker DOES create a file literally named
    --config=evil inside cwd, it passes path validation (must_exist=True
    succeeds), so the `--` separator is the actual remaining defense.
    Verify the realised argv places the lookalike AFTER `--` so semgrep
    parses it positionally, not as a flag."""
    monkeypatch.setattr("shutil.which", lambda _: "/usr/local/bin/semgrep")
    # POSIX-legal filename starting with `--` — actually create it on disk.
    evil_name = "--config=evil"
    (tmp_path / evil_name).write_text("# fixture")
    captured_argv: list[list[str]] = []

    def fake_run_tool(argv: list[str], **_k: object) -> SimpleNamespace:
        captured_argv.append(argv)
        return SimpleNamespace(returncode=0, stdout='{"results":[]}', stderr="")

    monkeypatch.setattr("hydra.phase1.tools.semgrep.run_tool", fake_run_tool)
    run_semgrep(tmp_path, changed_files=[evil_name])
    assert len(captured_argv) == 1
    argv = captured_argv[0]
    assert "--" in argv, f"-- separator missing: {argv}"
    sep_idx = argv.index("--")
    assert evil_name in argv[sep_idx + 1 :], (
        f"option-lookalike must be AFTER --, got argv={argv}"
    )
    # Belt-and-suspenders: the lookalike must NOT appear before --
    assert evil_name not in argv[: sep_idx], (
        f"option-lookalike leaked before --: {argv[:sep_idx]}"
    )


def test_run_semgrep_argv_inserts_dash_dash_separator(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A3-S1 belt-and-suspenders: `--` between config and paths so any
    POSIX-legal filename starting with `-` is parsed positionally."""
    monkeypatch.setattr("shutil.which", lambda _: "/usr/local/bin/semgrep")
    (tmp_path / "legit.py").write_text("# fixture")
    captured_argv: list[list[str]] = []

    def fake_run_tool(argv: list[str], **_k: object) -> SimpleNamespace:
        captured_argv.append(argv)
        return SimpleNamespace(returncode=0, stdout='{"results":[]}', stderr="")

    monkeypatch.setattr("hydra.phase1.tools.semgrep.run_tool", fake_run_tool)
    run_semgrep(tmp_path, changed_files=["legit.py"])
    assert len(captured_argv) == 1
    argv = captured_argv[0]
    assert "--" in argv, f"expected -- separator in argv: {argv}"
    sep_idx = argv.index("--")
    assert argv[sep_idx - 1] == "auto", "-- must follow --config auto"
    assert argv[sep_idx + 1 :] == ["legit.py"], "validated paths must follow --"


def test_parse_semgrep_rejects_absolute_emitted_path(tmp_path: Path) -> None:
    """A3-S7: semgrep emitting `/etc/passwd` (e.g. via followed symlink) must
    not propagate as a `ToolFinding.file` value."""
    raw: dict[str, Any] = {
        "results": [
            {
                "check_id": "x",
                "path": "/etc/passwd",
                "start": {"line": 1},
                "end": {"line": 1},
                "extra": {"severity": "WARNING", "message": "outside repo"},
            }
        ]
    }
    findings = parse_semgrep_json(raw, tmp_path)
    assert findings[0].file is None


def test_parse_semgrep_rejects_traversal_emitted_path(tmp_path: Path) -> None:
    """A3-S7: a relative path that resolves outside cwd is also rejected."""
    raw: dict[str, Any] = {
        "results": [
            {
                "check_id": "x",
                "path": "../../etc/passwd",
                "start": {"line": 1},
                "end": {"line": 1},
                "extra": {"severity": "WARNING", "message": "outside repo"},
            }
        ]
    }
    findings = parse_semgrep_json(raw, tmp_path)
    assert findings[0].file is None


# ---------------------------------------------------------------------------
# Iteration-1 follow-ups: S-N2 / S-N3 / A-F2
# ---------------------------------------------------------------------------


def test_validate_input_paths_warning_does_not_leak_resolved_target(
    tmp_path: Path,
) -> None:
    """S-N2: PathEscapeError text contains the RESOLVED real path of a symlink
    (e.g. ~/.ssh/id_rsa). That string would flow into SeedReport.warnings →
    cached payload → Anthropic. Warning must contain only the user-supplied
    raw input, never the resolved target.
    """
    from hydra.phase1.tools.semgrep import _validate_input_paths
    secret_file = tmp_path / "secret-target-leaked.txt"
    secret_file.write_text("never include this string in warnings")
    scan_root = tmp_path / "scan"
    scan_root.mkdir()
    link = scan_root / "innocent.py"
    link.symlink_to(secret_file)
    valid, warnings = _validate_input_paths(scan_root, ["innocent.py"])
    assert valid == [], "symlink to outside file should be rejected"
    assert len(warnings) == 1
    assert "innocent.py" in warnings[0], "user input must appear in warning"
    assert "secret-target-leaked" not in warnings[0], (
        f"resolved target leaked into warning: {warnings[0]!r}"
    )


def test_validate_input_paths_rejects_self_referential(tmp_path: Path) -> None:
    """S-N3: empty / "." / "./." resolve to cwd itself; semgrep would then
    recursively scan the entire repo (leaking .env, node_modules, etc.).
    Reject explicitly, do NOT pass them to argv.
    """
    from hydra.phase1.tools.semgrep import _validate_input_paths
    valid, warnings = _validate_input_paths(tmp_path, ["", ".", "./."])
    assert valid == []
    assert all("self-referential" in w for w in warnings)


def test_validate_input_paths_dedupes(tmp_path: Path) -> None:
    """S-N3: a path passed multiple times must only appear once in the
    semgrep argv (otherwise findings are inflated by N×)."""
    from hydra.phase1.tools.semgrep import _validate_input_paths
    (tmp_path / "a.py").write_text("# x")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.py").write_text("# y")
    valid, _ = _validate_input_paths(
        tmp_path, ["a.py", "a.py", "./a.py", "sub/b.py", "sub/b.py"]
    )
    assert sorted(valid) == ["a.py", "sub/b.py"]


def test_validate_input_paths_dedupes_case_insensitively(tmp_path: Path) -> None:
    """Iteration-2 F2: on case-insensitive volumes (APFS/NTFS), `A.py` and
    `a.py` resolve to the same inode. Without normcase-based dedup, semgrep
    would scan the same file twice.

    On case-sensitive volumes (Linux ext4) the two are genuinely distinct
    files; on those filesystems the dedup is a no-op for this input. This
    test verifies the deduplication behavior of the semgrep wrapper without
    depending on the underlying filesystem case-sensitivity.
    """
    from hydra.phase1.tools.semgrep import _validate_input_paths
    (tmp_path / "Alpha.py").write_text("# x")
    # On case-insensitive FS, this path will resolve to Alpha.py.
    # On case-sensitive FS, alpha.py wouldn't exist; would be rejected.
    inputs = ["Alpha.py", "alpha.py", "Alpha.py"]
    valid, _ = _validate_input_paths(tmp_path, inputs)
    # Either (case-insensitive FS): one entry, normcase-deduped.
    # Or (case-sensitive FS): one entry (Alpha.py kept; alpha.py rejected by must_exist).
    assert len(valid) == 1, f"expected exactly one deduped entry, got {valid}"


def test_safe_relative_path_handles_missing_cwd(tmp_path: Path) -> None:
    """A-F2: if cwd itself disappeared between scan start and result parse,
    `contained_path` raises FileNotFoundError on root resolution. Helper
    must catch and return None so parse_semgrep_json doesn't crash."""
    from hydra.phase1.tools.semgrep import _safe_relative_path
    gone = tmp_path / "removed-mid-scan"
    # Don't create it — passing a non-existent root is the failure mode.
    assert _safe_relative_path(gone, "x.py") is None
