from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class ScaffoldSpec:
    title: str
    slug: str
    subject: str
    level: str
    resource_type: str
    education_system: str
    exam_board: str
    course: str
    duration_minutes: int
    summary: str
    learning_objectives: tuple[str, ...]
    curriculum_references: tuple[str, ...]
    skills: tuple[str, ...]


class ScaffoldError(ValueError):
    """Raised when a scaffold file cannot be created."""


def default_slug(title: str) -> str:
    characters = []
    previous_dash = False
    for character in title.lower():
        if character.isalnum():
            characters.append(character)
            previous_dash = False
        elif not previous_dash:
            characters.append("-")
            previous_dash = True
    return "".join(characters).strip("-")


def scaffold_resource(spec: ScaffoldSpec, output_path: Path, output_format: str, force: bool = False) -> None:
    if output_format not in {"json", "yaml", "csv"}:
        raise ScaffoldError(f"unsupported scaffold format: {output_format}")
    if spec.duration_minutes < 1:
        raise ScaffoldError("duration_minutes must be a positive integer")
    if output_path.exists() and not force:
        raise ScaffoldError(f"refusing to overwrite existing file: {output_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_format == "json":
        output_path.write_text(json.dumps(_resource_dict(spec), indent=2) + "\n", encoding="utf-8")
    elif output_format == "yaml":
        output_path.write_text(
            yaml.safe_dump(_resource_dict(spec), sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
    else:
        _write_csv_scaffold(spec, output_path)


def _resource_dict(spec: ScaffoldSpec) -> dict[str, object]:
    return {
        "title": spec.title,
        "slug": spec.slug,
        "subject": spec.subject,
        "level": spec.level,
        "resource_type": spec.resource_type,
        "education_system": spec.education_system,
        "exam_board": spec.exam_board,
        "course": spec.course,
        "duration_minutes": spec.duration_minutes,
        "summary": spec.summary,
        "learning_objectives": list(spec.learning_objectives),
        "curriculum_references": list(spec.curriculum_references),
        "skills": list(spec.skills),
        "items": _starter_items(spec),
    }


def _starter_items(spec: ScaffoldSpec) -> list[dict[str, str]]:
    return [
        {
            "type": "concept-check",
            "difficulty": "foundation",
            "prompt": f"Introduce one key idea from {spec.course or spec.subject}.",
            "answer": "Replace with the expected answer or success criteria.",
            "explanation": "Explain why this answer is correct and how it supports the learning goal.",
        },
        {
            "type": "practice",
            "difficulty": "core",
            "prompt": "Add one learner-facing practice task.",
            "answer": "Replace with a complete worked answer.",
            "explanation": "Include the reasoning, method, or marking guidance a teacher needs.",
        },
        {
            "type": "reflection",
            "difficulty": "extension",
            "prompt": "Add one extension, discussion, or reflection prompt.",
            "answer": "Replace with a strong sample response or teacher note.",
            "explanation": "Explain what a high-quality response should demonstrate.",
        },
    ]


def _write_csv_scaffold(spec: ScaffoldSpec, output_path: Path) -> None:
    fieldnames = [
        "title",
        "slug",
        "subject",
        "level",
        "resource_type",
        "education_system",
        "exam_board",
        "course",
        "duration_minutes",
        "summary",
        "learning_objectives",
        "curriculum_references",
        "skills",
        "type",
        "difficulty",
        "prompt",
        "answer",
        "explanation",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for item in _starter_items(spec):
            writer.writerow(
                {
                    "title": spec.title,
                    "slug": spec.slug,
                    "subject": spec.subject,
                    "level": spec.level,
                    "resource_type": spec.resource_type,
                    "education_system": spec.education_system,
                    "exam_board": spec.exam_board,
                    "course": spec.course,
                    "duration_minutes": spec.duration_minutes,
                    "summary": spec.summary,
                    "learning_objectives": ";".join(spec.learning_objectives),
                    "curriculum_references": ";".join(spec.curriculum_references),
                    "skills": ";".join(spec.skills),
                    **item,
                }
            )
