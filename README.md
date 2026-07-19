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
