# Resource Format

Exam Materials Studio uses small JSON and CSV formats so education resources can
be reviewed, versioned, regenerated, and published without a database.

## Required Fields

- `title`: Human-readable resource title.
- `slug`: Lowercase URL/file-safe identifier using letters, numbers, and hyphens.
- `subject`: Subject area, such as Economics, Early Mathematics, Biology, or Computer Science.
- `level`: Learner level, such as Preschool, Primary, IGCSE, A Level, AP, IB, Vocational, or University.
- `summary`: Short teacher-facing description.
- `skills`: Non-empty list of skills practised.
- `items`: Non-empty list of activities, questions, prompts, or teacher notes.

## Optional Scope Fields

- `resource_type`: For example `exam-practice`, `activity-sheet`, `lesson-note`, `study-guide`, or `worksheet`.
- `education_system`: For example `Cambridge International`, `IB`, `AP`, `US Common Core`, or `General early years`.
- `exam_board`: For exam-board-specific resources, such as `Cambridge`, `Pearson Edexcel`, or `AQA`.
- `course`: Course or specification identifier, such as `0478 Computer Science`.
- `learning_objectives`: Teacher-facing objectives describing what learners should be able to do.
- `curriculum_references`: Syllabus sections, standards, specification points, or module outcomes.

These fields make the catalog useful when the repository grows across subjects,
education systems, age ranges, and course types.

## Item Fields

- `prompt`: The learner-facing or teacher-facing task.
- `answer`: The expected answer, marking note, or suggested response.
- `explanation`: Optional reasoning for answer keys.
- `type`: Optional item type such as `question`, `activity`, `teacher-note`, `calculation`, or `discussion`.
- `difficulty`: Optional progression label. Supported values are `foundation`,
  `core`, and `extension`.

## CSV Input

CSV input is intended for spreadsheet-first workflows. Use one row per resource
item. The first row supplies resource-level metadata, and every row supplies one
item.

Supported columns:

- `title`
- `slug`
- `subject`
- `level`
- `resource_type`
- `education_system`
- `exam_board`
- `course`
- `summary`
- `skills`
- `learning_objectives`
- `curriculum_references`
- `type`
- `difficulty`
- `prompt`
- `answer`
- `explanation`

Separate multiple skills, objectives, or references with semicolons, for example:
`classification;materials;properties` or
`Classify everyday materials;Link properties to object uses` or
`Cambridge 0478 4.1;Cambridge 0478 4.2`.

## Scaffolding

Run:

```bash
exam-materials-studio scaffold \
  --title "Primary Fractions Starter" \
  --subject Mathematics \
  --level Primary \
  --resource-type worksheet \
  --education-system "General primary" \
  --course Fractions \
  --learning-objectives "Represent equivalent fractions with simple models" \
  --curriculum-references "Local Grade 4 Fractions" \
  --skills "fractions;equivalent fractions" \
  --out examples/primary_fractions_starter.json
```

To avoid repeating metadata for common education systems, list and apply built-in
presets:

```bash
exam-materials-studio presets --out generated/scaffold-presets.md

exam-materials-studio scaffold \
  --preset ib-dp \
  --title "IB Biology Cell Respiration Study Guide" \
  --subject Biology \
  --course "Biology HL" \
  --learning-objectives "Explain how ATP is produced during respiration" \
  --curriculum-references "IB Biology: cell respiration" \
  --skills "cell respiration;ATP" \
  --out examples/ib_biology_cell_respiration_study_guide.json
```

Presets currently cover preschool, primary, Cambridge IGCSE, Cambridge A Level,
AP, IB Diploma, and university materials. The scaffold still accepts explicit
metadata flags, and explicit flags override preset defaults when a course or
school needs a more specific level, board, system, or resource type.

The scaffold command writes a valid three-item starter resource with placeholder
prompts, answers, explanations, and starter difficulty progression labels. Use
`--format csv` for spreadsheet-first authoring. Existing files are protected by
default; pass `--force` only when you intentionally want to replace a scaffold.

## Outputs

By default the CLI writes:

- Learner resource as Markdown.
- Learner resource as HTML.
- Answer key as Markdown.
- Answer key as HTML.
- Static `index.md` catalog for GitHub and release-note review.
- Static `index.json` catalog for search, hosting, and integration workflows.
- Static `index.html` catalog.

The JSON catalog includes per-resource `difficulty_counts` so maintainers can
quickly see whether a resource leans too heavily toward foundation, core, or
extension work.

Use `--formats markdown` or `--formats html` to limit resource and answer-key
formats. The Markdown catalog is written when Markdown output is requested; the
JSON and HTML catalogs are always written so the output directory has both a
machine-readable manifest and a browser entrypoint.

## Validation

Run:

```bash
exam-materials-studio validate examples/*.json
```

CSV files can be validated with the same command:

```bash
exam-materials-studio validate examples/*.csv
```

The validator fails on structural errors, such as missing required fields or
invalid JSON. It also emits warnings for resources that are technically valid
but weak for publishing, including missing `education_system`, missing `course`,
missing `learning_objectives`, missing `curriculum_references`, exam-specific
resources without an `exam_board`, missing item difficulty labels, very short
resources, and thin or missing explanations.

Use `--report path/to/report.txt` to save a report for release checks or pull
request review.

## Inventory Reports

Run:

```bash
exam-materials-studio inventory examples/*.json examples/*.csv --out generated/inventory.md --csv generated/inventory.csv
```

The Markdown inventory is designed for maintainers reviewing subject and
curriculum coverage. It reports total resources, total items, and counts by:

- subject
- level
- resource type
- education system
- exam board
- course

The CSV inventory writes one row per resource so maintainers can sort and
filter coverage in a spreadsheet.
