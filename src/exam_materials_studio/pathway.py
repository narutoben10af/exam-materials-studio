from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from .models import ExamPack


def render_pathway_markdown(packs: list[ExamPack]) -> str:
    ordered_packs = _ordered_packs(packs)
    sequenced_count = sum(1 for pack in ordered_packs if pack.sequence_order is not None)
    total_duration = sum(pack.duration_minutes or 0 for pack in ordered_packs)
    lines = [
        "# Learning Pathway",
        "",
        f"- Resources: {len(ordered_packs)}",
        f"- Sequenced resources: {sequenced_count}",
        f"- Unsequenced resources: {len(ordered_packs) - sequenced_count}",
        f"- Planned time: {total_duration} minutes",
        "",
    ]

    for group_key, group_packs in _group_packs(ordered_packs).items():
        level, subject, course = group_key
        lines.extend([f"## {_cell(level)} / {_cell(subject)} / {_cell(course)}", ""])
        for unit, unit_packs in _group_units(group_packs).items():
            lines.extend([f"### Unit: {_cell(unit)}", ""])
            lines.extend(
                [
                    "| Seq | Resource | Type | Duration | Delivery | Prerequisites | Learning Objectives | Outputs |",
                    "| --- | --- | --- | --- | --- | --- | --- | --- |",
                ]
            )
            for pack in unit_packs:
                lines.append(_pathway_row(pack))
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_pathway_csv(packs: list[ExamPack], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "level",
        "subject",
        "course",
        "unit",
        "sequence_order",
        "title",
        "slug",
        "resource_type",
        "duration_minutes",
        "delivery_modes",
        "prerequisites",
        "learning_objectives",
        "resource_file",
        "answer_key_file",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for pack in _ordered_packs(packs):
            writer.writerow(
                {
                    "level": pack.level,
                    "subject": pack.subject,
                    "course": pack.course,
                    "unit": pack.unit,
                    "sequence_order": str(pack.sequence_order) if pack.sequence_order is not None else "Unsequenced",
                    "title": pack.title,
                    "slug": pack.slug,
                    "resource_type": pack.resource_type,
                    "duration_minutes": str(pack.duration_minutes or ""),
                    "delivery_modes": ";".join(pack.delivery_modes),
                    "prerequisites": ";".join(pack.prerequisites),
                    "learning_objectives": ";".join(pack.learning_objectives),
                    "resource_file": f"{pack.slug}.md",
                    "answer_key_file": f"{pack.slug}-answer-key.md",
                }
            )


def _ordered_packs(packs: list[ExamPack]) -> list[ExamPack]:
    return sorted(
        packs,
        key=lambda pack: (
            pack.level,
            pack.subject,
            pack.course or "Unspecified course",
            pack.unit or "Unspecified unit",
            pack.sequence_order is None,
            pack.sequence_order or 0,
            pack.title,
        ),
    )


def _group_packs(packs: list[ExamPack]) -> dict[tuple[str, str, str], list[ExamPack]]:
    groups: dict[tuple[str, str, str], list[ExamPack]] = defaultdict(list)
    for pack in packs:
        groups[(pack.level, pack.subject, pack.course or "Unspecified course")].append(pack)
    return dict(groups)


def _group_units(packs: list[ExamPack]) -> dict[str, list[ExamPack]]:
    groups: dict[str, list[ExamPack]] = defaultdict(list)
    for pack in packs:
        groups[pack.unit or "Unspecified unit"].append(pack)
    return dict(groups)


def _pathway_row(pack: ExamPack) -> str:
    sequence = str(pack.sequence_order) if pack.sequence_order is not None else "Unsequenced"
    duration = f"{pack.duration_minutes} min" if pack.duration_minutes else "Unspecified"
    delivery = ";".join(pack.delivery_modes) or "Unspecified"
    prerequisites = ";".join(pack.prerequisites) or "Unspecified"
    objectives = ";".join(pack.learning_objectives) or "Unspecified"
    return (
        f"| {_cell(sequence)} | [{_cell(pack.title)}]({pack.slug}.md) | {_cell(pack.resource_type)} | "
        f"{_cell(duration)} | {_cell(delivery)} | {_cell(prerequisites)} | {_cell(objectives)} | "
        f"[Answer key]({pack.slug}-answer-key.md) |"
    )


def _cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()
