---
name: review-testcases
agent: Test Case Reviewer
description: Independently review generated test cases against their FSDs
---
Look in `docs/testcases/` for test case CSV files, and match each one to its FSD in `docs/fsd/`
by filename.

For each pair:
1. Read the FSD and the test case CSV (and the traceability and open-questions CSVs if present).
2. Review as instructed.
3. Save the report to `docs/reviews/<fsd-filename>-review.md`.

Do not modify any test case files. If a test case CSV has no matching FSD, list it in the
summary as "orphaned" and skip it.

If a review already exists for an FSD, skip it unless I say "regenerate".

Do not stop to ask me questions mid-run.

When done, give me a summary table: FSD file, verdict (Pass / Pass with fixes / Fail),
number of High / Medium / Low issues, and number of missing scenarios.