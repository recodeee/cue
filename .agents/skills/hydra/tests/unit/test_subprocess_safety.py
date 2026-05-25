from pathlib import Path

import pytest

from hydra.subprocess_safe import UnsafeArgError, run_tool


def test_runs_simple_command(tmp_path: Path) -> None:
    result = run_tool(["/bin/echo", "hello"], cwd=tmp_path, timeout=5)
    assert result.returncode == 0
    assert result.stdout.strip() == "hello"


def test_rejects_shell_metachar(tmp_path: Path) -> None:
    with pytest.raises(UnsafeArgError):
        run_tool(["/bin/echo", "foo; rm -rf /"], cwd=tmp_path, timeout=5)


def test_rejects_non_list_argv(tmp_path: Path) -> None:
    with pytest.raises(TypeError):
        run_tool("echo hello", cwd=tmp_path, timeout=5)  # type: ignore[arg-type]


def test_env_is_scrubbed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-leak-me")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "leak")
    result = run_tool(["/usr/bin/env"], cwd=tmp_path, timeout=5)
    assert "ANTHROPIC_API_KEY" not in result.stdout
    assert "AWS_SECRET_ACCESS_KEY" not in result.stdout
    assert "PATH=/usr/bin:/bin" in result.stdout


def test_timeout_raises(tmp_path: Path) -> None:
    with pytest.raises(TimeoutError):
        run_tool(["/bin/sleep", "5"], cwd=tmp_path, timeout=1)


def test_safe_fn_regex_accepts_normal_path(tmp_path: Path) -> None:
    # SAFE_FN: path-like args match r"^[A-Za-z0-9._/@:+=-]+$"
    result = run_tool(["/bin/echo", "src/foo_bar.py"], cwd=tmp_path, timeout=5)
    assert result.returncode == 0


def test_safe_fn_regex_rejects_backticks(tmp_path: Path) -> None:
    with pytest.raises(UnsafeArgError):
        run_tool(["/bin/echo", "`whoami`"], cwd=tmp_path, timeout=5)


def test_safe_fn_regex_rejects_dollar_paren(tmp_path: Path) -> None:
    with pytest.raises(UnsafeArgError):
        run_tool(["/bin/echo", "$(id)"], cwd=tmp_path, timeout=5)


def test_rejects_null_byte(tmp_path: Path) -> None:
    with pytest.raises(UnsafeArgError):
        run_tool(["/bin/echo", "foo\x00bar"], cwd=tmp_path, timeout=5)


def test_extra_env_non_allowlisted_key_dropped(
    tmp_path: Path,
) -> None:
    # MALICIOUS_KEY is neither in ALLOWED_ENV_KEYS nor HYDRA_*-prefixed.
    result = run_tool(
        ["/usr/bin/env"],
        cwd=tmp_path,
        timeout=5,
        extra_env={"MALICIOUS_KEY": "should-not-appear"},
    )
    assert "MALICIOUS_KEY" not in result.stdout
    assert "should-not-appear" not in result.stdout


def test_extra_env_hydra_prefix_passed_through(tmp_path: Path) -> None:
    result = run_tool(
        ["/usr/bin/env"],
        cwd=tmp_path,
        timeout=5,
        extra_env={"HYDRA_SCAN_TARGET": "src/"},
    )
    assert "HYDRA_SCAN_TARGET=src/" in result.stdout


def test_nonzero_exit_returns_rather_than_raises(tmp_path: Path) -> None:
    # /bin/false always returns 1. run_tool uses check=False, so it must
    # return a CompletedProcess rather than raise CalledProcessError.
    result = run_tool(["/usr/bin/false"], cwd=tmp_path, timeout=5)
    assert result.returncode != 0


def test_stderr_captured_separately(tmp_path: Path) -> None:
    script = tmp_path / "emit.py"
    script.write_text(
        "import sys\nprint('stdout-msg')\nprint('stderr-msg', file=sys.stderr)\n"
    )
    result = run_tool(
        ["/usr/bin/python3", str(script)],
        cwd=tmp_path,
        timeout=5,
    )
    assert "stdout-msg" in result.stdout
    assert "stderr-msg" in result.stderr
    assert "stderr-msg" not in result.stdout


def test_allowed_env_keys_is_immutable() -> None:
    """S-N5: ALLOWED_ENV_KEYS must be frozen — adding DYLD_INSERT_LIBRARIES at
    runtime would re-open the A3-S2 hole that's currently a verified false
    positive."""
    from hydra.subprocess_safe import ALLOWED_ENV_KEYS
    with pytest.raises(AttributeError):
        ALLOWED_ENV_KEYS.add("DYLD_INSERT_LIBRARIES")  # type: ignore[attr-defined]


def test_base_scrubbed_env_is_immutable() -> None:
    """S-N5: _BASE_SCRUBBED_ENV must be frozen via MappingProxyType."""
    from hydra.subprocess_safe import _BASE_SCRUBBED_ENV
    with pytest.raises(TypeError):
        _BASE_SCRUBBED_ENV["DYLD_INSERT_LIBRARIES"] = "/evil.dylib"  # type: ignore[index]


def test_run_tool_refreshes_home_each_call(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """S-N5: HOME must be re-read from os.environ each call, not cached at
    module import time. Otherwise a HOME change in CI / test fixtures gives
    a stale value to the child."""
    monkeypatch.setenv("HOME", "/tmp/fake-home-1")
    r1 = run_tool(["/usr/bin/env"], cwd=tmp_path, timeout=5)
    assert "HOME=/tmp/fake-home-1" in r1.stdout
    monkeypatch.setenv("HOME", "/tmp/fake-home-2")
    r2 = run_tool(["/usr/bin/env"], cwd=tmp_path, timeout=5)
    assert "HOME=/tmp/fake-home-2" in r2.stdout
