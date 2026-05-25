# tests/unit/test_path_containment.py
from pathlib import Path

import pytest

from hydra.path_safety import PathEscapeError, contained_path


def test_normal_relative_path(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "a.py").write_text("x")
    assert contained_path(tmp_path, "src/a.py") == (tmp_path / "src" / "a.py").resolve()


def test_escape_via_dotdot(tmp_path: Path) -> None:
    with pytest.raises(PathEscapeError):
        contained_path(tmp_path, "../etc/passwd", must_exist=False)


def test_escape_via_absolute(tmp_path: Path) -> None:
    with pytest.raises(PathEscapeError):
        contained_path(tmp_path, "/etc/passwd", must_exist=False)


def test_symlink_escape(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    target = tmp_path.parent / "outside"
    target.mkdir(exist_ok=True)
    (tmp_path / "src" / "link").symlink_to(target)
    with pytest.raises(PathEscapeError):
        contained_path(tmp_path, "src/link/secret.txt", must_exist=False)


def test_must_exist_missing_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        contained_path(tmp_path, "does/not/exist.py", must_exist=True)


def test_must_exist_false_allows_missing(tmp_path: Path) -> None:
    result = contained_path(tmp_path, "future/file.py", must_exist=False)
    assert result == (tmp_path / "future" / "file.py")


def test_path_max_rejected(tmp_path: Path) -> None:
    long_segment = "a" * 5000
    with pytest.raises(PathEscapeError):
        contained_path(tmp_path, f"src/{long_segment}.py", must_exist=False)


def test_case_fold_escape_apfs(tmp_path: Path) -> None:
    # APFS is case-insensitive by default; a path resolving via case-folding
    # outside the tree must still be rejected
    (tmp_path / "src").mkdir()
    with pytest.raises(PathEscapeError):
        contained_path(tmp_path, "SRC/../../outside.py", must_exist=False)
