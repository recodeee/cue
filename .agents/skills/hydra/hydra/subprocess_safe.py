"""Single subprocess entrypoint. Never call subprocess.run directly elsewhere."""
from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path
from types import MappingProxyType

SHELL_METACHARS = re.compile(r"[;&|`$<>\n\r]")
SAFE_FN = re.compile(r"^[A-Za-z0-9._/@:+=-]+$")
# frozenset/MappingProxyType — runtime-immutable to prevent any caller from
# silently widening the env passthrough (e.g. adding DYLD_INSERT_LIBRARIES
# would re-open the A3-S2 hole that's currently a confirmed false positive).
ALLOWED_ENV_KEYS: frozenset[str] = frozenset({"PATH", "LANG", "HOME", "TMPDIR"})
_BASE_SCRUBBED_ENV: MappingProxyType[str, str] = MappingProxyType({
    "PATH": "/usr/bin:/bin",
    "LANG": "C.UTF-8",
})


class UnsafeArgError(Exception):
    """Argument contains shell metacharacters or fails SAFE_FN."""


def _validate_args(argv: list[str]) -> None:
    if not isinstance(argv, list):
        raise TypeError(f"argv must be list[str], got {type(argv).__name__}")
    for arg in argv:
        if "\x00" in arg:
            raise UnsafeArgError(f"null byte in arg: {arg!r}")
        if SHELL_METACHARS.search(arg):
            raise UnsafeArgError(f"shell metacharacter in arg: {arg!r}")
        if ("/" in arg or arg.startswith(".")) and not SAFE_FN.fullmatch(arg):
            raise UnsafeArgError(f"path-like arg fails SAFE_FN: {arg!r}")


def run_tool(
    argv: list[str],
    cwd: Path,
    timeout: int = 120,
    extra_env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run subprocess with shell=False, scrubbed env, timeout, arg validation."""
    _validate_args(argv)
    env = dict(_BASE_SCRUBBED_ENV)
    # Refresh HOME each call: capturing at import time would freeze a stale
    # value if HOME changes (rare, but happens in test fixtures and CI matrix).
    env["HOME"] = os.environ.get("HOME", "/tmp")
    if extra_env:
        for k, v in extra_env.items():
            # HYDRA_* passthrough — callers must not forward user-controlled env keys here
            # (names like HYDRA_LD_PRELOAD would reach the dynamic linker).
            if k in ALLOWED_ENV_KEYS or k.startswith("HYDRA_"):
                env[k] = v
    try:
        return subprocess.run(
            argv,
            cwd=str(cwd),
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise TimeoutError(
            f"{argv[0]} exceeded {timeout}s timeout"
        ) from exc
