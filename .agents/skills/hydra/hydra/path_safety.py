"""Path containment helpers. Single source of truth for all path resolution."""
from __future__ import annotations

import os
from pathlib import Path

PATH_MAX = 4096  # Linux default; macOS is lower but 4096 is a safe ceiling


class PathEscapeError(Exception):
    """Raised when a path resolves outside the repository root or exceeds PATH_MAX."""


def contained_path(
    repo_root: Path | str,
    user_path: str,
    *,
    must_exist: bool = True,
) -> Path:
    """Resolve `user_path` against `repo_root`; raise PathEscapeError on escape.

    Rules (in code order):
      1. Absolute paths are rejected outright.
      2. PATH_MAX: combined length must fit.
      3. Resolved path must be relative to repo_root (symlinks followed).
      4. If must_exist, resolution requires the target to exist
         (FileNotFoundError propagates).
      5. Null bytes / other malformed paths surface as PathEscapeError.
    """
    root = Path(repo_root).resolve(strict=True)
    candidate = Path(user_path)

    if candidate.is_absolute():
        raise PathEscapeError(f"absolute path rejected: {user_path!r}")

    combined = root / candidate
    if len(str(combined)) > PATH_MAX:
        raise PathEscapeError(f"path exceeds PATH_MAX ({PATH_MAX}): {user_path!r}")

    try:
        resolved = combined.resolve(strict=must_exist)
    except ValueError as exc:
        # e.g. embedded null byte — not a FileNotFoundError, normalize to PathEscapeError
        # so every callsite (Task 22 ground_finding etc.) catches a single exception type.
        raise PathEscapeError(f"malformed path: {user_path!r}") from exc

    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise PathEscapeError(
            f"path escapes repo_root: {user_path!r} -> {resolved}"
        ) from exc

    # Belt-and-suspenders: resolve() already canonicalizes case on APFS/NTFS, so this
    # check is normatively redundant after relative_to(). Kept as a paranoid tripwire
    # in case a future refactor weakens one of the earlier guards.
    if os.path.normcase(str(resolved)).find(os.path.normcase(str(root))) != 0:
        raise PathEscapeError(f"case-fold escape: {user_path!r}")

    return resolved
