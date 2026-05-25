"""Integration tests — require real Codex CLI. Skip with CODEX_SKIP_LIVE=1.

These tests protect Hydra 2.0's Cross-Provider-Review from silent Codex-side
degradation. A failing test here means the dev environment cannot run Part-3+
advisors reliably.
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(
    os.environ.get("CODEX_SKIP_LIVE") == "1",
    reason="CODEX_SKIP_LIVE=1 set",
)


def test_codex_cli_installed() -> None:
    """codex binary is on PATH."""
    assert shutil.which("codex") is not None, (
        "codex CLI not on PATH. Install via npm or platform package."
    )


def test_codex_cli_responds() -> None:
    """codex --version returns non-empty output within 5s."""
    result = subprocess.run(
        ["codex", "--version"],
        capture_output=True,
        text=True,
        timeout=5,
        check=True,
    )
    assert result.stdout.strip(), "codex --version returned empty"
    assert "codex" in result.stdout.lower(), f"unexpected output: {result.stdout!r}"


def test_codex_plugin_cache_present() -> None:
    """Claude Code Codex plugin cache is populated."""
    cache = Path.home() / ".claude" / "plugins" / "cache" / "openai-codex" / "codex"
    assert cache.is_dir(), (
        f"plugin cache missing at {cache} — run: claude plugins install openai-codex"
    )
    versions = [p for p in cache.iterdir() if p.is_dir()]
    assert versions, "no Codex versions cached in plugin dir"


def test_codex_companion_script_resolvable() -> None:
    """The codex-companion.mjs script SKILL.md §147 references is findable."""
    cache = Path.home() / ".claude" / "plugins" / "cache" / "openai-codex" / "codex"
    if not cache.is_dir():
        pytest.skip("plugin cache missing — separate test catches this")
    scripts = sorted(
        cache.glob("*/scripts/codex-companion.mjs"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    assert scripts, (
        "no codex-companion.mjs resolvable via SKILL.md §147 pattern"
    )
