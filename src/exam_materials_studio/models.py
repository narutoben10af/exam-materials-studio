from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PackItem:
    prompt: str
    answer: str
    explanation: str = ""
    item_type: str = "question"
    phase: str = ""
    difficulty: str = ""
    marks: int = 0
    command_word: str = ""
    rubric: tuple[str, ...] = ()


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
    duration_minutes: int | None = None
    prerequisites: tuple[str, ...] = ()
    materials: tuple[str, ...] = ()
    delivery_modes: tuple[str, ...] = ()
    learning_objectives: tuple[str, ...] = ()
    curriculum_references: tuple[str, ...] = ()


class PackValidationError(ValueError):
    """Raised when a pack file is missing required content."""


DIFFICULTY_ORDER = ("foundation", "core", "extension")
ALLOWED_DIFFICULTIES = set(DIFFICULTY_ORDER)


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
    learning_objectives = _optional_text_list(data.get("learning_objectives", []), "learning_objectives")
    curriculum_references = _optional_text_list(
        data.get("curriculum_references", []),
        "curriculum_references",
    )
    prerequisites = _optional_text_list(data.get("prerequisites", []), "prerequisites")
    materials = _optional_text_list(data.get("materials", []), "materials")
    delivery_modes = _optional_text_list(data.get("delivery_modes", []), "delivery_modes")

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
        phase = _optional_item_label(raw_item.get("phase", ""), "phase", index)
        difficulty = _optional_difficulty(raw_item.get("difficulty", ""), index)
        marks = _optional_item_marks(raw_item.get("marks", None), index)
        command_word = str(raw_item.get("command_word", "")).strip().lower()
        rubric = _optional_item_text_list(raw_item.get("rubric", []), "rubric", index)
        items.append(
            PackItem(
                prompt=prompt,
                answer=answer,
                explanation=explanation,
                item_type=item_type,
                phase=phase,
                difficulty=difficulty,
                marks=marks,
                command_word=command_word,
                rubric=rubric,
            )
        )

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
        duration_minutes=_optional_positive_int(data.get("duration_minutes", None), "duration_minutes"),
        prerequisites=prerequisites,
        materials=materials,
        delivery_modes=delivery_modes,
        learning_objectives=learning_objectives,
        curriculum_references=curriculum_references,
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


def _optional_text_list(value: Any, field: str) -> tuple[str, ...]:
    if value in (None, ""):
        return ()
    if not isinstance(value, list):
        raise PackValidationError(f"{field} must be a list when provided")
    return tuple(str(item).strip() for item in value if str(item).strip())


def _optional_item_text_list(value: Any, field: str, index: int) -> tuple[str, ...]:
    if value in (None, ""):
        return ()
    if not isinstance(value, list):
        raise PackValidationError(f"item {index} {field} must be a list when provided")
    return tuple(str(item).strip() for item in value if str(item).strip())


def _optional_item_label(value: Any, field: str, index: int) -> str:
    if value in (None, ""):
        return ""
    if not isinstance(value, str):
        raise PackValidationError(f"item {index} {field} must be text when provided")
    return "-".join(value.strip().lower().split())


def _optional_difficulty(value: Any, index: int) -> str:
    difficulty = str(value or "").strip().lower()
    if difficulty and difficulty not in ALLOWED_DIFFICULTIES:
        allowed = ", ".join(sorted(ALLOWED_DIFFICULTIES))
        raise PackValidationError(f"item {index} difficulty must be one of: {allowed}")
    return difficulty


def _optional_positive_int(value: Any, field: str) -> int | None:
    if value in (None, ""):
        return None
    try:
        duration = int(str(value).strip())
    except (TypeError, ValueError) as error:
        raise PackValidationError(f"{field} must be a positive integer") from error
    if duration < 1:
        raise PackValidationError(f"{field} must be a positive integer")
    return duration


def _optional_item_marks(value: Any, index: int) -> int:
    if value in (None, ""):
        return 0
    try:
        marks = int(str(value).strip())
    except (TypeError, ValueError) as error:
        raise PackValidationError(f"item {index} marks must be a positive integer") from error
    if marks < 1:
        raise PackValidationError(f"item {index} marks must be a positive integer")
    return marks
