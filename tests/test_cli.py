import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from exam_materials_studio.cli import build_packs, inventory_packs, validate_packs


class CliTests(unittest.TestCase):
    def test_build_packs_writes_markdown_and_html_outputs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pack_path = root / "resource.json"
            output_dir = root / "generated"
            pack_path.write_text(
                json.dumps(
                    {
                        "title": "Primary Fractions Worksheet",
                        "slug": "primary-fractions-worksheet",
                        "subject": "Mathematics",
                        "level": "Primary",
                        "resource_type": "worksheet",
                        "education_system": "General primary",
                        "summary": "A short worksheet for equivalent fractions.",
                        "skills": ["equivalent fractions"],
                        "items": [{"prompt": "Write one half as quarters.", "answer": "2/4"}],
                    }
                ),
                encoding="utf-8",
            )

            with redirect_stdout(StringIO()):
                result = build_packs([pack_path], output_dir, {"markdown", "html"})

            self.assertEqual(result, 0)
            self.assertTrue((output_dir / "primary-fractions-worksheet.md").exists())
            self.assertTrue((output_dir / "primary-fractions-worksheet.html").exists())
            self.assertTrue((output_dir / "primary-fractions-worksheet-answer-key.md").exists())
            self.assertTrue((output_dir / "primary-fractions-worksheet-answer-key.html").exists())
            self.assertTrue((output_dir / "index.html").exists())

    def test_build_packs_accepts_csv_resource(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pack_path = root / "resource.csv"
            output_dir = root / "generated"
            pack_path.write_text(
                "\n".join(
                    [
                        "title,slug,subject,level,resource_type,education_system,course,summary,skills,type,prompt,answer,explanation",
                        "Primary Science,primary-science,Science,Primary,lesson-resource,General primary,Materials,A materials lesson,classification;properties,activity,Sort objects by material.,Objects are grouped by material.,This checks classification by observable material properties.",
                        "Primary Science,primary-science,Science,Primary,lesson-resource,General primary,Materials,A materials lesson,classification;properties,question,Name one property of glass.,Glass is transparent.,Transparency is a useful property for windows.",
                        "Primary Science,primary-science,Science,Primary,lesson-resource,General primary,Materials,A materials lesson,classification;properties,discussion,Why use plastic for bottles?,Plastic is waterproof and light.,This links material properties to object function.",
                    ]
                ),
                encoding="utf-8",
            )

            with redirect_stdout(StringIO()):
                result = build_packs([pack_path], output_dir, {"markdown", "html"})

            self.assertEqual(result, 0)
            self.assertTrue((output_dir / "primary-science.md").exists())
            self.assertTrue((output_dir / "primary-science.html").exists())

    def test_validate_packs_writes_report(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pack_path = root / "resource.json"
            report_path = root / "validation.txt"
            pack_path.write_text(
                json.dumps(
                    {
                        "title": "Primary Fractions Worksheet",
                        "slug": "primary-fractions-worksheet",
                        "subject": "Mathematics",
                        "level": "Primary",
                        "resource_type": "worksheet",
                        "education_system": "General primary",
                        "course": "Fractions",
                        "summary": "A short worksheet for equivalent fractions.",
                        "skills": ["equivalent fractions"],
                        "items": [
                            {
                                "prompt": "Write one half as quarters.",
                                "answer": "2/4",
                                "explanation": "Two quarters cover the same amount as one half.",
                            },
                            {
                                "prompt": "Write two quarters as a fraction in simplest form.",
                                "answer": "1/2",
                                "explanation": "Both numerator and denominator can be divided by two.",
                            },
                            {
                                "prompt": "Circle the larger fraction: 1/4 or 1/2.",
                                "answer": "1/2",
                                "explanation": "One half is larger because it is two quarters.",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            with redirect_stdout(StringIO()):
                result = validate_packs([pack_path], report_path)

            self.assertEqual(result, 0)
            self.assertIn("PASS", report_path.read_text(encoding="utf-8"))

    def test_inventory_packs_writes_markdown_and_csv_reports(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pack_path = root / "resource.json"
            report_path = root / "reports" / "inventory.md"
            csv_path = root / "reports" / "inventory.csv"
            pack_path.write_text(
                json.dumps(
                    {
                        "title": "Primary Fractions Worksheet",
                        "slug": "primary-fractions-worksheet",
                        "subject": "Mathematics",
                        "level": "Primary",
                        "resource_type": "worksheet",
                        "education_system": "General primary",
                        "course": "Fractions",
                        "summary": "A short worksheet for equivalent fractions.",
                        "skills": ["equivalent fractions"],
                        "items": [
                            {
                                "prompt": "Write one half as quarters.",
                                "answer": "2/4",
                                "explanation": "Two quarters cover the same amount as one half.",
                            },
                            {
                                "prompt": "Write two quarters as a fraction in simplest form.",
                                "answer": "1/2",
                                "explanation": "Both numerator and denominator can be divided by two.",
                            },
                            {
                                "prompt": "Circle the larger fraction: 1/4 or 1/2.",
                                "answer": "1/2",
                                "explanation": "One half is larger because it is two quarters.",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            with redirect_stdout(StringIO()):
                result = inventory_packs([pack_path], report_path, csv_path)

            self.assertEqual(result, 0)
            self.assertIn("Resource Coverage Inventory", report_path.read_text(encoding="utf-8"))
            self.assertIn("Primary Fractions Worksheet", csv_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
