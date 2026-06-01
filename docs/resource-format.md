# Resource Format

Exam Materials Studio uses a small JSON format so education resources can be
reviewed, versioned, regenerated, and published without a database.

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

These fields make the catalog useful when the repository grows across subjects,
education systems, age ranges, and course types.

## Item Fields

- `prompt`: The learner-facing or teacher-facing task.
- `answer`: The expected answer, marking note, or suggested response.
- `explanation`: Optional reasoning for answer keys.
- `type`: Optional item type such as `question`, `activity`, `teacher-note`, `calculation`, or `discussion`.

## Outputs

By default the CLI writes:

- Learner resource as Markdown.
- Learner resource as HTML.
- Answer key as Markdown.
- Answer key as HTML.
- Static `index.html` catalog.

Use `--formats markdown` or `--formats html` to limit output formats.

