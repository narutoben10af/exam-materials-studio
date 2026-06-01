from __future__ import annotations

import argparse
from pathlib import Path

from .inventory import build_inventory, render_inventory_markdown, write_inventory_csv
from .loader import ResourceLoadError, load_resource
from .renderer import (
    render_answer_key_html,
    render_answer_key_markdown,
    render_catalog_html,
    render_pack_html,
    render_pack_markdown,
)
from .validator import has_errors, render_validation_report, validate_resources


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="exam-materials-studio",
        description="Build printable education resources and answer keys from JSON or CSV files.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build", help="Build one or more resource JSON or CSV files")
    build_parser.add_argument("packs", nargs="+", type=Path)
    build_parser.add_argument("--out", type=Path, default=Path("generated"))
    build_parser.add_argument(
        "--formats",
        default="markdown,html",
        help="Comma-separated output formats: markdown, html",
    )

    validate_parser = subparsers.add_parser("validate", help="Validate one or more resource JSON or CSV files")
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

    args = parser.parse_args(argv)
    if args.command == "build":
        return build_packs(args.packs, args.out, _parse_formats(args.formats))
    if args.command == "validate":
        return validate_packs(args.packs, args.report)
    if args.command == "inventory":
        return inventory_packs(args.packs, args.out, args.csv)

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

    (output_dir / "index.html").write_text(render_catalog_html(packs, formats=formats), encoding="utf-8")
    print(f"Built {len(packs)} pack(s) into {output_dir}")
    return 0


def validate_packs(pack_paths: list[Path], report_path: Path | None = None) -> int:
    results = validate_resources(pack_paths)
    report = render_validation_report(results)
    print(report, end="")
    if report_path:
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
        report_path.write_text(report, encoding="utf-8")
    if csv_path:
        write_inventory_csv(inventory, csv_path)
    return 0


def _parse_formats(raw_formats: str) -> set[str]:
    formats = {item.strip().lower() for item in raw_formats.split(",") if item.strip()}
    supported = {"markdown", "html"}
    unknown = formats - supported
    if unknown:
        raise SystemExit(f"unsupported format(s): {', '.join(sorted(unknown))}")
    return formats or {"markdown", "html"}
