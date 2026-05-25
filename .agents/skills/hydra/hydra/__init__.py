"""Hydra 2.0 Core — multi-advisor code review."""

__version__ = "2.0.0a0"
# SCHEMA_VERSION mirrors the Literal in envelopes.SeedReport.schema_version.
# pydantic Literal cannot reference this constant, so both must change together.
SCHEMA_VERSION = "2.0"
