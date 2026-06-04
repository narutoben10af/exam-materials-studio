# Exam Materials Studio

Exam Materials Studio is an open-source toolkit for teachers, tutors, and small
education teams who need to turn syllabus topics into printable education
resources, answer keys, and simple static catalog pages.

The project started from the repeatable parts of ExamMason's materials workflow:
pack structure, answer-key generation, printable Markdown, HTML export, and
lightweight static publishing. It does not include private prospect lists,
payment workflows, or commercial customer data.

## What It Does

- Builds printable Markdown and HTML resources from structured JSON, YAML, or CSV.
- Generates separate answer keys for marking or self-study.
- Creates static Markdown, HTML, and JSON catalog files for sharing and indexing
  available packs.
- Validates resource structure before output is written.
- Supports optional metadata for education systems, exam boards, courses, and
  curriculum references.
- Tracks prerequisites so resources can fit into lesson sequences, tutoring
  pathways, and revision plans.
- Tracks materials so teachers can prepare supplies, devices, files, or tools
  before running a resource.
- Tracks delivery modes so resources can be planned for classroom, tutoring,
  self-study, homework, revision, seminar, or discussion workflows.
- Tracks estimated duration so resources can support lesson, tutoring, and
  independent-study planning.
- Tracks optional item time metadata so lesson steps, tutoring tasks, worksheet
  activities, and study-guide prompts can show pacing.
- Tracks optional item difficulty metadata for foundation, core, and extension
  activities.
- Tracks optional item phase metadata so resources can show lesson flow across
  warm-up, guided practice, application, assessment, reflection, and discussion.
- Tracks optional item marks so assessment resources can show scoring weight
  and inventory reports can roll up total marks.
- Tracks optional item command words so teachers can review assessment intent
  across define, explain, calculate, discuss, compare, identify, and evaluate tasks.
- Tracks optional item rubric points so teacher answer keys can include marking
  criteria while learner-facing resources stay clean.
- Provides scaffold presets for common preschool, primary, exam-board, and
  university workflows.
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
- `generated/index.md`
- `generated/index.json`
- `generated/index.html`

You can also run the module directly:

```bash
python3 -m exam_materials_studio build examples/igcse_economics_definitions.json --out generated
```

## Validate Resources

Before publishing or adding a new subject area, run validation:

```bash
exam-materials-studio validate examples/*.json examples/*.yaml examples/*.csv --report generated/validation-report.txt
```

Validation reports separate structural errors from quality warnings. Errors
return a non-zero exit code. Warnings call out weaker maintainer signals such as
missing education-system metadata, missing course fields, thin answer-key
explanations, missing learning objectives, missing curriculum references,
missing estimated duration, missing item difficulty, or very short resources.

## Inventory Coverage

Use the inventory command to see what the repository currently covers:

```bash
exam-materials-studio inventory examples/*.json examples/*.yaml examples/*.csv --out generated/inventory.md --csv generated/inventory.csv
```

The Markdown report summarizes resources and item counts by subject, level,
resource type, education system, exam board, course, delivery mode, command
word, learning phase, and difficulty coverage. The CSV export gives a
spreadsheet-friendly row per resource, including delivery modes, command words,
learning phases, estimated duration, item-level planned time, total marks,
rubric points, and
foundation/core/extension/unspecified difficulty counts for maintainer review.

## Scaffold New Resources

Use the scaffold command to start a new resource without copying an existing
example:

```bash
exam-materials-studio scaffold \
  --title "Primary Fractions Starter" \
  --subject Mathematics \
  --level Primary \
  --resource-type worksheet \
  --education-system "General primary" \
  --course Fractions \
  --duration-minutes 30 \
  --prerequisites "Count equal parts in a shape" \
  --materials "Fraction strips;Counters" \
  --delivery-modes "classroom;tutoring" \
  --learning-objectives "Represent equivalent fractions with simple models" \
  --curriculum-references "Local Grade 4 Fractions" \
  --skills "fractions;equivalent fractions" \
  --out examples/primary_fractions_starter.json
```

For common systems and levels, use a preset instead of repeating the same
metadata:

```bash
exam-materials-studio presets

exam-materials-studio scaffold \
  --preset cambridge-igcse \
  --title "IGCSE Chemistry Acids Starter" \
  --subject Chemistry \
  --course "0620 Chemistry" \
  --learning-objectives "Classify acids and bases using common indicators" \
  --curriculum-references "Cambridge IGCSE Chemistry 0620: acids and bases" \
  --skills "acids;bases" \
  --out examples/igcse_chemistry_acids_starter.json
```

Built-in presets cover `preschool`, `primary`, `cambridge-igcse`,
`cambridge-a-level`, `ap`, `ib-dp`, and `university`. Explicit flags such as
`--level`, `--resource-type`, `--education-system`, and `--exam-board` override
the preset when a resource needs a local variation.

Use `--format yaml` for a hand-editable starter or `--format csv` for a
spreadsheet-friendly starter instead. The command refuses to overwrite existing
files unless `--force` is provided.

## Resource Format

Each resource can be authored as JSON, YAML, or CSV. JSON is best for
machine-generated structured files. YAML is useful for hand-edited resources
where teachers want readable lists and indentation. CSV is useful when teachers
are drafting in a spreadsheet.

JSON resources use this shape. The `resource_type`, `education_system`,
`exam_board`, `course`, `duration_minutes`, `prerequisites`, `materials`,
`delivery_modes`, `learning_objectives`, and `curriculum_references` fields are
optional, but useful for catalogs and teacher-facing resources that span
different levels, curricula, and delivery settings. Each item can also include
optional `difficulty` metadata using `foundation`, `core`, or `extension`, plus
optional `phase` metadata such as `warm-up`, `guided-practice`, `application`,
`assessment`, or `reflection`, plus optional positive-integer `time_minutes`
metadata for item pacing. Items can also include optional positive-integer
`marks` metadata for assessment weighting and optional `command_word` metadata for
assessment intent. Optional `rubric` bullets are teacher-facing marking criteria
that appear in answer keys and coverage reports, not in learner-facing resources.

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
  "duration_minutes": 25,
  "prerequisites": [
    "Recognise binary values 0 and 1.",
    "Read simple two-column truth tables."
  ],
  "materials": [
    "Printed worksheet or shared digital copy.",
    "Logic-gate reference sheet."
  ],
  "delivery_modes": [
    "classroom",
    "revision",
    "self-study"
  ],
  "summary": "Targeted practice for Boolean logic gates and truth tables.",
  "learning_objectives": [
    "Complete truth-table outputs for common logic gates.",
    "Translate simple real-world rules into Boolean expressions."
  ],
  "curriculum_references": [
    "Cambridge IGCSE Computer Science 0478: logic gates",
    "Cambridge IGCSE Computer Science 0478: truth tables"
  ],
  "skills": ["truth tables", "logic gates"],
  "items": [
    {
      "phase": "warm-up",
      "time_minutes": 5,
      "difficulty": "foundation",
      "marks": 1,
      "command_word": "state",
      "prompt": "State the output of A AND B when A = 1 and B = 0.",
      "answer": "0",
      "explanation": "AND only outputs 1 when both inputs are 1.",
      "rubric": [
        "1 mark for the correct output."
      ]
    }
  ]
}
```

CSV resources use one row per activity, question, or teacher note. Resource
metadata is read from the first row. `skills`, `prerequisites`, `materials`,
`delivery_modes`, `learning_objectives`, and `curriculum_references` are
separated with semicolons:

```csv
title,slug,subject,level,resource_type,education_system,exam_board,course,duration_minutes,prerequisites,materials,delivery_modes,summary,skills,learning_objectives,curriculum_references,type,phase,time_minutes,difficulty,marks,command_word,rubric,prompt,answer,explanation
Primary Science Materials,primary-science-materials,Science,Primary,lesson-resource,General primary,,Materials and properties,25,Name common classroom objects,Wood sample;Metal spoon,classroom;tutoring,A simple primary science resource,classification;materials,Classify everyday materials;Link properties to uses,Primary science: everyday materials,activity,warm-up,5,foundation,1,sort,1 mark for grouping objects by material.,Sort objects by material.,Objects are grouped by material.,This checks classification by observable properties.
```

YAML resources use the same fields as JSON:

```yaml
title: Secondary History Source Analysis
slug: secondary-history-source-analysis
subject: History
level: Secondary
resource_type: source-analysis
education_system: General secondary
course: Historical source skills
duration_minutes: 30
prerequisites:
  - Identify the author and date of a historical source.
  - Distinguish fact from opinion in a short text.
materials:
  - Printed or projected historical source extract.
  - Highlighters or annotation tools.
delivery_modes:
  - classroom
  - discussion
  - homework
summary: A short resource for evaluating historical source reliability and usefulness.
skills:
  - provenance
  - reliability
items:
  - type: concept-check
    phase: warm-up
    time_minutes: 8
    difficulty: foundation
    marks: 2
    command_word: identify
    prompt: Identify two provenance details a historian should check before using a source.
    answer: The author and the date of creation.
    explanation: Provenance details such as author, date, audience, and origin help establish context.
    rubric:
      - 1 mark for identifying the author.
      - 1 mark for identifying the date or origin.
```

## Development

```bash
python3 -m unittest discover -s tests
python3 -m exam_materials_studio presets --out generated/scaffold-presets.md
python3 -m exam_materials_studio scaffold --preset primary --title "Primary Fractions Starter" --subject Mathematics --course Fractions --delivery-modes "classroom;tutoring" --learning-objectives "Represent equivalent fractions with simple models" --curriculum-references "Local Grade 4 Fractions" --skills "fractions;equivalent fractions" --out generated/primary-fractions-starter.json
python3 -m exam_materials_studio scaffold --preset primary --title "Primary Fractions YAML Starter" --subject Mathematics --course Fractions --delivery-modes "classroom;tutoring" --learning-objectives "Represent equivalent fractions with simple models" --curriculum-references "Local Grade 4 Fractions" --skills "fractions;equivalent fractions" --format yaml --out generated/primary-fractions-yaml-starter.yaml
python3 -m exam_materials_studio validate examples/*.json examples/*.yaml examples/*.csv
python3 -m exam_materials_studio inventory examples/*.json examples/*.yaml examples/*.csv --out generated/inventory.md --csv generated/inventory.csv
python3 -m exam_materials_studio build examples/*.json examples/*.yaml examples/*.csv --out generated
```

## Roadmap

- PDF export through optional backends.
- More sample resources across preschool, primary, secondary, exam-board, vocational, and university workflows.
- More teacher-facing validation checks for missing answers, weak explanations,
  and incomplete progression metadata.
- GitHub Action examples for publishing pack catalogs to Pages.

## Open Source Scope

This repository is for the reusable tooling. Commercial lesson packs, client
communications, payment setup, and prospect data should stay outside the repo.
