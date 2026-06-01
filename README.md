# Exam Materials Studio

Exam Materials Studio is an open-source toolkit for teachers, tutors, and small
education teams who need to turn syllabus topics into printable revision packs,
answer keys, and simple static catalog pages.

The project started from the repeatable parts of ExamMason's materials workflow:
pack structure, answer-key generation, printable Markdown, and lightweight
static publishing. It does not include private prospect lists, payment
workflows, or commercial customer data.

## What It Does

- Builds printable Markdown revision packs from structured JSON.
- Generates separate answer keys for marking or self-study.
- Creates a static HTML catalog page for sharing available packs.
- Validates pack structure before output is written.
- Ships with sample IGCSE-style packs that can be reused as templates.

## Why This Is Useful

Many small tutoring centres and independent teachers maintain learning material
in scattered documents, spreadsheets, and chat threads. This repository gives
them a reproducible, inspectable format for building and updating exam-support
packs without needing a full publishing platform.

It is intentionally plain Python and file-based so it can run on school laptops,
GitHub Actions, or a cheap static hosting workflow.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
exam-materials-studio build examples/igcse_computer_science_boolean_logic.json --out generated
```

Generated files:

- `generated/igcse-computer-science-boolean-logic.md`
- `generated/igcse-computer-science-boolean-logic-answer-key.md`
- `generated/index.html`

You can also run the module directly:

```bash
python3 -m exam_materials_studio build examples/igcse_economics_definitions.json --out generated
```

## Pack Format

Each pack is JSON with this shape:

```json
{
  "title": "IGCSE Computer Science Boolean Logic",
  "slug": "igcse-computer-science-boolean-logic",
  "subject": "Computer Science",
  "level": "IGCSE",
  "summary": "Targeted practice for Boolean logic gates and truth tables.",
  "skills": ["truth tables", "logic gates"],
  "items": [
    {
      "prompt": "State the output of A AND B when A = 1 and B = 0.",
      "answer": "0",
      "explanation": "AND only outputs 1 when both inputs are 1."
    }
  ]
}
```

## Development

```bash
python3 -m unittest discover
python3 -m exam_materials_studio build examples/igcse_computer_science_boolean_logic.json --out generated
```

## Roadmap

- YAML input support.
- PDF export through optional backends.
- More sample packs for IGCSE Economics, Accounting, Computer Science, and Maths.
- Teacher-facing validation reports for missing answers and weak explanations.
- GitHub Action examples for publishing pack catalogs to Pages.

## Open Source Scope

This repository is for the reusable tooling. Commercial lesson packs, client
communications, payment setup, and prospect data should stay outside the repo.

