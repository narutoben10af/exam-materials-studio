import csv
import tempfile
import unittest
from pathlib import Path

from exam_materials_studio.inventory import build_inventory, render_inventory_markdown, write_inventory_csv
from exam_materials_studio.models import pack_from_dict


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.packs = [
            pack_from_dict(
                {
                    "title": "Preschool Counting",
                    "slug": "preschool-counting",
                    "subject": "Early Mathematics",
                    "level": "Preschool",
                    "resource_type": "activity-sheet",
                    "education_system": "General early years",
                    "course": "Counting",
                    "summary": "Count small groups.",
                    "skills": ["counting"],
                    "items": [
                        {"prompt": "Count two dots.", "answer": "2", "explanation": "Two dots are counted."},
                        {"prompt": "Count three dots.", "answer": "3", "explanation": "Three dots are counted."},
                    ],
                }
            ),
            pack_from_dict(
                {
                    "title": "IGCSE Economics Definitions",
                    "slug": "igcse-economics-definitions",
                    "subject": "Economics",
                    "level": "IGCSE",
                    "resource_type": "definitions-drill",
                    "education_system": "Cambridge International",
                    "exam_board": "Cambridge",
                    "course": "0455 Economics",
                    "summary": "Define key economics terms.",
                    "skills": ["definitions"],
                    "items": [{"prompt": "Define scarcity.", "answer": "Limited resources.", "explanation": "Resources are limited."}],
                }
            ),
        ]

    def test_inventory_counts_resources_and_items(self):
        inventory = build_inventory(self.packs)

        self.assertEqual(inventory.resource_count, 2)
        self.assertEqual(inventory.item_count, 3)

    def test_markdown_report_contains_coverage_sections(self):
        report = render_inventory_markdown(build_inventory(self.packs))

        self.assertIn("# Resource Coverage Inventory", report)
        self.assertIn("## Subjects", report)
        self.assertIn("| Economics | 1 |", report)
        self.assertIn("| Preschool | 1 |", report)
        self.assertIn("0455 Economics", report)

    def test_writes_resource_level_csv_inventory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "inventory.csv"
            write_inventory_csv(build_inventory(self.packs), path)

            with path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))

            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["title"], "Preschool Counting")
            self.assertEqual(rows[1]["course"], "0455 Economics")


if __name__ == "__main__":
    unittest.main()

