"""Config loader + hash freeze/verify (P-13 TOCTOU guard)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ALLOWED_KEYS = {"profile", "max_cost_usd"}
MAX_CONFIG_BYTES = 64 * 1024
MAX_DEPTH = 10


class ConfigChangedMidFlight(Exception):
    """config_hash at Phase 3 does not match Phase 0 snapshot."""


def _check_depth(obj: object, depth: int = 0) -> None:
    if depth > MAX_DEPTH:
        raise ValueError(f"config depth exceeds {MAX_DEPTH}")
    if isinstance(obj, dict):
        for v in obj.values():
            _check_depth(v, depth + 1)
    elif isinstance(obj, list):
        for v in obj:
            _check_depth(v, depth + 1)


def load_config(path: Path) -> dict[str, object]:
    """Strict loader: size-bounded, depth-bounded, unknown keys rejected."""
    size = path.stat().st_size
    if size > MAX_CONFIG_BYTES:
        raise ValueError(f"config exceeds 64KB: {size} bytes")
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError("config must be a JSON object")
    _check_depth(data)
    unknown = set(data.keys()) - ALLOWED_KEYS
    if unknown:
        raise ValueError(f"unknown key(s) in config: {sorted(unknown)}")
    return data


def config_hash(path: Path) -> str:
    """Frozen hash of raw config bytes. Compared at Phase 3 (§18.9, P-13)."""
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return f"sha256:{digest}"


def verify_config_hash(path: Path, frozen_hash: str) -> None:
    """Raise ConfigChangedMidFlight if current hash != frozen."""
    current = config_hash(path)
    if current != frozen_hash:
        raise ConfigChangedMidFlight(
            f"config hash drift: phase0={frozen_hash}, now={current}"
        )
