from __future__ import annotations

import argparse
import json
from pathlib import Path

from .models import PackValidationError, pack_from_dict
from .renderer import (
    render_answer_key_html,
    render_answer_key_markdown,
    render_catalog_html,
    render_pack_html,
    render_pack_markdown,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="exam-materials-studio",
        description="Build printable education resources and answer keys from JSON files.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build", help="Build one or more resource JSON files")
    build_parser.add_argument("packs", nargs="+", type=Path)
    build_parser.add_argument("--out", type=Path, default=Path("generated"))
    build_parser.add_argument(
        "--formats",
        default="markdown,html",
        help="Comma-separated output formats: markdown, html",
    )

    args = parser.parse_args(argv)
    if args.command == "build":
        return build_packs(args.packs, args.out, _parse_formats(args.formats))

    parser.error("unknown command")
    return 2


def build_packs(pack_paths: list[Path], output_dir: Path, formats: set[str]) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)
    packs = []

    for pack_path in pack_paths:
        try:
            data = json.loads(pack_path.read_text(encoding="utf-8"))
            pack = pack_from_dict(data)
        except (json.JSONDecodeError, OSError, PackValidationError) as error:
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


def _parse_formats(raw_formats: str) -> set[str]:
    formats = {item.strip().lower() for item in raw_formats.split(",") if item.strip()}
    supported = {"markdown", "html"}
    unknown = formats - supported
    if unknown:
        raise SystemExit(f"unsupported format(s): {', '.join(sorted(unknown))}")
    return formats or {"markdown", "html"}
