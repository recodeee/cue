from hydra.phase1.seed_ids import SeedIdAssigner


def test_assign_preserves_source_prefix() -> None:
    a = SeedIdAssigner()
    assert a.next("semgrep") == "T-SEM-1"
    assert a.next("semgrep") == "T-SEM-2"
    assert a.next("osv") == "T-OSV-1"
    assert a.next("lang_checker") == "T-LANG-1"
    assert a.next("echo") == "E-1"
    assert a.next("navigator") == "N-1"


def test_unknown_source_raises() -> None:
    a = SeedIdAssigner()
    import pytest
    with pytest.raises(ValueError):
        a.next("made_up")
