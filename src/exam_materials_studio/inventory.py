from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from .models import DIFFICULTY_ORDER, ExamPack


UNSPECIFIED_DIFFICULTY = "unspecified"
DIFFICULTY_LABELS = (*DIFFICULTY_ORDER, UNSPECIFIED_DIFFICULTY)


@dataclass(frozen=True)
class Inventory:
    packs: tuple[ExamPack, ...]

    @property
    def resource_count(self) -> int:
        return len(self.packs)

    @property
    def item_count(self) -> int:
        return sum(len(pack.items) for pack in self.packs)

    @property
    def total_duration_minutes(self) -> int:
        return sum(pack.duration_minutes or 0 for pack in self.packs)

    @property
    def total_item_time_minutes(self) -> int:
        return sum(_item_time_minutes(pack) for pack in self.packs)

    @property
    def total_marks(self) -> int:
        return sum(_total_marks(pack) for pack in self.packs)

    @property
    def total_rubric_points(self) -> int:
        return sum(_rubric_point_count(pack) for pack in self.packs)


def build_inventory(packs: list[ExamPack]) -> Inventory:
    return Inventory(packs=tuple(packs))


def render_inventory_markdown(inventory: Inventory) -> str:
    lines = [
        "# Resource Coverage Inventory",
        "",
        f"- Resources: {inventory.resource_count}",
        f"- Items: {inventory.item_count}",
        f"- Planned time: {inventory.total_duration_minutes} minutes",
        f"- Item planned time: {inventory.total_item_time_minutes} minutes",
        f"- Total marks: {inventory.total_marks}",
        f"- Rubric points: {inventory.total_rubric_points}",
        "",
    ]

    for title, counter in [
        ("Subjects", _count_field(inventory.packs, "subject")),
        ("Levels", _count_field(inventory.packs, "level")),
        ("Resource Types", _count_field(inventory.packs, "resource_type")),
        ("Education Systems", _count_field(inventory.packs, "education_system")),
        ("Exam Boards", _count_field(inventory.packs, "exam_board")),
        ("Courses", _count_field(inventory.packs, "course")),
        ("Delivery Modes", _count_list_field(inventory.packs, "delivery_modes")),
        ("Command Words", _count_command_words(inventory.packs)),
        ("Learning Phases", _count_phases(inventory.packs)),
    ]:
        lines.extend(_render_counter_section(title, counter))

    lines.extend(_render_item_counter_section("Standards", _count_standards(inventory.packs)))
    lines.extend(_render_difficulty_section(_count_difficulties(inventory.packs)))

    lines.extend(
        [
            "## Resources",
            "",
            "| Title | Level | Subject | Type | Course | Duration | Item Time | Marks | Rubric Points | Phases | Standards | Items | Foundation | Core | Extension | Unspecified Difficulty |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for pack in sorted(inventory.packs, key=lambda item: (item.level, item.subject, item.title)):
        difficulty_counts = _difficulty_counts_for_pack(pack)
        lines.append(
            "| "
            + " | ".join(
                [
                    _table_cell(pack.title),
                    _table_cell(pack.level),
                    _table_cell(pack.subject),
                    _table_cell(pack.resource_type),
                    _table_cell(pack.course or "Unspecified"),
                    _table_cell(_duration_label(pack)),
                    str(_item_time_minutes(pack)),
                    str(_total_marks(pack)),
                    str(_rubric_point_count(pack)),
                    _table_cell(";".join(_phases_for_pack(pack)) or "Unspecified"),
                    _table_cell(";".join(_standards_for_pack(pack)) or "Unspecified"),
                    str(len(pack.items)),
                    str(difficulty_counts["foundation"]),
                    str(difficulty_counts["core"]),
                    str(difficulty_counts["extension"]),
                    str(difficulty_counts[UNSPECIFIED_DIFFICULTY]),
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
                "duration_minutes",
                "item_time_minutes",
                "total_marks",
                "rubric_points",
                "phases",
                "standards",
                "command_words",
                "delivery_modes",
                "item_count",
                "foundation_items",
                "core_items",
                "extension_items",
                "unspecified_difficulty_items",
            ],
        )
        writer.writeheader()
        for pack in inventory.packs:
            difficulty_counts = _difficulty_counts_for_pack(pack)
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
                    "duration_minutes": pack.duration_minutes or "",
                    "item_time_minutes": _item_time_minutes(pack),
                    "total_marks": _total_marks(pack),
                    "rubric_points": _rubric_point_count(pack),
                    "phases": ";".join(_phases_for_pack(pack)),
                    "standards": ";".join(_standards_for_pack(pack)),
                    "command_words": ";".join(_command_words_for_pack(pack)),
                    "delivery_modes": ";".join(pack.delivery_modes),
                    "item_count": len(pack.items),
                    "foundation_items": difficulty_counts["foundation"],
                    "core_items": difficulty_counts["core"],
                    "extension_items": difficulty_counts["extension"],
                    "unspecified_difficulty_items": difficulty_counts[UNSPECIFIED_DIFFICULTY],
                }
            )


def _count_field(packs: tuple[ExamPack, ...], field_name: str) -> Counter[str]:
    values = []
    for pack in packs:
        value = str(getattr(pack, field_name)).strip() or "Unspecified"
        values.append(value)
    return Counter(values)


def _count_list_field(packs: tuple[ExamPack, ...], field_name: str) -> Counter[str]:
    values = []
    for pack in packs:
        entries = tuple(str(value).strip() for value in getattr(pack, field_name) if str(value).strip())
        values.extend(entries or ("Unspecified",))
    return Counter(values)


def _count_command_words(packs: tuple[ExamPack, ...]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for pack in packs:
        counter.update(item.command_word for item in pack.items if item.command_word)
    if not counter:
        counter.update(["Unspecified"])
    return counter


def _count_phases(packs: tuple[ExamPack, ...]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for pack in packs:
        counter.update(item.phase for item in pack.items if item.phase)
    if not counter:
        counter.update(["Unspecified"])
    return counter


def _count_standards(packs: tuple[ExamPack, ...]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for pack in packs:
        for item in pack.items:
            counter.update(item.standards)
    if not counter:
        counter.update(["Unspecified"])
    return counter


def _render_counter_section(title: str, counter: Counter[str]) -> list[str]:
    lines = [f"## {title}", "", "| Value | Resources |", "| --- | --- |"]
    for value, count in sorted(counter.items(), key=lambda item: (-item[1], item[0].lower())):
        lines.append(f"| {_table_cell(value)} | {count} |")
    lines.append("")
    return lines


def _render_item_counter_section(title: str, counter: Counter[str]) -> list[str]:
    lines = [f"## {title}", "", "| Value | Items |", "| --- | --- |"]
    for value, count in sorted(counter.items(), key=lambda item: (-item[1], item[0].lower())):
        lines.append(f"| {_table_cell(value)} | {count} |")
    lines.append("")
    return lines


def _render_difficulty_section(counter: Counter[str]) -> list[str]:
    lines = ["## Difficulty Coverage", "", "| Difficulty | Items |", "| --- | --- |"]
    for difficulty in DIFFICULTY_LABELS:
        lines.append(f"| {_table_cell(difficulty)} | {counter[difficulty]} |")
    lines.append("")
    return lines


def _count_difficulties(packs: tuple[ExamPack, ...]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for pack in packs:
        counter.update(_difficulty_label(item.difficulty) for item in pack.items)
    return counter


def _difficulty_counts_for_pack(pack: ExamPack) -> dict[str, int]:
    counter = Counter(_difficulty_label(item.difficulty) for item in pack.items)
    return {difficulty: counter[difficulty] for difficulty in DIFFICULTY_LABELS}


def _difficulty_label(difficulty: str) -> str:
    return difficulty if difficulty in DIFFICULTY_ORDER else UNSPECIFIED_DIFFICULTY


def _duration_label(pack: ExamPack) -> str:
    if not pack.duration_minutes:
        return "Unspecified"
    return f"{pack.duration_minutes} min"


def _total_marks(pack: ExamPack) -> int:
    return sum(item.marks for item in pack.items)


def _item_time_minutes(pack: ExamPack) -> int:
    return sum(item.time_minutes for item in pack.items)


def _rubric_point_count(pack: ExamPack) -> int:
    return sum(len(item.rubric) for item in pack.items)


def _command_words_for_pack(pack: ExamPack) -> tuple[str, ...]:
    return tuple(sorted({item.command_word for item in pack.items if item.command_word}))


def _phases_for_pack(pack: ExamPack) -> tuple[str, ...]:
    return tuple(sorted({item.phase for item in pack.items if item.phase}))


def _standards_for_pack(pack: ExamPack) -> tuple[str, ...]:
    return tuple(sorted({standard for item in pack.items for standard in item.standards}))


def _table_cell(value: str) -> str:
    return str(value).replace("|", "\\|")
