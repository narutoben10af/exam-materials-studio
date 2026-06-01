from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScaffoldPreset:
    name: str
    description: str
    level: str
    resource_type: str
    education_system: str
    exam_board: str = ""


PRESETS: dict[str, ScaffoldPreset] = {
    "preschool": ScaffoldPreset(
        name="preschool",
        description="General early-years activities and teacher notes",
        level="Preschool",
        resource_type="activity-sheet",
        education_system="General early years",
    ),
    "primary": ScaffoldPreset(
        name="primary",
        description="General primary classroom worksheets and lesson resources",
        level="Primary",
        resource_type="worksheet",
        education_system="General primary",
    ),
    "cambridge-igcse": ScaffoldPreset(
        name="cambridge-igcse",
        description="Cambridge International IGCSE resources",
        level="IGCSE",
        resource_type="exam-practice",
        education_system="Cambridge International",
        exam_board="Cambridge",
    ),
    "cambridge-a-level": ScaffoldPreset(
        name="cambridge-a-level",
        description="Cambridge International AS and A Level resources",
        level="A Level",
        resource_type="exam-practice",
        education_system="Cambridge International",
        exam_board="Cambridge",
    ),
    "ap": ScaffoldPreset(
        name="ap",
        description="Advanced Placement course resources",
        level="AP",
        resource_type="exam-practice",
        education_system="Advanced Placement",
        exam_board="College Board",
    ),
    "ib-dp": ScaffoldPreset(
        name="ib-dp",
        description="International Baccalaureate Diploma Programme resources",
        level="IB",
        resource_type="study-guide",
        education_system="International Baccalaureate",
        exam_board="IB",
    ),
    "university": ScaffoldPreset(
        name="university",
        description="Higher-education study guides and seminar resources",
        level="University",
        resource_type="study-guide",
        education_system="Higher education",
    ),
}


class PresetError(ValueError):
    """Raised when an unknown scaffold preset is requested."""


def get_preset(name: str | None) -> ScaffoldPreset | None:
    if not name:
        return None
    try:
        return PRESETS[name]
    except KeyError as error:
        raise PresetError(f"unknown preset: {name}") from error


def render_presets_markdown() -> str:
    lines = [
        "# Scaffold Presets",
        "",
        "| Name | Level | Resource Type | Education System | Exam Board | Description |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for preset in PRESETS.values():
        lines.append(
            "| "
            + " | ".join(
                [
                    preset.name,
                    preset.level,
                    preset.resource_type,
                    preset.education_system,
                    preset.exam_board or "Unspecified",
                    preset.description,
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)
