"""Case-level scoring. Judge-free — used for unit-testable scoring logic."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CaseScore:
    recall: float
    precision: float
    f1: float
    critical_recall: float
    matched: int
    missed: int
    noise: int


@dataclass(frozen=True)
class FindingMatch:
    ground_truth_idx: int
    candidate_idx: int
    score: float


def _parse_range(lines: str) -> tuple[int, int]:
    if "-" in lines:
        a, b = lines.split("-", 1)
        return int(a), int(b)
    n = int(lines)
    return n, n


def _ranges_overlap(a: str, b: str, tol: int = 10) -> bool:
    try:
        a1, a2 = _parse_range(a)
        b1, b2 = _parse_range(b)
    except ValueError:
        return False
    return not (a2 + tol < b1 or b2 + tol < a1)


def _match_score(gt: dict[str, object], cand: dict[str, object], file_match_weight: float) -> float:
    if gt["file"] != cand.get("file"):
        return 0.0
    gt_lines = str(gt["lines"])
    cand_lines = str(cand.get("lines", ""))
    if not _ranges_overlap(gt_lines, cand_lines):
        return 0.0
    score = file_match_weight
    if gt["issue_class"] == cand.get("issue_class"):
        score += 0.5
    if gt["severity"] == cand.get("severity"):
        score += 0.3
    return score


def score_case(
    ground_truth: list[dict[str, object]],
    candidates: list[dict[str, object]],
    *,
    file_match_weight: float = 0.6,
    match_threshold: float = 0.8,
) -> CaseScore:
    """Greedy one-to-one matching on (file, range-overlap, issue_class)."""
    used_candidates: set[int] = set()
    matches: list[FindingMatch] = []

    for gi, gt in enumerate(ground_truth):
        best: FindingMatch | None = None
        for ci, cand in enumerate(candidates):
            if ci in used_candidates:
                continue
            s = _match_score(gt, cand, file_match_weight)
            if s >= match_threshold and (best is None or s > best.score):
                best = FindingMatch(gi, ci, s)
        if best is not None:
            matches.append(best)
            used_candidates.add(best.candidate_idx)

    matched = len(matches)
    mandatory = [g for g in ground_truth if g.get("mandatory", False)]
    matched_mandatory = sum(
        1 for m in matches if ground_truth[m.ground_truth_idx].get("mandatory", False)
    )
    missed = len(ground_truth) - matched
    noise = len(candidates) - matched

    recall = matched / max(len(ground_truth), 1)
    precision = matched / max(len(candidates), 1)
    f1 = 2 * recall * precision / max(recall + precision, 1e-9)
    critical_recall = matched_mandatory / max(len(mandatory), 1)
    return CaseScore(
        recall=recall,
        precision=precision,
        f1=f1,
        critical_recall=critical_recall,
        matched=matched,
        missed=missed,
        noise=noise,
    )
