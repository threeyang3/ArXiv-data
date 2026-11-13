import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_quality.py"
spec = importlib.util.spec_from_file_location("audit_quality", SCRIPT)
audit_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit_module)


def _feed(tmp_path, *, uid="arxiv:2504.16054", analysis=None):
    relative = "papers/arxiv_2504.16054/ai/api/v1.json"
    target = tmp_path / relative
    target.parent.mkdir(parents=True)
    target.write_text(json.dumps({
        "paper_uid": uid,
        "analysis_id": "test12345678",
        "status": "complete",
        "identity": {
            "source_content_hash": "abc", "model": "model", "prompt_version": "v3",
        },
        "analysis": analysis or {
            "sections": {"method": "Method", "experiments": "Exp", "limitations": "Limits"},
        },
    }), encoding="utf-8")
    manifest = tmp_path / "manifests/analyses.jsonl"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(json.dumps({
        "paper_uid": uid, "analysis_id": "test12345678", "path": relative,
    }) + "\n", encoding="utf-8")
    return manifest


def test_audit_is_read_only_and_surfaces_perishable_claims(tmp_path: Path):
    _feed(tmp_path, analysis={
        "sections": {"method": "Method", "experiments": "Exp", "limitations": "代码未开源"},
    })
    before = sorted((p.relative_to(tmp_path).as_posix(), p.read_bytes())
                    for p in tmp_path.rglob("*") if p.is_file())
    result = audit_module.audit(tmp_path)
    after = sorted((p.relative_to(tmp_path).as_posix(), p.read_bytes())
                   for p in tmp_path.rglob("*") if p.is_file())
    assert result["analysis_count"] == 1
    assert result["advisory_issues"] == 1
    assert result["issues"][0]["kind"] == "time-sensitive-resource-claim"
    assert before == after


def test_manifest_identity_mismatch_fails(tmp_path: Path):
    manifest = _feed(tmp_path)
    content = json.loads(manifest.read_text(encoding="utf-8"))
    content["paper_uid"] = "arxiv:other"
    manifest.write_text(json.dumps(content), encoding="utf-8")
    with pytest.raises(ValueError, match="identity mismatch"):
        audit_module.audit(tmp_path)


def test_unsafe_manifest_path_is_rejected(tmp_path: Path):
    manifest = _feed(tmp_path)
    line = json.loads(manifest.read_text(encoding="utf-8"))
    line["path"] = "../secrets.txt"
    manifest.write_text(json.dumps(line), encoding="utf-8")
    with pytest.raises(ValueError, match="unsafe"):
        audit_module.audit(tmp_path)
