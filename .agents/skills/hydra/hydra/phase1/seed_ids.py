"""Seed ID assigner (spec §13.3)."""
from __future__ import annotations

PREFIXES: dict[str, str] = {
    "semgrep": "T-SEM",
    "osv": "T-OSV",
    "lang_checker": "T-LANG",
    "echo": "E",
    "navigator": "N",
}


def _validate_source(source: str) -> None:
    if source not in PREFIXES:
        raise ValueError(f"unknown source: {source!r}")


class SeedIdAssigner:
    def __init__(self) -> None:
        self._counters: dict[str, int] = {k: 0 for k in PREFIXES}

    def next(self, source: str) -> str:
        _validate_source(source)
        self._counters[source] += 1
        return f"{PREFIXES[source]}-{self._counters[source]}"
