from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from .models import ExamPack, PackValidationError, pack_from_dict


class ResourceLoadError(ValueError):
    """Raised when a resource file cannot be loaded."""


def load_resource(path: Path) -> ExamPack:
    suffix = path.suffix.lower()
    try:
        if suffix == ".json":
            data = json.loads(path.read_text(encoding="utf-8"))
        elif suffix == ".csv":
            data = _resource_dict_from_csv(path)
        else:
            raise ResourceLoadError(f"unsupported resource format: {suffix or 'no extension'}")
        return pack_from_dict(data)
    except json.JSONDecodeError as error:
        raise ResourceLoadError(str(error)) from error
    except OSError as error:
        raise ResourceLoadError(str(error)) from error
    except PackValidationError as error:
        raise ResourceLoadError(str(error)) from error


def _resource_dict_from_csv(path: Path) -> dict[str, Any]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        raise ResourceLoadError("CSV file has no resource rows")

    first = rows[0]
    required_resource_fields = ["title", "slug", "subject", "level", "summary", "skills"]
    missing = [field for field in required_resource_fields if not _cell(first, field)]
    if missing:
        raise ResourceLoadError(f"CSV first row missing required resource fields: {', '.join(missing)}")

    items = []
    for index, row in enumerate(rows, start=1):
        prompt = _cell(row, "prompt")
        answer = _cell(row, "answer")
        if not prompt or not answer:
            raise ResourceLoadError(f"CSV row {index} must include prompt and answer")
        item: dict[str, str] = {
            "prompt": prompt,
            "answer": answer,
            "explanation": _cell(row, "explanation"),
        }
        item_type = _cell(row, "type")
        if item_type:
            item["type"] = item_type
        items.append(item)

    return {
        "title": _cell(first, "title"),
        "slug": _cell(first, "slug"),
        "subject": _cell(first, "subject"),
        "level": _cell(first, "level"),
        "resource_type": _cell(first, "resource_type") or "exam-pack",
        "education_system": _cell(first, "education_system"),
        "exam_board": _cell(first, "exam_board"),
        "course": _cell(first, "course"),
        "summary": _cell(first, "summary"),
        "skills": _split_skills(_cell(first, "skills")),
        "learning_objectives": _split_skills(_cell(first, "learning_objectives")),
        "curriculum_references": _split_skills(_cell(first, "curriculum_references")),
        "items": items,
    }


def _cell(row: dict[str, str | None], field: str) -> str:
    return str(row.get(field) or "").strip()


def _split_skills(raw_skills: str) -> list[str]:
    return [skill.strip() for skill in raw_skills.split(";") if skill.strip()]
