"""Tests for bench/runner/invoke_hydra_1x.py — guards against harness pre-flight regressions."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from bench.runner import invoke_hydra_1x
from bench.runner.invoke_hydra_1x import invoke_hydra
from bench.runner.run_bench import CASES_DIR


def test_invoke_hydra_argv_has_no_cwd_flag(tmp_path: Path) -> None:
    """--cwd is not a valid Claude Code CLI flag; subprocess cwd= must be used instead."""
    fake_report = tmp_path / ".hydra" / "reports" / "hydra-20260417-120000.md"
    fake_report.parent.mkdir(parents=True)
    fake_report.write_text("# report")

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        invoke_hydra(tmp_path)

    call_args = mock_run.call_args
    argv: list[str] = call_args.args[0]
    assert "--cwd" not in argv, f"--cwd must not appear in argv; got: {argv}"


def test_invoke_hydra_uses_cwd_kwarg(tmp_path: Path) -> None:
    """subprocess.run must receive cwd= so the child process runs in the workspace."""
    fake_report = tmp_path / ".hydra" / "reports" / "hydra-20260417-120000.md"
    fake_report.parent.mkdir(parents=True)
    fake_report.write_text("# report")

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        invoke_hydra(tmp_path)

    call_kwargs = mock_run.call_args.kwargs
    assert "cwd" in call_kwargs, "subprocess.run must receive cwd= kwarg"
    assert call_kwargs["cwd"] == str(tmp_path)


def test_prepare_case_workspace_missing_workspace_dir_raises(tmp_path: Path) -> None:
    """RuntimeError when a case has no workspace/ subdirectory."""
    case_id = "99-no-such-case"
    case_dir = tmp_path / case_id
    case_dir.mkdir()
    # No workspace/ subdir created

    saved = invoke_hydra_1x.CASES_DIR  # type: ignore[attr-defined]
    try:
        invoke_hydra_1x.CASES_DIR = tmp_path  # type: ignore[attr-defined]
        with pytest.raises(RuntimeError, match="no workspace"):
            invoke_hydra_1x.prepare_case_workspace(case_id)
    finally:
        invoke_hydra_1x.CASES_DIR = saved  # type: ignore[attr-defined]


def test_prepare_case_workspace_bad_diff_raises(tmp_path: Path) -> None:
    """A workspace with an unapplicable diff must raise RuntimeError (not silently pass)."""
    case_id = "test-bad-diff"
    case_dir = tmp_path / case_id
    workspace_dir = case_dir / "workspace"
    workspace_dir.mkdir(parents=True)

    src = workspace_dir / "src" / "foo.ts"
    src.parent.mkdir(parents=True)
    src.write_text("export const x = 1;\n")

    # Diff references context lines that don't exist in the file
    bad_patch = case_dir / "diff.patch"
    bad_patch.write_text(
        "--- a/src/foo.ts\n"
        "+++ b/src/foo.ts\n"
        "@@ -1,3 +1,4 @@\n"
        " export const x = 1;\n"
        " THIS_LINE_DOES_NOT_EXIST\n"
        " NEITHER_DOES_THIS\n"
        "+export const y = 2;\n"
    )

    saved = invoke_hydra_1x.CASES_DIR  # type: ignore[attr-defined]
    try:
        invoke_hydra_1x.CASES_DIR = tmp_path  # type: ignore[attr-defined]
        with pytest.raises(RuntimeError, match="git apply failed"):
            invoke_hydra_1x.prepare_case_workspace(case_id)
    finally:
        invoke_hydra_1x.CASES_DIR = saved  # type: ignore[attr-defined]


def test_prepare_case_workspace_real_case_applies_diff() -> None:
    """Integration: prepare_case_workspace for a real case leaves diff applied (unstaged)."""
    real_cases = sorted(p.name for p in CASES_DIR.iterdir() if (p / "workspace").is_dir())
    if not real_cases:
        pytest.skip("no real cases with workspace/ dirs found")

    case_id = real_cases[0]
    workspace = invoke_hydra_1x.prepare_case_workspace(case_id)
    try:
        assert workspace.is_dir(), "scratch dir must exist"

        # The diff has been applied (working tree has unstaged changes)
        result = subprocess.run(
            ["git", "diff", "--name-only"],
            cwd=workspace,
            capture_output=True,
            text=True,
            check=True,
        )
        assert result.stdout.strip(), (
            f"expected unstaged changes after diff apply for {case_id}, "
            f"got empty diff output"
        )

        # HEAD commit must exist (base was committed)
        log_result = subprocess.run(
            ["git", "log", "--oneline", "-1"],
            cwd=workspace,
            capture_output=True,
            text=True,
            check=True,
        )
        assert "base" in log_result.stdout, (
            f"expected 'base' commit in HEAD, got: {log_result.stdout!r}"
        )
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


def test_validate_case_id_rejects_traversal() -> None:
    """A3-S5: --cases ../../tmp/evil must be rejected before any filesystem ops."""
    from bench.runner.invoke_hydra_1x import _validate_case_id
    with pytest.raises(RuntimeError, match="invalid case id"):
        _validate_case_id("../../../tmp/evil")


def test_validate_case_id_rejects_absolute_path() -> None:
    from bench.runner.invoke_hydra_1x import _validate_case_id
    with pytest.raises(RuntimeError, match="invalid case id"):
        _validate_case_id("/etc/passwd")


def test_validate_case_id_rejects_empty_and_self_ref() -> None:
    """A-F1: empty/dot/dot-slash case_id resolves to CASES_DIR itself; reject loudly."""
    from bench.runner.invoke_hydra_1x import _validate_case_id
    for bad in ("", ".", "./."):
        with pytest.raises(RuntimeError, match="empty/self-referential"):
            _validate_case_id(bad)


def test_validate_case_id_rejects_nonexistent_case() -> None:
    """D-5: a syntactically valid case_id that resolves inside CASES_DIR but
    doesn't exist on disk hits the `is_dir()` branch — distinct from
    traversal/absolute/self-ref. Common in production via `--cases typo`."""
    from bench.runner.invoke_hydra_1x import _validate_case_id
    with pytest.raises(RuntimeError, match="case directory does not exist"):
        _validate_case_id("does-not-exist-xyz-12345")


def test_validate_case_id_accepts_legitimate_case() -> None:
    """A real case under bench/cases/ resolves cleanly."""
    from bench.runner.invoke_hydra_1x import _validate_case_id
    legit_cases = [p.name for p in CASES_DIR.iterdir() if p.is_dir()]
    if not legit_cases:
        pytest.skip("no bench cases on disk")
    resolved = _validate_case_id(legit_cases[0])
    assert resolved.is_dir()
    assert resolved.parent == CASES_DIR.resolve()


def test_prepare_case_workspace_handles_git_as_file_gitlink(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Iteration-2 F1: a bench case shipping `workspace/.git` as a regular file
    (a valid git "gitlink" pointing to an external gitdir) used to crash
    prepare_case_workspace with NotADirectoryError because `shutil.rmtree`
    requires a directory. Now scrubs files/symlinks via unlink(), dirs via
    rmtree(); workspace then proceeds to `git init` cleanly.
    """
    from bench.runner import invoke_hydra_1x
    fake_case = tmp_path / "fake-case"
    workspace = fake_case / "workspace"
    workspace.mkdir(parents=True)
    (workspace / "hello.py").write_text("print('hi')\n")
    # gitlink: a file at .git pointing to an external gitdir (legit git feature
    # used by submodules and worktrees). Path doesn't have to exist.
    (workspace / ".git").write_text("gitdir: /tmp/some-external-gitdir\n")
    (fake_case / "diff.patch").write_text(
        "diff --git a/hello.py b/hello.py\n"
        "--- a/hello.py\n"
        "+++ b/hello.py\n"
        "@@ -1 +1,2 @@\n"
        " print('hi')\n"
        "+# patched\n"
    )
    monkeypatch.setattr(invoke_hydra_1x, "CASES_DIR", tmp_path)
    scratch: Path | None = None
    try:
        scratch = invoke_hydra_1x.prepare_case_workspace("fake-case")
        # Real .git/ now exists from `git init`; gitlink file replaced by dir.
        assert (scratch / ".git").is_dir()
    finally:
        if scratch is not None:
            shutil.rmtree(scratch, ignore_errors=True)


def test_prepare_case_workspace_purges_malicious_git_hooks(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """S-N1: a bench case shipping .git/hooks/post-commit must NOT execute it.

    Live exploit pre-fix: shutil.copytree preserved hooks; git init kept them;
    git commit ran them. We verify the hook directory is purged before init.
    """
    from bench.runner import invoke_hydra_1x
    fake_case = tmp_path / "fake-case"
    workspace = fake_case / "workspace"
    workspace.mkdir(parents=True)
    (workspace / "hello.py").write_text("print('hi')\n")
    hooks = workspace / ".git" / "hooks"
    hooks.mkdir(parents=True)
    sentinel = tmp_path / "PWNED-SENTINEL"
    hook = hooks / "post-commit"
    hook.write_text(f"#!/bin/sh\ntouch {sentinel}\n")
    hook.chmod(0o755)
    # Minimal valid patch so prepare_case_workspace runs to completion.
    (fake_case / "diff.patch").write_text(
        "diff --git a/hello.py b/hello.py\n"
        "--- a/hello.py\n"
        "+++ b/hello.py\n"
        "@@ -1 +1,2 @@\n"
        " print('hi')\n"
        "+# patched\n"
    )

    monkeypatch.setattr(invoke_hydra_1x, "CASES_DIR", tmp_path)
    scratch: Path | None = None
    try:
        scratch = invoke_hydra_1x.prepare_case_workspace("fake-case")
        assert not sentinel.exists(), (
            "post-commit hook fired — .git scrub failed to prevent RCE"
        )
        # Belt-and-suspenders: confirm scrub happened by inspecting hooks dir.
        # git init recreates a fresh hooks/ with .sample files only.
        live_hooks = scratch / ".git" / "hooks" / "post-commit"
        assert not live_hooks.exists(), "non-sample post-commit hook survived scrub"
    finally:
        if scratch is not None:
            shutil.rmtree(scratch, ignore_errors=True)
