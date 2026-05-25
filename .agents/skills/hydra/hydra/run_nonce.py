"""Per-run nonce + <<UNTRUSTED_*>> wrapper helpers.

UNTRUSTED_RE: detection regex for trusted-zone boundaries. It enforces
matching `kind` and `nonce` between open and close tags via backreferences,
so forged close tags with a different nonce will NOT prematurely close
a wrapper.
"""
from __future__ import annotations

import re
import secrets

UNTRUSTED_RE = re.compile(
    r"<<UNTRUSTED_(?P<kind>[A-Za-z_]+)_(?P<nonce>[0-9a-f]{6})>>"
    r".*?"
    r"<<END_UNTRUSTED_(?P=kind)_(?P=nonce)>>",
    re.DOTALL,
)

_KIND_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def mint_nonce() -> str:
    """6-hex-char nonce (48 bits). Minted at Phase 0; reused through the run."""
    return secrets.token_hex(3)


def wrap_untrusted(kind: str, nonce: str, body: str) -> str:
    """Wrap untrusted content with per-run-tagged delimiters.

    `kind` examples: PR_DIFF, PR_DESCRIPTION, TOOL_OUTPUT_SEMGREP,
                     ADVISOR_OUTPUT_cassandra, CONFIG_JSON.
    """
    if not _KIND_PATTERN.fullmatch(kind):
        raise ValueError(
            f"kind must match {_KIND_PATTERN.pattern!r}, got {kind!r}"
        )
    if not re.fullmatch(r"[0-9a-f]{6}", nonce):
        raise ValueError(f"nonce must be 6 hex chars, got {nonce!r}")
    return f"<<UNTRUSTED_{kind}_{nonce}>>{body}<<END_UNTRUSTED_{kind}_{nonce}>>"
