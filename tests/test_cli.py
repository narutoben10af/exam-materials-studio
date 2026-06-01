import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from exam_materials_studio.cli import build_packs, inventory_packs, list_presets, main, scaffold_pack, validate_packs


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
            self.assertTrue((output_dir / "index.md").exists())
            self.assertIn("Primary Fractions Worksheet", (output_dir / "index.md").read_text(encoding="utf-8"))

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
            report_path = root / "reports" / "validation.txt"
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

    def test_scaffold_pack_creates_json_from_cli_args(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "scaffolds" / "primary-fractions.json"
            args = type(
                "Args",
                (),
                {
                    "title": "Primary Fractions",
                    "preset": None,
                    "subject": "Mathematics",
                    "level": "Primary",
                    "out": output_path,
                    "format": "json",
                    "slug": None,
                    "resource_type": "worksheet",
                    "education_system": "General primary",
                    "exam_board": "",
                    "course": "Fractions",
                    "summary": "",
                    "skills": "fractions;equivalent fractions",
                    "force": False,
                },
            )()

            with redirect_stdout(StringIO()):
                result = scaffold_pack(args)

            self.assertEqual(result, 0)
            self.assertTrue(output_path.exists())
            self.assertIn("primary-fractions", output_path.read_text(encoding="utf-8"))

    def test_scaffold_pack_applies_preset_when_level_is_omitted(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "scaffolds" / "igcse-chemistry.json"
            args = type(
                "Args",
                (),
                {
                    "title": "IGCSE Chemistry Acids Starter",
                    "preset": "cambridge-igcse",
                    "subject": "Chemistry",
                    "level": None,
                    "out": output_path,
                    "format": "json",
                    "slug": None,
                    "resource_type": None,
                    "education_system": None,
                    "exam_board": None,
                    "course": "0620 Chemistry",
                    "summary": "",
                    "skills": "acids;bases",
                    "force": False,
                },
            )()

            with redirect_stdout(StringIO()):
                result = scaffold_pack(args)

            data = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(result, 0)
            self.assertEqual(data["level"], "IGCSE")
            self.assertEqual(data["resource_type"], "exam-practice")
            self.assertEqual(data["education_system"], "Cambridge International")
            self.assertEqual(data["exam_board"], "Cambridge")

    def test_main_scaffold_accepts_preset_without_level_argument(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "scaffolds" / "primary-fractions.json"

            with redirect_stdout(StringIO()):
                result = main(
                    [
                        "scaffold",
                        "--preset",
                        "primary",
                        "--title",
                        "Primary Fractions",
                        "--subject",
                        "Mathematics",
                        "--course",
                        "Fractions",
                        "--learning-objectives",
                        "Represent equivalent fractions with simple models;Compare fraction models",
                        "--out",
                        str(output_path),
                    ]
                )

            data = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(result, 0)
            self.assertEqual(data["level"], "Primary")
            self.assertEqual(data["education_system"], "General primary")
            self.assertEqual(
                data["learning_objectives"],
                ["Represent equivalent fractions with simple models", "Compare fraction models"],
            )

    def test_scaffold_pack_requires_level_without_preset(self):
        args = type(
            "Args",
            (),
            {
                "title": "Untyped Resource",
                "preset": None,
                "subject": "Mathematics",
                "level": None,
                "out": Path("resource.json"),
                "format": "json",
                "slug": None,
                "resource_type": None,
                "education_system": None,
                "exam_board": None,
                "course": "",
                "summary": "",
                "skills": "",
                "force": False,
            },
        )()

        with redirect_stdout(StringIO()) as stdout:
            result = scaffold_pack(args)

        self.assertEqual(result, 1)
        self.assertIn("--level is required", stdout.getvalue())

    def test_scaffold_pack_reports_unknown_preset(self):
        args = type(
            "Args",
            (),
            {
                "title": "Mystery Resource",
                "preset": "unknown-system",
                "subject": "Mathematics",
                "level": None,
                "out": Path("resource.json"),
                "format": "json",
                "slug": None,
                "resource_type": None,
                "education_system": None,
                "exam_board": None,
                "course": "",
                "summary": "",
                "skills": "",
                "force": False,
            },
        )()

        with redirect_stdout(StringIO()) as stdout:
            result = scaffold_pack(args)

        self.assertEqual(result, 1)
        self.assertIn("unknown preset: unknown-system", stdout.getvalue())

    def test_scaffold_pack_allows_explicit_fields_to_override_preset(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "scaffolds" / "primary-history.csv"
            args = type(
                "Args",
                (),
                {
                    "title": "History Source Analysis",
                    "preset": "cambridge-igcse",
                    "subject": "History",
                    "level": "Primary",
                    "out": output_path,
                    "format": "csv",
                    "slug": None,
                    "resource_type": "discussion-guide",
                    "education_system": "Local primary",
                    "exam_board": "District",
                    "course": "History",
                    "summary": "",
                    "skills": "sources",
                    "force": False,
                },
            )()

            with redirect_stdout(StringIO()):
                result = scaffold_pack(args)

            output = output_path.read_text(encoding="utf-8")
            self.assertEqual(result, 0)
            self.assertIn("Primary", output)
            self.assertIn("discussion-guide", output)
            self.assertIn("Local primary", output)
            self.assertIn("District", output)

    def test_list_presets_writes_markdown_report(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "reports" / "presets.md"

            with redirect_stdout(StringIO()) as stdout:
                result = list_presets(output_path)

            self.assertEqual(result, 0)
            self.assertIn("cambridge-igcse", stdout.getvalue())
            self.assertIn("university", output_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
