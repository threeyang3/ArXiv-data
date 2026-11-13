# PaperFlow public Feed: quality review and cloud ingestion

This repository contains **public data**, not an unattended research agent.
Historical analyses remain immutable and their `analyzed_at` dates reflect
when those claims were recorded. `status=complete` means the schema-valid
analysis job completed; it **does not** guarantee that the PDF, every figure,
external code repository, or dataset availability was verified.

## Quality inspection

```bash
python3 scripts/audit_quality.py
python3 scripts/audit_quality.py --json
```

The advisory tool checks manifest identities, provenance completeness,
structured-method coverage and time-sensitive claims such as "code is not
open-source". It never writes to the Feed and it does not declare those
historical claims false. Re-check official repositories before using old
reproducibility scores. Example: the existing `arxiv:2410.24164` analysis
records publication-era code/weight availability; the current state of
`https://github.com/Physical-Intelligence/openpi` needs independent review.

The existing `paperflow publish validate` and `publish scan` remain the
only integrity/privacy gates. The advisory tool is an additional signal,
not a substitute.

## Cloud source workflow (planned; not deployed)

1. A scheduled ChatGPT job reads a reviewed research profile, a previously
   committed cursor and the current Feed manifest from GitHub.
2. It discovers arXiv candidates and deduplicates by `paper_uid`, keeping
   the arXiv source version independent of the paper identity.
3. It records the actual evidence available: `abstract-only`, `partial-text`,
   or `full-text`. No guessed PDF coverage, figure evidence or citation pages.
4. It stages candidate Raw/AI revisions according to PaperFlow's public schemas
   without overwriting prior analyses, private User notes or Community data.
5. It verifies identities, checksums, source provenance and allowed public
   fields, then commits a single validated update. Failed items retain an
   explicit retry record. A successful GitHub write is distinct from a client
   having imported the update.
6. Zotero/Obsidian consume the validated Feed and use the same `paper_uid`;
   detailed figures and human research notes live in the separate ReadPaper
   archive, not in this link-only Feed.

No PDFs, extracted full text, access tokens, local paths, human user notes,
or unlicensed figures belong in this public data repository. Do not create
an unattended agent that writes directly to `main` without publication checks.
Limit cloud operations to the smallest approved token scope and use a staging
branch/PR where content provenance is uncertain.

**Status:** protocol only. No ChatGPT scheduled task, deployed cloud runner
or native-client import acknowledgement is implied by this document.
