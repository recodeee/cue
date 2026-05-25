import re

from hydra.run_nonce import UNTRUSTED_RE, mint_nonce, wrap_untrusted


def test_mint_nonce_format() -> None:
    nonce = mint_nonce()
    assert re.fullmatch(r"[0-9a-f]{6}", nonce)


def test_mint_nonce_unique_across_calls() -> None:
    # 48-bit nonce — collisions are negligible for any realistic sample
    samples = {mint_nonce() for _ in range(1000)}
    assert len(samples) == 1000


def test_wrap_untrusted_emits_correct_tags() -> None:
    out = wrap_untrusted("PR_DIFF", "abc123", "diff --git a/x b/x\n")
    assert out.startswith("<<UNTRUSTED_PR_DIFF_abc123>>")
    assert out.endswith("<<END_UNTRUSTED_PR_DIFF_abc123>>")


def test_untrusted_re_matches_wrapped_block() -> None:
    wrapped = wrap_untrusted("ADVISOR_OUTPUT_cassandra", "abc123", "finding")
    assert UNTRUSTED_RE.search(wrapped) is not None


def test_untrusted_re_rejects_mismatched_nonce() -> None:
    forged = "<<UNTRUSTED_KIND_aaaaaa>>body<<END_UNTRUSTED_KIND_bbbbbb>>"
    assert UNTRUSTED_RE.search(forged) is None


def test_untrusted_re_rejects_mismatched_kind() -> None:
    forged = "<<UNTRUSTED_KINDA_aaaaaa>>body<<END_UNTRUSTED_KINDB_aaaaaa>>"
    assert UNTRUSTED_RE.search(forged) is None


def test_untrusted_re_matches_multiline_body() -> None:
    wrapped = wrap_untrusted("PR_DIFF", "abc123", "line1\nline2\nline3")
    assert UNTRUSTED_RE.search(wrapped) is not None


def test_wrap_untrusted_rejects_bad_kind() -> None:
    import pytest
    with pytest.raises(ValueError, match="kind must match"):
        wrap_untrusted("BAD>>INJECT", "abc123", "body")


def test_wrap_untrusted_rejects_bad_nonce() -> None:
    import pytest
    with pytest.raises(ValueError, match="nonce must be 6 hex"):
        wrap_untrusted("PR_DIFF", "XXXXXX", "body")
