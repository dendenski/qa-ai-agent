---
name: analyze-fsd
agent: FSD Analyzer
description: Check every FSD in docs/fsd for testability and write readiness reports
---
Look in the `docs/fsd/` folder and find all FSD files (.md or .txt).

For each FSD:
1. Read the whole file.
2. Assess every requirement as instructed.
3. Save the report to `docs/analysis/<fsd-filename>-readiness.md`.

If a readiness report already exists for an FSD, skip it unless I say "regenerate".

Do not stop to ask me questions mid-run; record them in the reports instead.

When done, give me a summary table: FSD file, requirements Ready / Needs clarification /
Not testable, and the verdict (Ready to generate / Resolve blockers first).