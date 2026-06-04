# Resource Format

Exam Materials Studio uses small JSON, YAML, and CSV formats so education
resources can be reviewed, versioned, regenerated, and published without a
database.

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
- `unit`: Lesson, module, topic, course-pack section, or study-guide unit.
- `sequence_order`: Positive integer for placing the resource inside a unit,
  module, course pack, tutoring pathway, or study-guide progression.
- `duration_minutes`: Estimated learner or classroom time as a positive integer.
- `prerequisites`: Prior knowledge, skills, or lessons expected before starting the resource.
- `materials`: Supplies, devices, files, or tools needed to run the resource.
- `delivery_modes`: Intended teaching or learning settings, such as `classroom`,
  `tutoring`, `self-study`, `homework`, `revision`, `seminar`, or `discussion`.
- `learning_objectives`: Teacher-facing objectives describing what learners should be able to do.
- `curriculum_references`: Syllabus sections, standards, specification points, or module outcomes.

These fields make the catalog useful when the repository grows across subjects,
education systems, age ranges, course types, and ordered learning pathways.

## Item Fields

- `prompt`: The learner-facing or teacher-facing task.
- `answer`: The expected answer, marking note, or suggested response.
- `explanation`: Optional reasoning for answer keys.
- `type`: Optional item type such as `question`, `activity`, `teacher-note`, `calculation`, or `discussion`.
- `phase`: Optional lesson-flow label such as `warm-up`, `instruction`,
  `guided-practice`, `independent-practice`, `application`, `assessment`,
  `extension`, `reflection`, or `discussion`. Spaces are normalised to hyphens.
- `time_minutes`: Optional positive integer for pacing an individual item,
  activity, question, or teacher note.
- `standards`: Optional list of syllabus points, curriculum standards,
  specification objectives, local scheme references, or course outcomes covered
  by the individual item.
- `difficulty`: Optional progression label. Supported values are `foundation`,
  `core`, and `extension`.
- `marks`: Optional positive integer for assessment weighting, scoring, or
  rubric planning.
- `command_word`: Optional assessment-intent label such as `define`, `explain`,
  `calculate`, `discuss`, `compare`, `identify`, or `evaluate`.
- `rubric`: Optional list of teacher-facing marking or success-criteria bullets.
  Rubric points render in answer keys and roll up in catalogs and inventory
  reports, but they are intentionally not shown in learner-facing resources.

## YAML Input

YAML resources use the same fields as JSON. They are useful for hand-edited
resources because lists of objectives, references, skills, and items stay
readable without spreadsheet quoting.

Supported file extensions are `.yaml` and `.yml`.

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
- `unit`
- `sequence_order`
- `duration_minutes`
- `prerequisites`
- `materials`
- `delivery_modes`
- `summary`
- `skills`
- `learning_objectives`
- `curriculum_references`
- `type`
- `phase`
- `time_minutes`
- `standards`
- `difficulty`
- `marks`
- `command_word`
- `rubric`
- `prompt`
- `answer`
- `explanation`

Separate multiple skills, prerequisites, materials, delivery modes, objectives,
references, item standards, or rubric points with semicolons, for example:
`classification;materials;properties` or
`Name common classroom objects;Describe simple object uses` or
`Wood sample;Metal spoon;Plastic bottle` or
`classroom;tutoring;self-study` or
`Classify everyday materials;Link properties to object uses` or
`Cambridge 0478 4.1;Cambridge 0478 4.2` or
`Primary science: everyday materials;Primary science: material properties` or
`1 mark for the method;1 mark for the final answer`.

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
  --unit "Equivalent fractions" \
  --sequence-order 1 \
  --duration-minutes 30 \
  --prerequisites "Count equal parts in a shape" \
  --materials "Fraction strips;Counters" \
  --delivery-modes "classroom;tutoring" \
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
  --unit "Cell respiration" \
  --sequence-order 2 \
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
prompts, answers, explanations, prerequisites, materials, estimated duration,
delivery modes, unit and sequence metadata, starter difficulty progression
labels, 1/2/3 mark weights, and starter command words, lesson-flow phases, and
rubric bullets.
Starter items also include item-level pacing with `time_minutes` and standards
mapping from the scaffold curriculum references.
Use `--format yaml` for hand-edited resources or `--format csv` for
spreadsheet-first authoring. Existing files are protected by default; pass
`--force` only when you intentionally want to replace a scaffold.

## Outputs

By default the CLI writes:

- Learner resource as Markdown.
- Learner resource as HTML.
- Answer key as Markdown.
- Answer key as HTML.
- Static `index.md` catalog for GitHub and release-note review.
- Static `index.json` catalog for search, hosting, and integration workflows.
- Static `index.html` catalog.

The JSON catalog includes per-resource `unit`, `sequence_order`,
`duration_minutes`, `prerequisites`, `materials`, `delivery_modes`, `total_marks`, `command_word_counts`,
`phase_counts`, `standard_counts`, `item_time_minutes`, `rubric_point_count`, and
`difficulty_counts` so maintainers can quickly see entry requirements,
preparation needs, course-pack placement, delivery settings, planned time, item
pacing, assessment weight, lesson-flow coverage, standards coverage,
marking-criteria depth, assessment intent, and whether a resource leans too
heavily toward foundation, core, or extension work.

Use `--formats markdown` or `--formats html` to limit resource and answer-key
formats. The Markdown catalog is written when Markdown output is requested; the
JSON and HTML catalogs are always written so the output directory has both a
machine-readable manifest and a browser entrypoint.

## Validation

Run:

```bash
exam-materials-studio validate examples/*.json examples/*.yaml
```

CSV files can be validated with the same command:

```bash
exam-materials-studio validate examples/*.csv
```

The validator fails on structural errors, such as missing required fields,
invalid JSON, invalid YAML, or malformed CSV rows. It also emits warnings for
resources that are technically valid but weak for publishing, including missing
`education_system`, missing `course`, missing `learning_objectives`, missing
`curriculum_references`, exam-specific resources without an `exam_board`,
missing item difficulty labels, very short resources, and thin or missing
explanations. Missing `duration_minutes` is also reported as a
planning-quality warning.

Use `--report path/to/report.txt` to save a report for release checks or pull
request review.

## Inventory Reports

Run:

```bash
exam-materials-studio inventory examples/*.json examples/*.yaml examples/*.csv --out generated/inventory.md --csv generated/inventory.csv
```

The Markdown inventory is designed for maintainers reviewing subject and
curriculum coverage. It reports total resources, total items, and counts by:

- subject
- level
- resource type
- education system
- exam board
- course
- unit
- delivery mode
- command word
- learning phase
- item standards
- total planned duration
- item-level planned time
- total marks
- rubric points
- difficulty coverage

The CSV inventory writes one row per resource so maintainers can sort and
filter coverage in a spreadsheet. It includes `unit`, `sequence_order`,
`delivery_modes`, `command_words`, `phases`, `standards`, `duration_minutes`,
`item_time_minutes`, `total_marks`, `foundation_items`, `core_items`,
`extension_items`, `rubric_points`, and `unspecified_difficulty_items` columns
so reviewers can spot resources that need more sequence coverage, delivery
coverage, pacing detail, lesson-flow coverage, standards mapping, assessment
intent coverage, marking support, assessment balance, or progression balance.
