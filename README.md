# ArXiv Data

`ArXiv-data` is the public, versioned data source produced by PaperFlow. It is
separate from the [`PaperRead`](https://github.com/threeyang3/PaperRead)
application repository so that software releases and data refreshes can evolve
independently.

The feed contains:

- arXiv metadata normalized to the PaperFlow Raw schema;
- schema-validated AI analyses with provider, model, prompt and source-hash
  provenance;
- manifests and checksums used to verify every published record.

The feed does **not** contain PDFs, extracted full text, rendered Obsidian
notes, User records, credentials, logs or local filesystem paths.

## Subscribe

```powershell
paperflow source add https://github.com/threeyang3/ArXiv-data.git --name arxiv-data
paperflow source inspect arxiv-data
paperflow source sync arxiv-data --dry-run
paperflow source sync arxiv-data
```

Subscribers execute no code from this repository. PaperFlow clones it as
read-only data, validates schemas and checksums, applies the configured trust
policy, and writes remote records only to the subscription cache.

## Licensing

Published data records are licensed under CC BY 4.0. Paper metadata and paper
content remain subject to their original sources and licenses. The PaperFlow
software itself is distributed separately under the MIT License.

## 质量审计与云端接入

本仓库增加只读、无需 Agent CLI 的分析质量审计：`python3 scripts/audit_quality.py`。它提示历史分析中可能过时的代码／权重状态等结论，但**不会擅自改写原分析**。端到端云端发现与客户端接入的协议和边界见 [docs/cloud-workflow.md](docs/cloud-workflow.md)；目前尚未部署无人值守任务。
