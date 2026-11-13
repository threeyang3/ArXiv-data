#!/usr/bin/env python3
"""Non-destructive audit of public AI analysis coverage and perishable claims.

The PaperFlow Feed schema/checksum validator remains the integrity gate.
This audit is advisory: it never rewrites immutable AI records or claims that a
full PDF was read merely because a content hash is present.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PERISHABLE_CLAIMS = (
    "代码未开源", "未公开代码", "代码和数据集均未开源",
    "没有公开代码", "缺乏模型权重发布", "no code released",
    "not open source", "no weights released",
)


def _safe_file(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise ValueError("invalid Feed manifest path")
    parts = relative.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError("unsafe Feed manifest path")
    path = (root / relative).resolve()
    path.relative_to(root.resolve())
    if not path.is_file():
        raise FileNotFoundError(relative)
    return path


def audit(root: Path = ROOT) -> dict[str, Any]:
    root = root.resolve()
    manifest = root / "manifests/analyses.jsonl"
    issues: list[dict[str, str]] = []
    records = 0
    for lineno, line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        entry = json.loads(line)
        path = _safe_file(root, entry.get("path", ""))
        record = json.loads(path.read_text(encoding="utf-8"))
        uid = str(record.get("paper_uid") or "")
        records += 1
        if uid != entry.get("paper_uid") or record.get("analysis_id") != entry.get("analysis_id"):
            raise ValueError(f"manifest identity mismatch on line {lineno}")
        identity = record.get("identity") or {}
        analysis = record.get("analysis") or {}
        if (
            record.get("status") != "complete"
            or not identity.get("source_content_hash")
            or not identity.get("model")
            or not identity.get("prompt_version")
        ):
            issues.append({"paper_uid": uid, "kind": "incomplete-provenance",
                           "detail": "Validate source hash/model/prompt before reuse."})
        sections = analysis.get("sections") or {}
        if not isinstance(sections, dict) or not all(
            sections.get(key) for key in ("method", "experiments", "limitations")
        ):
            issues.append({"paper_uid": uid, "kind": "limited-analysis-coverage",
                           "detail": "Method, experiments or limitations lack structured detail."})
        # Reproducibility claims change after paper publication. Flag for
        # human research, never silently edit an immutable analysis or assert
        # that the historical claim was false at generation time.
        candidates = [
            str(analysis.get("ai_reproducibility_reason") or ""),
            str(analysis.get("ai_recommendation") or ""),
            str(sections.get("limitations") or ""),
        ]
        if any(token.casefold() in " ".join(candidates).casefold() for token in PERISHABLE_CLAIMS):
            issues.append({"paper_uid": uid, "kind": "time-sensitive-resource-claim",
                           "detail": "Recheck official code/weights/datasets; original analysis is historical."})
    return {
        "schema_version": 1,
        "analysis_count": records,
        "advisory_issues": len(issues),
        "issues": issues,
        "note": "Schema/checksums are separate checks. A source hash is not proof of complete PDF or figure coverage.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="Print machine-readable advisory report")
    args = parser.parse_args()
    result = audit()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Advisory analysis quality: {result['analysis_count']} records, {result['advisory_issues']} review flags.")
        for issue in result["issues"]:
            print(f"  {issue['paper_uid']}: {issue['kind']} — {issue['detail']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
