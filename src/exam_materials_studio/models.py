from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PackItem:
    prompt: str
    answer: str
    explanation: str = ""
    item_type: str = "question"


@dataclass(frozen=True)
class ExamPack:
    title: str
    slug: str
    subject: str
    level: str
    summary: str
    skills: tuple[str, ...]
    items: tuple[PackItem, ...]
    resource_type: str = "exam-pack"
    education_system: str = ""
    exam_board: str = ""
    course: str = ""


class PackValidationError(ValueError):
    """Raised when a pack file is missing required content."""


def pack_from_dict(data: dict[str, Any]) -> ExamPack:
    required = ["title", "slug", "subject", "level", "summary", "skills", "items"]
    missing = [field for field in required if field not in data]
    if missing:
        raise PackValidationError(f"Missing required fields: {', '.join(missing)}")

    if not isinstance(data["skills"], list) or not data["skills"]:
        raise PackValidationError("skills must be a non-empty list")
    skills = tuple(str(skill).strip() for skill in data["skills"] if str(skill).strip())
    if not skills:
        raise PackValidationError("skills must include at least one non-empty skill")

    if not isinstance(data["items"], list) or not data["items"]:
        raise PackValidationError("items must be a non-empty list")

    items: list[PackItem] = []
    for index, raw_item in enumerate(data["items"], start=1):
        if not isinstance(raw_item, dict):
            raise PackValidationError(f"item {index} must be an object")
        prompt = _required_text(raw_item, "prompt", f"item {index}")
        answer = _required_text(raw_item, "answer", f"item {index}")
        explanation = str(raw_item.get("explanation", "")).strip()
        item_type = str(raw_item.get("type", "question")).strip() or "question"
        items.append(PackItem(prompt=prompt, answer=answer, explanation=explanation, item_type=item_type))

    return ExamPack(
        title=_required_text(data, "title", "pack"),
        slug=_required_slug(data),
        subject=_required_text(data, "subject", "pack"),
        level=_required_text(data, "level", "pack"),
        summary=_required_text(data, "summary", "pack"),
        skills=skills,
        items=tuple(items),
        resource_type=str(data.get("resource_type", "exam-pack")).strip() or "exam-pack",
        education_system=str(data.get("education_system", "")).strip(),
        exam_board=str(data.get("exam_board", "")).strip(),
        course=str(data.get("course", "")).strip(),
    )


def _required_text(data: dict[str, Any], field: str, label: str) -> str:
    value = str(data.get(field, "")).strip()
    if not value:
        raise PackValidationError(f"{label} missing required text field: {field}")
    return value


def _required_slug(data: dict[str, Any]) -> str:
    slug = _required_text(data, "slug", "pack")
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789-")
    if any(character not in allowed for character in slug):
        raise PackValidationError("slug may only contain lowercase letters, numbers, and hyphens")
    return slug
