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
                    "duration_minutes": 15,
                    "delivery_modes": ["classroom", "tutoring"],
                    "summary": "Count small groups.",
                    "skills": ["counting"],
                    "items": [
                        {
                            "prompt": "Count two dots.",
                            "answer": "2",
                            "explanation": "Two dots are counted.",
                            "difficulty": "foundation",
                        },
                        {
                            "prompt": "Count three dots.",
                            "answer": "3",
                            "explanation": "Three dots are counted.",
                            "difficulty": "core",
                        },
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
                    "duration_minutes": 20,
                    "delivery_modes": ["revision", "self-study"],
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
        self.assertEqual(inventory.total_duration_minutes, 35)

    def test_markdown_report_contains_coverage_sections(self):
        report = render_inventory_markdown(build_inventory(self.packs))

        self.assertIn("# Resource Coverage Inventory", report)
        self.assertIn("- Planned time: 35 minutes", report)
        self.assertIn("## Subjects", report)
        self.assertIn("## Delivery Modes", report)
        self.assertIn("| classroom | 1 |", report)
        self.assertIn("| self-study | 1 |", report)
        self.assertIn("## Difficulty Coverage", report)
        self.assertIn("| foundation | 1 |", report)
        self.assertIn("| core | 1 |", report)
        self.assertIn("| extension | 0 |", report)
        self.assertIn("| unspecified | 1 |", report)
        self.assertIn("| Economics | 1 |", report)
        self.assertIn("| Preschool | 1 |", report)
        self.assertIn("0455 Economics", report)
        self.assertIn(
            "| Preschool Counting | Preschool | Early Mathematics | activity-sheet | Counting | 15 min | 2 | 1 | 1 | 0 | 0 |",
            report,
        )
        self.assertIn(
            "| IGCSE Economics Definitions | IGCSE | Economics | definitions-drill | 0455 Economics | 20 min | 1 | 0 | 0 | 0 | 1 |",
            report,
        )

    def test_writes_resource_level_csv_inventory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "inventory.csv"
            write_inventory_csv(build_inventory(self.packs), path)

            with path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))

            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["title"], "Preschool Counting")
            self.assertEqual(rows[0]["duration_minutes"], "15")
            self.assertEqual(rows[0]["delivery_modes"], "classroom;tutoring")
            self.assertEqual(rows[0]["foundation_items"], "1")
            self.assertEqual(rows[0]["core_items"], "1")
            self.assertEqual(rows[0]["extension_items"], "0")
            self.assertEqual(rows[0]["unspecified_difficulty_items"], "0")
            self.assertEqual(rows[1]["course"], "0455 Economics")
            self.assertEqual(rows[1]["duration_minutes"], "20")
            self.assertEqual(rows[1]["delivery_modes"], "revision;self-study")
            self.assertEqual(rows[1]["unspecified_difficulty_items"], "1")


if __name__ == "__main__":
    unittest.main()
