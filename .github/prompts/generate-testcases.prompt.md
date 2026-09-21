---
name: generate-testcases
agent: Test Case Generator
description: Generate test cases for every FSD found in docs/fsd
---
Look in the `docs/fsd/` folder and find all FSD files (.md or .txt).

For each FSD:
1. Read the whole file.
2. Generate test cases following your instructions.
3. Save the results to `docs/testcases/<fsd-filename>-testcases.csv`
   and `docs/testcases/<fsd-filename>-traceability.csv`.

If `docs/testcases/` already has a CSV for an FSD, skip that FSD unless I say "regenerate".

When done, give me a short summary table: FSD file, number of requirements,
number of test cases, number of open questions, and number of requirements
skipped as untestable. Do not stop to ask me questions mid-run; record them in
the open-questions file instead.