from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PackItem:
    prompt: str
    answer: str
    explanation: str = ""


@dataclass(frozen=True)
class ExamPack:
    title: str
    slug: str
    subject: str
    level: str
    summary: str
    skills: tuple[str, ...]
    items: tuple[PackItem, ...]


class PackValidationError(ValueError):
    """Raised when a pack file is missing required content."""


def pack_from_dict(data: dict[str, Any]) -> ExamPack:
    required = ["title", "slug", "subject", "level", "summary", "skills", "items"]
    missing = [field for field in required if field not in data]
    if missing:
        raise PackValidationError(f"Missing required fields: {', '.join(missing)}")

    if not isinstance(data["skills"], list) or not data["skills"]:
        raise PackValidationError("skills must be a non-empty list")

    if not isinstance(data["items"], list) or not data["items"]:
        raise PackValidationError("items must be a non-empty list")

    items: list[PackItem] = []
    for index, raw_item in enumerate(data["items"], start=1):
        if not isinstance(raw_item, dict):
            raise PackValidationError(f"item {index} must be an object")
        prompt = _required_text(raw_item, "prompt", f"item {index}")
        answer = _required_text(raw_item, "answer", f"item {index}")
        explanation = str(raw_item.get("explanation", "")).strip()
        items.append(PackItem(prompt=prompt, answer=answer, explanation=explanation))

    return ExamPack(
        title=_required_text(data, "title", "pack"),
        slug=_required_slug(data),
        subject=_required_text(data, "subject", "pack"),
        level=_required_text(data, "level", "pack"),
        summary=_required_text(data, "summary", "pack"),
        skills=tuple(str(skill).strip() for skill in data["skills"] if str(skill).strip()),
        items=tuple(items),
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

