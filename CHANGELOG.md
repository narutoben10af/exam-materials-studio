# Changelog

## Unreleased

- Added resource-level `unit` and `sequence_order` metadata so resources can be
  organized into lesson sequences, course packs, tutoring pathways, modules, and
  study-guide progressions.
- Added unit and sequence output to rendered resources, answer keys, JSON
  catalogs, Markdown inventory summaries, CSV inventory exports, scaffolds, and
  bundled examples.

## v0.8.0

- Added item-level `standards` metadata for mapping individual activities,
  questions, prompts, and teacher notes to syllabus points, curriculum
  standards, or course outcomes.
- Added standards output to rendered resources, answer keys, JSON catalogs,
  Markdown inventory summaries, CSV inventory exports, scaffolds, and bundled examples.
- Added item-level `time_minutes` metadata for pacing individual lesson,
  tutoring, activity, worksheet, study-guide, and assessment steps.
- Added item-time output to rendered resources, answer keys, JSON catalogs,
  Markdown inventory summaries, CSV inventory exports, scaffolds, and bundled examples.

## v0.7.0

- Added item-level `phase` metadata for lesson-flow labels such as warm-up,
  guided practice, application, assessment, reflection, and discussion.
- Added phase output to rendered resources, answer keys, JSON catalogs, Markdown
  inventory summaries, CSV inventory exports, scaffolds, and bundled examples.

## v0.6.0

- Added item-level `rubric` metadata for teacher-facing marking criteria and success criteria.
- Added rubric output to answer keys while keeping learner-facing resources free of rubric content.
- Added rubric point totals to JSON catalogs, Markdown inventory summaries, and CSV inventory exports.
- Added default scaffold rubric bullets and rubric examples for JSON, YAML, and CSV resources.

## v0.5.0

- Added item-level `command_word` metadata for assessment intent such as define, explain, calculate, discuss, compare, identify, and evaluate.
- Added command-word output to rendered resources, answer keys, JSON catalogs, inventory summaries, and CSV inventory exports.
- Added default scaffold command words and command-word examples for JSON, YAML, and CSV resources.
- Added item-level `marks` metadata for assessment weighting across exams, worksheets, quizzes, problem sets, and study checks.
- Added marks output to rendered resources, answer keys, JSON catalogs, inventory summaries, and CSV inventory exports.
- Added default scaffold marks and marks examples for JSON, YAML, and CSV resources.

## v0.4.0

- Added `delivery_modes` metadata for classroom, tutoring, self-study, homework, revision, seminar, and discussion workflows.
- Added delivery-mode output to rendered resources, answer keys, Markdown/HTML catalogs, JSON catalogs, and inventory reports.
- Added `--delivery-modes` scaffold support and delivery-mode examples for JSON, YAML, and CSV resources.
- Added `duration_minutes` metadata for lesson, tutoring, and study-planning estimates.
- Added duration output to rendered resources, answer keys, JSON catalogs, and inventory reports.
- Added `--duration-minutes` scaffold support and duration examples for JSON, YAML, and CSV resources.
- Added validation warnings for resources missing estimated duration metadata.
- Added `prerequisites` metadata for sequencing resources into lessons, courses, and revision pathways.
- Added prerequisite output to rendered resources, answer keys, Markdown/HTML catalogs, and JSON catalogs.
- Added `--prerequisites` scaffold support and prerequisite examples for JSON, YAML, and CSV resources.
- Added `materials` metadata for classroom supplies, devices, files, and preparation needs.
- Added materials output to rendered resources, answer keys, Markdown/HTML catalogs, and JSON catalogs.
- Added `--materials` scaffold support and materials examples for JSON, YAML, and CSV resources.

## v0.3.0

- Added item difficulty metadata with foundation, core, and extension progression labels.
- Added difficulty counts to JSON catalogs and inventory reports for maintainer coverage review.
- Added YAML resource input support with a secondary History source-analysis example.
- Added YAML scaffold output so contributors can start hand-editable resources from presets.
- Declared the PyYAML runtime dependency and added tests for YAML loading, building, and scaffolding.
- Added release metadata consistency tests so package version metadata, module version, and changelog stay aligned.

## v0.2.0

- Added JSON and CSV resource loading for broader education-material workflows.
- Added validation reports for maintainer review before publishing resources.
- Added coverage inventory reports across subjects, levels, resource types, education systems, exam boards, and courses.
- Added scaffold presets for preschool, primary, Cambridge IGCSE, Cambridge A Level, AP, IB Diploma, and university resources.
- Added Markdown catalog output for GitHub and release-note review.
- Added learning objectives metadata for teacher-facing outcomes in resources, scaffolds, validation, and rendered learner materials.

## v0.1.0

- Initial open-source release with structured resource packs, printable Markdown and HTML output, answer keys, and static HTML catalogs.
