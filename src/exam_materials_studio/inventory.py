from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from .models import ExamPack


@dataclass(frozen=True)
class Inventory:
    packs: tuple[ExamPack, ...]

    @property
    def resource_count(self) -> int:
        return len(self.packs)

    @property
    def item_count(self) -> int:
        return sum(len(pack.items) for pack in self.packs)


def build_inventory(packs: list[ExamPack]) -> Inventory:
    return Inventory(packs=tuple(packs))


def render_inventory_markdown(inventory: Inventory) -> str:
    lines = [
        "# Resource Coverage Inventory",
        "",
        f"- Resources: {inventory.resource_count}",
        f"- Items: {inventory.item_count}",
        "",
    ]

    for title, counter in [
        ("Subjects", _count_field(inventory.packs, "subject")),
        ("Levels", _count_field(inventory.packs, "level")),
        ("Resource Types", _count_field(inventory.packs, "resource_type")),
        ("Education Systems", _count_field(inventory.packs, "education_system")),
        ("Exam Boards", _count_field(inventory.packs, "exam_board")),
        ("Courses", _count_field(inventory.packs, "course")),
    ]:
        lines.extend(_render_counter_section(title, counter))

    lines.extend(["## Resources", "", "| Title | Level | Subject | Type | Course | Items |", "| --- | --- | --- | --- | --- | --- |"])
    for pack in sorted(inventory.packs, key=lambda item: (item.level, item.subject, item.title)):
        lines.append(
            "| "
            + " | ".join(
                [
                    _table_cell(pack.title),
                    _table_cell(pack.level),
                    _table_cell(pack.subject),
                    _table_cell(pack.resource_type),
                    _table_cell(pack.course or "Unspecified"),
                    str(len(pack.items)),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def write_inventory_csv(inventory: Inventory, path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "title",
                "slug",
                "subject",
                "level",
                "resource_type",
                "education_system",
                "exam_board",
                "course",
                "item_count",
            ],
        )
        writer.writeheader()
        for pack in inventory.packs:
            writer.writerow(
                {
                    "title": pack.title,
                    "slug": pack.slug,
                    "subject": pack.subject,
                    "level": pack.level,
                    "resource_type": pack.resource_type,
                    "education_system": pack.education_system,
                    "exam_board": pack.exam_board,
                    "course": pack.course,
                    "item_count": len(pack.items),
                }
            )


def _count_field(packs: tuple[ExamPack, ...], field_name: str) -> Counter[str]:
    values = []
    for pack in packs:
        value = str(getattr(pack, field_name)).strip() or "Unspecified"
        values.append(value)
    return Counter(values)


def _render_counter_section(title: str, counter: Counter[str]) -> list[str]:
    lines = [f"## {title}", "", "| Value | Resources |", "| --- | --- |"]
    for value, count in sorted(counter.items(), key=lambda item: (-item[1], item[0].lower())):
        lines.append(f"| {_table_cell(value)} | {count} |")
    lines.append("")
    return lines


def _table_cell(value: str) -> str:
    return str(value).replace("|", "\\|")

