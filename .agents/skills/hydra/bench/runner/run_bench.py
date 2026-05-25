"""Bench runner — judge-free scoring + baseline writer (MVP; full harness deferred)."""
from __future__ import annotations

import argparse
import json
import statistics
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

import yaml

from bench.runner.scoring import CaseScore, score_case

ROOT = Path(__file__).resolve().parents[2]
CASES_DIR = ROOT / "bench" / "cases"
BASELINES_DIR = ROOT / "bench" / "baselines"


def load_ground_truth(case_id: str) -> list[dict[str, Any]]:
    path = CASES_DIR / case_id / "expected_findings.jsonl"
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def load_manifest(case_id: str) -> dict[str, Any]:
    return cast(dict[str, Any], yaml.safe_load((CASES_DIR / case_id / "manifest.yaml").read_text()))


def run_single_case(case_id: str, candidates_path: Path) -> CaseScore:
    gt = load_ground_truth(case_id)
    candidates = [
        json.loads(line)
        for line in candidates_path.read_text().splitlines()
        if line.strip()
    ]
    return score_case(gt, candidates)


def write_baseline(
    label: str,
    commit_sha: str,
    runs: list[dict[str, Any]],
    output_path: Path,
) -> None:
    """Write baseline file with median-of-runs metrics."""
    by_case: dict[str, list[CaseScore]] = {}
    for run in runs:
        for case_id, score in run["scores"].items():
            by_case.setdefault(case_id, []).append(score)

    aggregated = {
        case_id: {
            "median_f1": statistics.median(s.f1 for s in scores),
            "median_recall": statistics.median(s.recall for s in scores),
            "median_precision": statistics.median(s.precision for s in scores),
            "median_critical_recall": statistics.median(s.critical_recall for s in scores),
            "runs": [asdict(s) for s in scores],
        }
        for case_id, scores in by_case.items()
    }

    payload = {
        "label": label,
        "captured_at": datetime.now(UTC).isoformat(),
        "commit_sha": commit_sha,
        "cases": aggregated,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True, help="case id (e.g. 01-axios-header-injection)")
    parser.add_argument("--candidates", required=True, type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    score = run_single_case(args.case, args.candidates)
    if args.json:
        print(json.dumps(score.__dict__, indent=2))
    else:
        print(
            f"Case {args.case}: F1={score.f1:.2f} R={score.recall:.2f} "
            f"P={score.precision:.2f} crit_R={score.critical_recall:.2f}"
        )


if __name__ == "__main__":
    main()
