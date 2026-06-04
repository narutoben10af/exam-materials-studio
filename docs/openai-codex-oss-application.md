# OpenAI Codex for Open Source Application Notes

These notes are for the maintainer when filling the OpenAI Codex for Open
Source form. They should be updated as the project gains users, contributors,
stars, issues, releases, and downstream usage.

## Repository

https://github.com/narutoben10af/exam-materials-studio

## Role

Primary maintainer.

## Why The Repository Qualifies

Exam Materials Studio is an open-source toolkit for teachers and tutoring
centres to generate printable education resources, answer keys, and static
catalogs from structured syllabus data. It now supports metadata for education
systems, exam boards, courses, and resource types, which makes it suitable for a
path beyond exam packs into lesson materials, activity sheets, worksheets, and
study guides across preschool through university workflows. The repository also
includes a validation command that maintainers can use to triage resource
quality before publishing. It also supports hand-editable YAML and
spreadsheet-friendly CSV input, so teachers can draft resources in familiar
tools before generating Markdown, HTML, answer keys, and catalogs. The
inventory command gives maintainers a way to
track coverage across subjects, education systems, exam boards, courses, levels,
resource types, and item difficulty progression as the project grows. A scaffold
command helps contributors
start new JSON, YAML, or CSV resources with the required metadata and starter items,
and built-in scaffold presets now make common preschool, primary, Cambridge
IGCSE, Cambridge A Level, AP, IB Diploma, and university resources easier to
start consistently. The format also supports learning objectives so resources
can describe teacher-facing outcomes, not just question skills, which helps the
project expand beyond exam packs into broader education materials.
Curriculum reference metadata lets packs cite syllabus sections, standards, or
module outcomes, which is important as the project grows across exam boards,
school systems, and university courses.
The build output also includes a machine-readable JSON catalog so generated
resources can be indexed or integrated into static sites and future education
tools without scraping Markdown or HTML.
Item-level difficulty metadata now lets maintainers balance foundation, core,
and extension work inside each resource, while inventory reports expose that
balance across the repository. This supports deeper learning progressions
beyond simple exam-question generation.
Estimated duration metadata now helps the project support broader education
materials too: lesson activities, tutoring sessions, revision blocks, and study
guides can show expected time and roll up total planned minutes in inventory
reports.
Prerequisite metadata helps resources become sequenced education materials
rather than isolated packs, since teachers can show expected prior knowledge for
lesson pathways, tutoring courses, revision plans, and university study guides.
Materials metadata adds practical classroom preparation support, so activity
sheets, lessons, labs, tutoring sessions, and study guides can state the
supplies, devices, files, or tools needed before delivery.
Delivery-mode metadata is another step beyond exam materials into deeper
education-material workflows. Resources can now identify whether they are meant
for classrooms, tutoring, self-study, homework, revision, seminars, or
discussion, which helps the repository grow into a broader platform for lesson
materials, worksheets, study guides, activities, and course resources rather
than only exam-pack generation.
Item-level marks metadata adds assessment planning support across exam papers,
worksheets, quizzes, problem sets, and study checks. Generated resources and
answer keys can show item weights, while catalogs and inventory reports roll up
total marks so maintainers can review scoring balance across levels and formats.
Item-level command-word metadata adds exam-board and assessment-intent support:
resources can show whether an item asks learners to define, explain, calculate,
discuss, compare, identify, or evaluate. Inventory and catalog outputs can then
surface command-word coverage across subjects, levels, and formats.
Item-level rubric metadata adds teacher-facing marking criteria and success
criteria to answer keys while keeping learner-facing resources clean. Catalog
and inventory outputs roll up rubric point counts, which helps maintainers see
whether a resource has enough marking depth for exams, worksheets, activities,
study guides, and course materials across preschool through university levels.
Item-level phase metadata adds lesson-flow structure beyond assessment fields:
resources can label warm-up, instruction, guided-practice, application,
assessment, reflection, discussion, and seminar steps. Catalog and inventory
outputs surface phase coverage, which helps maintainers review whether resources
work as complete lessons, tutoring sessions, activity sheets, study guides, and
course materials rather than just isolated questions.
Item-level time metadata adds practical pacing for each step of a resource.
Learner outputs and answer keys can show how long a warm-up, guided-practice
task, assessment item, or reflection should take, while catalogs and inventory
reports roll up item-level planned minutes for maintainer review.
Item-level standards metadata adds curriculum mapping at the activity/question
level: resources can connect individual prompts to syllabus points, local
standards, specification objectives, or university module outcomes. Catalog and
inventory outputs surface standards coverage, which helps maintainers review
whether a resource is useful for broader lesson planning and course coverage,
not just exam-style generation.

## API Credits Use

Use API credits to add optional maintainer automation: generate draft question
sets from user-provided syllabus outlines, review packs for missing answers or
weak explanations, suggest accessibility improvements, and automate release
notes for new education-material templates.

## Current Caveat

This is a new repository. The strongest application should mention concrete
adoption signals once they exist, such as stars, external users, issues,
downloads, forks, or school/tutor usage.
