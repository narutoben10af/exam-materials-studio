from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .loader import ResourceLoadError, load_resource
from .models import ExamPack


@dataclass(frozen=True)
class ValidationMessage:
    path: Path
    level: str
    message: str


@dataclass(frozen=True)
class ValidationResult:
    path: Path
    pack: ExamPack | None
    errors: tuple[ValidationMessage, ...]
    warnings: tuple[ValidationMessage, ...]

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_resource(path: Path) -> ValidationResult:
    try:
        pack = load_resource(path)
    except ResourceLoadError as error:
        return ValidationResult(
            path=path,
            pack=None,
            errors=(ValidationMessage(path, "error", str(error)),),
            warnings=(),
        )

    warnings = tuple(_quality_warnings(path, pack))
    return ValidationResult(path=path, pack=pack, errors=(), warnings=warnings)


def validate_resources(paths: list[Path]) -> list[ValidationResult]:
    return [validate_resource(path) for path in paths]


def render_validation_report(results: list[ValidationResult]) -> str:
    lines = ["Resource validation report", ""]
    total_errors = sum(len(result.errors) for result in results)
    total_warnings = sum(len(result.warnings) for result in results)
    lines.append(f"Checked: {len(results)}")
    lines.append(f"Errors: {total_errors}")
    lines.append(f"Warnings: {total_warnings}")
    lines.append("")

    for result in results:
        status = "PASS" if result.ok else "FAIL"
        title = result.pack.title if result.pack else result.path.name
        lines.append(f"{status} {result.path}: {title}")
        for message in [*result.errors, *result.warnings]:
            lines.append(f"  {message.level}: {message.message}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def has_errors(results: list[ValidationResult]) -> bool:
    return any(not result.ok for result in results)


def _quality_warnings(path: Path, pack: ExamPack) -> list[ValidationMessage]:
    warnings: list[ValidationMessage] = []

    if pack.resource_type == "exam-pack":
        warnings.append(
            ValidationMessage(
                path,
                "warning",
                "resource_type is using the generic default; set a specific type for catalog clarity",
            )
        )

    if not pack.education_system:
        warnings.append(ValidationMessage(path, "warning", "education_system is missing"))

    if pack.level.lower() in {"igcse", "a level", "gcse", "ap", "ib"} and not pack.exam_board:
        warnings.append(
            ValidationMessage(path, "warning", "exam_board is recommended for exam-specific resources")
        )

    if not pack.course:
        warnings.append(ValidationMessage(path, "warning", "course is missing"))

    if not pack.learning_objectives:
        warnings.append(ValidationMessage(path, "warning", "learning_objectives is missing"))

    if not pack.curriculum_references:
        warnings.append(ValidationMessage(path, "warning", "curriculum_references is missing"))

    if len(pack.items) < 3:
        warnings.append(
            ValidationMessage(path, "warning", "resource has fewer than 3 items; consider adding depth")
        )

    missing_explanations = [
        index for index, item in enumerate(pack.items, start=1) if len(item.explanation.split()) < 4
    ]
    if missing_explanations:
        joined = ", ".join(str(index) for index in missing_explanations)
        warnings.append(
            ValidationMessage(path, "warning", f"thin or missing explanations for item(s): {joined}")
        )

    return warnings
