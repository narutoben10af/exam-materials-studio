from __future__ import annotations

import argparse
from pathlib import Path

from .inventory import build_inventory, render_inventory_markdown, write_inventory_csv
from .loader import ResourceLoadError, load_resource
from .presets import PresetError, get_preset, render_presets_markdown
from .renderer import (
    render_answer_key_html,
    render_answer_key_markdown,
    render_catalog_html,
    render_catalog_json,
    render_catalog_markdown,
    render_pack_html,
    render_pack_markdown,
)
from .scaffold import ScaffoldError, ScaffoldSpec, default_slug, scaffold_resource
from .validator import has_errors, render_validation_report, validate_resources


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="exam-materials-studio",
        description="Build printable education resources and answer keys from JSON, YAML, or CSV files.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build", help="Build one or more resource JSON, YAML, or CSV files")
    build_parser.add_argument("packs", nargs="+", type=Path)
    build_parser.add_argument("--out", type=Path, default=Path("generated"))
    build_parser.add_argument(
        "--formats",
        default="markdown,html",
        help="Comma-separated output formats: markdown, html",
    )

    validate_parser = subparsers.add_parser("validate", help="Validate one or more resource JSON, YAML, or CSV files")
    validate_parser.add_argument("packs", nargs="+", type=Path)
    validate_parser.add_argument(
        "--report",
        type=Path,
        help="Optional path for writing the validation report",
    )

    inventory_parser = subparsers.add_parser(
        "inventory",
        help="Summarize resource coverage across subjects, levels, systems, boards, and courses",
    )
    inventory_parser.add_argument("packs", nargs="+", type=Path)
    inventory_parser.add_argument(
        "--out",
        type=Path,
        help="Optional path for writing the Markdown inventory report",
    )
    inventory_parser.add_argument(
        "--csv",
        type=Path,
        help="Optional path for writing a resource-level CSV inventory",
    )

    presets_parser = subparsers.add_parser(
        "presets",
        help="List built-in scaffold presets for common education systems and levels",
    )
    presets_parser.add_argument(
        "--out",
        type=Path,
        help="Optional path for writing the Markdown preset list",
    )

    scaffold_parser = subparsers.add_parser(
        "scaffold",
        help="Create a starter resource JSON or CSV file",
    )
    scaffold_parser.add_argument("--title", required=True)
    scaffold_parser.add_argument("--preset", help="Built-in preset such as primary, cambridge-igcse, ap, or ib-dp")
    scaffold_parser.add_argument("--subject", required=True)
    scaffold_parser.add_argument("--level")
    scaffold_parser.add_argument("--out", required=True, type=Path)
    scaffold_parser.add_argument("--format", choices=["json", "yaml", "csv"], default="json")
    scaffold_parser.add_argument("--slug")
    scaffold_parser.add_argument("--resource-type")
    scaffold_parser.add_argument("--education-system")
    scaffold_parser.add_argument("--exam-board")
    scaffold_parser.add_argument("--course", default="")
    scaffold_parser.add_argument("--summary", default="")
    scaffold_parser.add_argument(
        "--learning-objectives",
        default="",
        help="Semicolon-separated learning objectives for the resource",
    )
    scaffold_parser.add_argument(
        "--curriculum-references",
        default="",
        help="Semicolon-separated curriculum, syllabus, or standards references",
    )
    scaffold_parser.add_argument(
        "--skills",
        default="",
        help="Semicolon-separated skills, for example: fractions;equivalent fractions",
    )
    scaffold_parser.add_argument("--force", action="store_true", help="Overwrite the output file if it exists")

    args = parser.parse_args(argv)
    if args.command == "build":
        return build_packs(args.packs, args.out, _parse_formats(args.formats))
    if args.command == "validate":
        return validate_packs(args.packs, args.report)
    if args.command == "inventory":
        return inventory_packs(args.packs, args.out, args.csv)
    if args.command == "presets":
        return list_presets(args.out)
    if args.command == "scaffold":
        return scaffold_pack(args)

    parser.error("unknown command")
    return 2


def build_packs(pack_paths: list[Path], output_dir: Path, formats: set[str]) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)
    packs = []

    for pack_path in pack_paths:
        try:
            pack = load_resource(pack_path)
        except ResourceLoadError as error:
            print(f"error: {pack_path}: {error}")
            return 1

        if "markdown" in formats:
            (output_dir / f"{pack.slug}.md").write_text(render_pack_markdown(pack), encoding="utf-8")
            (output_dir / f"{pack.slug}-answer-key.md").write_text(
                render_answer_key_markdown(pack),
                encoding="utf-8",
            )
        if "html" in formats:
            (output_dir / f"{pack.slug}.html").write_text(render_pack_html(pack), encoding="utf-8")
            (output_dir / f"{pack.slug}-answer-key.html").write_text(
                render_answer_key_html(pack),
                encoding="utf-8",
            )
        packs.append(pack)

    if "markdown" in formats:
        (output_dir / "index.md").write_text(render_catalog_markdown(packs), encoding="utf-8")
    (output_dir / "index.json").write_text(render_catalog_json(packs, formats=formats), encoding="utf-8")
    (output_dir / "index.html").write_text(render_catalog_html(packs, formats=formats), encoding="utf-8")
    print(f"Built {len(packs)} pack(s) into {output_dir}")
    return 0


def validate_packs(pack_paths: list[Path], report_path: Path | None = None) -> int:
    results = validate_resources(pack_paths)
    report = render_validation_report(results)
    print(report, end="")
    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding="utf-8")
    return 1 if has_errors(results) else 0


def inventory_packs(
    pack_paths: list[Path],
    report_path: Path | None = None,
    csv_path: Path | None = None,
) -> int:
    packs = []
    for pack_path in pack_paths:
        try:
            packs.append(load_resource(pack_path))
        except ResourceLoadError as error:
            print(f"error: {pack_path}: {error}")
            return 1

    inventory = build_inventory(packs)
    report = render_inventory_markdown(inventory)
    print(report, end="")
    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding="utf-8")
    if csv_path:
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        write_inventory_csv(inventory, csv_path)
    return 0


def scaffold_pack(args: argparse.Namespace) -> int:
    try:
        preset = get_preset(args.preset)
    except PresetError as error:
        print(f"error: {error}")
        return 1

    level = args.level or (preset.level if preset else None)
    if not level:
        print("error: --level is required when --preset is not provided")
        return 1

    resource_type = args.resource_type or (preset.resource_type if preset else "worksheet")
    education_system = args.education_system or (preset.education_system if preset else "")
    exam_board = args.exam_board or (preset.exam_board if preset else "")
    learning_objectives = _parse_skills(getattr(args, "learning_objectives", ""))
    if not learning_objectives:
        learning_objectives = (f"Practise {args.subject} skills through {resource_type} tasks.",)
    curriculum_references = _parse_skills(getattr(args, "curriculum_references", ""))
    if not curriculum_references:
        curriculum_references = (args.course or f"{education_system or args.level} {args.subject}",)
    skills = _parse_skills(args.skills) or (args.subject,)
    summary = args.summary or f"Starter {resource_type} for {args.subject} at {level} level."
    spec = ScaffoldSpec(
        title=args.title,
        slug=args.slug or default_slug(args.title),
        subject=args.subject,
        level=level,
        resource_type=resource_type,
        education_system=education_system,
        exam_board=exam_board,
        course=args.course,
        summary=summary,
        learning_objectives=learning_objectives,
        curriculum_references=curriculum_references,
        skills=skills,
    )
    try:
        scaffold_resource(spec, args.out, args.format, force=args.force)
    except ScaffoldError as error:
        print(f"error: {error}")
        return 1
    print(f"Created {args.format} scaffold at {args.out}")
    return 0


def list_presets(report_path: Path | None = None) -> int:
    report = render_presets_markdown()
    print(report, end="")
    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding="utf-8")
    return 0


def _parse_formats(raw_formats: str) -> set[str]:
    formats = {item.strip().lower() for item in raw_formats.split(",") if item.strip()}
    supported = {"markdown", "html"}
    unknown = formats - supported
    if unknown:
        raise SystemExit(f"unsupported format(s): {', '.join(sorted(unknown))}")
    return formats or {"markdown", "html"}


def _parse_skills(raw_skills: str) -> tuple[str, ...]:
    return tuple(skill.strip() for skill in raw_skills.split(";") if skill.strip())
