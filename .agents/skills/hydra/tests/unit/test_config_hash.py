import json
from pathlib import Path

import pytest

from hydra.config import ConfigChangedMidFlight, config_hash, load_config, verify_config_hash


def test_config_hash_stable(tmp_path: Path) -> None:
    cfg = tmp_path / "config.json"
    cfg.write_text(json.dumps({"profile": "quality"}))
    h1 = config_hash(cfg)
    h2 = config_hash(cfg)
    assert h1 == h2
    assert h1.startswith("sha256:")


def test_config_hash_changes_on_edit(tmp_path: Path) -> None:
    cfg = tmp_path / "config.json"
    cfg.write_text(json.dumps({"profile": "quality"}))
    h1 = config_hash(cfg)
    cfg.write_text(json.dumps({"profile": "budget"}))
    h2 = config_hash(cfg)
    assert h1 != h2


def test_verify_aborts_on_mismatch(tmp_path: Path) -> None:
    cfg = tmp_path / "config.json"
    cfg.write_text(json.dumps({"profile": "quality"}))
    h0 = config_hash(cfg)
    cfg.write_text(json.dumps({"profile": "budget"}))
    with pytest.raises(ConfigChangedMidFlight):
        verify_config_hash(cfg, h0)


def test_load_config_rejects_oversized(tmp_path: Path) -> None:
    cfg = tmp_path / "config.json"
    cfg.write_text("{" + '"x":"' + "a" * 70000 + '"}')
    with pytest.raises(ValueError, match="64KB"):
        load_config(cfg)


def test_load_config_rejects_unknown_keys(tmp_path: Path) -> None:
    cfg = tmp_path / "config.json"
    cfg.write_text(json.dumps({"profile": "quality", "unknown": "value"}))
    with pytest.raises(ValueError, match="unknown key"):
        load_config(cfg)


def test_verify_success_returns_none(tmp_path: Path) -> None:
    cfg = tmp_path / "config.json"
    cfg.write_text(json.dumps({"profile": "quality"}))
    h = config_hash(cfg)
    # Must not raise — verify_config_hash returns None on success.
    verify_config_hash(cfg, h)


def test_load_config_rejects_too_deep(tmp_path: Path) -> None:
    # Build {"a": {"a": {"a": ... 11 levels deep ... : "end"}}}.
    nested: object = "end"
    for _ in range(12):
        nested = {"profile": nested}
    cfg = tmp_path / "config.json"
    cfg.write_text(json.dumps(nested))
    with pytest.raises(ValueError, match="depth"):
        load_config(cfg)
