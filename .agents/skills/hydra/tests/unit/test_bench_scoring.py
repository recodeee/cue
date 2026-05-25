from bench.runner.scoring import score_case


def test_exact_match_full_recall() -> None:
    gt = [{
        "title": "Unvalidated auth header",
        "file": "src/a.ts",
        "lines": "14-28",
        "severity": "SERIOUS",
        "issue_class": "auth_bypass",
        "mandatory": True,
    }]
    candidates: list[dict[str, object]] = [{
        "title": "Authorization header forwarded without check",
        "file": "src/a.ts",
        "lines": "14-28",
        "severity": "SERIOUS",
        "issue_class": "auth_bypass",
        "position": "REJECT",
    }]
    result = score_case(gt, candidates, file_match_weight=1.0)
    assert result.recall == 1.0
    assert result.precision == 1.0
    assert result.f1 == 1.0


def test_missing_mandatory_zero_recall() -> None:
    gt = [{"title": "x", "file": "a.ts", "lines": "1-1", "severity": "SERIOUS",
           "issue_class": "auth_bypass", "mandatory": True}]
    result = score_case(gt, [], file_match_weight=1.0)
    assert result.recall == 0.0
    assert result.critical_recall == 0.0


def test_noise_drops_precision() -> None:
    gt = [{"title": "x", "file": "a.ts", "lines": "1-1", "severity": "SERIOUS",
           "issue_class": "auth_bypass", "mandatory": True}]
    candidates: list[dict[str, object]] = [
        {"title": "x", "file": "a.ts", "lines": "1-1", "severity": "SERIOUS",
         "issue_class": "auth_bypass"},
        {"title": "irrelevant", "file": "b.ts", "lines": "5-5",
         "severity": "MINOR", "issue_class": "other"},
    ]
    result = score_case(gt, candidates, file_match_weight=1.0)
    assert result.recall == 1.0
    assert result.precision == 0.5
    assert 0.6 < result.f1 < 0.7


def test_range_overlap_still_matches() -> None:
    gt = [{"title": "x", "file": "a.ts", "lines": "14-28", "severity": "SERIOUS",
           "issue_class": "auth_bypass", "mandatory": True}]
    candidates: list[dict[str, object]] = [{"title": "x", "file": "a.ts", "lines": "20-32",
                   "severity": "SERIOUS", "issue_class": "auth_bypass",
                   "position": "CONCERN"}]
    result = score_case(gt, candidates, file_match_weight=1.0)
    assert result.recall == 1.0
