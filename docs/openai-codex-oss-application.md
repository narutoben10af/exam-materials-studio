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
start new JSON or CSV resources with the required metadata and starter items,
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

## API Credits Use

Use API credits to add optional maintainer automation: generate draft question
sets from user-provided syllabus outlines, review packs for missing answers or
weak explanations, suggest accessibility improvements, and automate release
notes for new education-material templates.

## Current Caveat

This is a new repository. The strongest application should mention concrete
adoption signals once they exist, such as stars, external users, issues,
downloads, forks, or school/tutor usage.
