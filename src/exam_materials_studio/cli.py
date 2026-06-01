from __future__ import annotations

import argparse
import json
from pathlib import Path

from .models import PackValidationError, pack_from_dict
from .renderer import render_answer_key_markdown, render_catalog_html, render_pack_markdown


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="exam-materials-studio",
        description="Build printable exam packs and answer keys from JSON pack files.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build", help="Build one or more pack JSON files")
    build_parser.add_argument("packs", nargs="+", type=Path)
    build_parser.add_argument("--out", type=Path, default=Path("generated"))

    args = parser.parse_args(argv)
    if args.command == "build":
        return build_packs(args.packs, args.out)

    parser.error("unknown command")
    return 2


def build_packs(pack_paths: list[Path], output_dir: Path) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)
    packs = []

    for pack_path in pack_paths:
        try:
            data = json.loads(pack_path.read_text(encoding="utf-8"))
            pack = pack_from_dict(data)
        except (json.JSONDecodeError, OSError, PackValidationError) as error:
            print(f"error: {pack_path}: {error}")
            return 1

        (output_dir / f"{pack.slug}.md").write_text(render_pack_markdown(pack), encoding="utf-8")
        (output_dir / f"{pack.slug}-answer-key.md").write_text(
            render_answer_key_markdown(pack),
            encoding="utf-8",
        )
        packs.append(pack)

    (output_dir / "index.html").write_text(render_catalog_html(packs), encoding="utf-8")
    print(f"Built {len(packs)} pack(s) into {output_dir}")
    return 0

