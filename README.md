# Exam Materials Studio

Exam Materials Studio is an open-source toolkit for teachers, tutors, and small
education teams who need to turn syllabus topics into printable education
resources, answer keys, and simple static catalog pages.

The project started from the repeatable parts of ExamMason's materials workflow:
pack structure, answer-key generation, printable Markdown, HTML export, and
lightweight static publishing. It does not include private prospect lists,
payment workflows, or commercial customer data.

## What It Does

- Builds printable Markdown and HTML resources from structured JSON.
- Generates separate answer keys for marking or self-study.
- Creates a static HTML catalog page for sharing available packs.
- Validates resource structure before output is written.
- Supports optional metadata for education systems, exam boards, and courses.
- Ships with sample resources from preschool through university level.

## Why This Is Useful

Many small tutoring centres and independent teachers maintain learning material
in scattered documents, spreadsheets, and chat threads. This repository gives
them a reproducible, inspectable format for building and updating teaching
resources without needing a full publishing platform.

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
- `generated/igcse-computer-science-boolean-logic.html`
- `generated/igcse-computer-science-boolean-logic-answer-key.md`
- `generated/igcse-computer-science-boolean-logic-answer-key.html`
- `generated/index.html`

You can also run the module directly:

```bash
python3 -m exam_materials_studio build examples/igcse_economics_definitions.json --out generated
```

## Validate Resources

Before publishing or adding a new subject area, run validation:

```bash
exam-materials-studio validate examples/*.json --report generated/validation-report.txt
```

Validation reports separate structural errors from quality warnings. Errors
return a non-zero exit code. Warnings call out weaker maintainer signals such as
missing education-system metadata, missing course fields, thin answer-key
explanations, or very short resources.

## Resource Format

Each resource is JSON with this shape. The `resource_type`,
`education_system`, `exam_board`, and `course` fields are optional, but useful
for catalogs that span different levels and curricula.

```json
{
  "title": "IGCSE Computer Science Boolean Logic",
  "slug": "igcse-computer-science-boolean-logic",
  "subject": "Computer Science",
  "level": "IGCSE",
  "resource_type": "exam-practice",
  "education_system": "Cambridge International",
  "exam_board": "Cambridge",
  "course": "0478 Computer Science",
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
python3 -m unittest discover -s tests
python3 -m exam_materials_studio validate examples/*.json
python3 -m exam_materials_studio build examples/*.json --out generated
```

## Roadmap

- YAML input support.
- PDF export through optional backends.
- More sample resources across preschool, primary, secondary, exam-board, vocational, and university workflows.
- Teacher-facing validation reports for missing answers and weak explanations.
- GitHub Action examples for publishing pack catalogs to Pages.

## Open Source Scope

This repository is for the reusable tooling. Commercial lesson packs, client
communications, payment setup, and prospect data should stay outside the repo.
