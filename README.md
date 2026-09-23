# QA AI Agent

This repository is a lightweight QA workflow for turning Functional Specification Documents (FSDs) into structured, testable artifacts. It is designed to help teams convert source documents from Word into Markdown, assess readiness for testing, and generate traceable test cases without inventing requirements.

## Purpose

The project supports a simple QA pipeline:

1. Convert a Word-based FSD into Markdown
2. Check the FSD for missing details, contradictions, and untestable requirements
3. Generate test cases tied to requirement IDs
4. Review the generated test cases for traceability and quality

This repo is intended as a generator and validation toolkit for specification-driven QA work.

## Repository structure

```text
.
├── .github/
│   ├── agents/
│   ├── prompts/
│   └── copilot-instructions.md
├── docs/
│   ├── fsd-source/          # Original .docx FSD files
│   ├── fsd/                 # Converted Markdown FSDs
│   ├── analysis/            # Readiness reports for FSDs
│   │   └── questions/       # Open questions captured during FSD review
│   ├── testcases/           # Generated test case artifacts
│   └── reviews/             # Test case review reports
├── scripts/
│   └── docx_to_md.py        # DOCX to Markdown conversion script
├── templates/
│   └── testcase-template.md # Standard test case template
├── README.md
├── .gitignore
└── ...
```

## Core workflow

### Step 1: FSD conversion and image prompt preparation

This repository expects the workflow to proceed in this order:

1. Run the FSD Converter agent to convert each `.docx` source in `docs/fsd-source/` into Markdown in `docs/fsd/`.
2. Run the FSD Image Prompt Generator agent to create prompt files for any images that still need descriptions.
3. Run the generated prompts so the agent can attach image descriptions beneath each `![...](...)` reference in the Markdown FSD.

#### 1.1 FSD Converter agent

The FSD Converter agent follows the instructions in `.github/agents/fsd-converter.agent.md` and converts files using:

```bash
python scripts/docx_to_md.py docs/fsd-source/<name>.docx docs/fsd/<name>.md docs/fsd/<name>-media
```

This step:

- reads the Word document
- extracts text and headings into Markdown
- converts tables into Markdown tables
- extracts embedded images into `docs/fsd/<name>-media/`

#### 1.2 FSD Image Prompt Generator agent

After conversion, run the FSD Image Prompt Generator agent defined in `.github/agents/fsd-image-prompt-generator.agent.md`.

This agent checks each Markdown FSD for image references, matches them to extracted image files, and creates a prompt file such as:

```text
.github/prompts/generated.describe-<name>-images.prompt.md
```

Those generated prompts are then executed to describe the attached images and insert blocks like:

```md
> **IMAGE DESCRIPTION** (DRAFT, needs human verification)
> <description>
```

below each matching image reference.

### 2) Check FSD readiness

The repo includes prompts and agents for analyzing whether an FSD is ready for test generation. The analyzer flags:

- missing or ambiguous requirements
- contradictions between requirements
- missing limits, error cases, and formats
- untestable language such as vague quality claims
- missing image descriptions for referenced graphical content
- malformed Markdown tables

The readiness review produces:

- readiness reports in `docs/analysis/`
- open questions in `docs/analysis/questions/`

This ensures any requirements that are vague, untestable, or missing needed detail are recorded clearly instead of guessed.

### 3) Generate test cases

The test case generator reads each FSD and creates structured test cases using the template in `templates/testcase-template.md`.

Key rules from the project guidance:

- never invent requirements that are not in the FSD
- record unclear items as open questions
- maintain requirement traceability
- output artifacts in the `docs/testcases/` folder

### 4) Review generated test cases

A review step checks whether the generated cases:

- cover all real requirements
- match the stated behavior in the FSD
- maintain traceability
- avoid poor or duplicate test coverage

Reports are stored in `docs/reviews/`.

## Project scripts and files

### `scripts/docx_to_md.py`

Converts `.docx` FSD files into Markdown while also extracting image assets into a sibling media directory.

### `templates/testcase-template.md`

Defines the expected structure for generated test cases, including columns for:

- test case ID
- requirement ID
- title
- preconditions
- steps
- test data
- expected result
- priority
- type
- notes

### `.github/copilot-instructions.md`

Contains shared instructions for the assistant, including the rule to avoid inventing requirements and to use consistent IDs.

## Typical usage

```text
Step 1 workflow:
1. fsd-converter.agent.md
2. fsd-image-prompt-generator.agent.md
3. run the generated prompts

Then continue with:
4. analyze-fsd.prompt.md
5. generate-testcases.prompt.md
6. review-testcases.prompt.md
```

Example conversion command:

```bash
python scripts/docx_to_md.py docs/fsd-source/login-module.docx docs/fsd/login-module.md docs/fsd/login-module-media
```

Example generated prompt pattern:

```text
.github/prompts/generated.describe-login-module-images.prompt.md
```

## Notes

- This repo is focused on QA artifact generation and review, not on running an app or service.
- The source of truth for requirements is the FSD itself.
- Any unclear or unsupported requirement should be documented as an open question instead of guessed.

## Minimum setup

- Python 3.x
- A source `.docx` FSD in `docs/fsd-source/`
- Access to the project prompts and agent instructions in `.github/`

## Summary

This repository provides a practical QA pipeline for converting functional specs, validating their testability, and generating structured test cases while preserving traceability and confidence.
