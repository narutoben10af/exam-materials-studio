import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from exam_materials_studio.cli import (
    build_packs,
    inventory_packs,
    list_presets,
    main,
    pathway_packs,
    scaffold_pack,
    validate_packs,
)


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
            self.assertTrue((output_dir / "index.json").exists())
            self.assertIn("Primary Fractions Worksheet", (output_dir / "index.md").read_text(encoding="utf-8"))
            catalog = json.loads((output_dir / "index.json").read_text(encoding="utf-8"))
            self.assertEqual(catalog["resource_count"], 1)
            self.assertEqual(catalog["resources"][0]["slug"], "primary-fractions-worksheet")
            self.assertEqual(catalog["resources"][0]["files"]["html"], "primary-fractions-worksheet.html")

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

    def test_build_packs_accepts_yaml_resource(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pack_path = root / "resource.yaml"
            output_dir = root / "generated"
            pack_path.write_text(
                """title: Primary Fractions YAML
slug: primary-fractions-yaml
subject: Mathematics
level: Primary
resource_type: worksheet
education_system: General primary
course: Fractions
summary: A YAML-authored fractions resource.
skills:
  - equivalent fractions
items:
  - difficulty: foundation
    prompt: Write one half as quarters.
    answer: 2/4
    explanation: Two quarters cover the same amount as one half.
""",
                encoding="utf-8",
            )

            with redirect_stdout(StringIO()):
                result = build_packs([pack_path], output_dir, {"markdown", "html"})

            self.assertEqual(result, 0)
            self.assertTrue((output_dir / "primary-fractions-yaml.md").exists())
            catalog = json.loads((output_dir / "index.json").read_text(encoding="utf-8"))
            self.assertEqual(catalog["resources"][0]["slug"], "primary-fractions-yaml")
            self.assertEqual(catalog["resources"][0]["difficulty_counts"], {"foundation": 1})

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

    def test_pathway_packs_writes_ordered_markdown_report(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pack_path = root / "resource.json"
            report_path = root / "reports" / "pathway.md"
            csv_path = root / "reports" / "pathway.csv"
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
                        "unit": "Equivalent fractions",
                        "sequence_order": 1,
                        "duration_minutes": 20,
                        "delivery_modes": ["classroom"],
                        "learning_objectives": ["Represent equivalent fractions"],
                        "summary": "A short worksheet for equivalent fractions.",
                        "skills": ["equivalent fractions"],
                        "items": [{"prompt": "Write one half as quarters.", "answer": "2/4"}],
                    }
                ),
                encoding="utf-8",
            )

            with redirect_stdout(StringIO()):
                result = pathway_packs([pack_path], report_path, csv_path)

            self.assertEqual(result, 0)
            report = report_path.read_text(encoding="utf-8")
            self.assertIn("# Learning Pathway", report)
            self.assertIn("## Primary / Mathematics / Fractions", report)
            self.assertIn("| 1 | [Primary Fractions Worksheet](primary-fractions-worksheet.md)", report)
            csv_output = csv_path.read_text(encoding="utf-8")
            self.assertIn("level,subject,course,unit,sequence_order,title", csv_output)
            self.assertIn("Primary,Mathematics,Fractions,Equivalent fractions,1,Primary Fractions Worksheet", csv_output)

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
                        "--unit",
                        "Fraction equivalence",
                        "--sequence-order",
                        "4",
                        "--learning-objectives",
                        "Represent equivalent fractions with simple models;Compare fraction models",
                        "--curriculum-references",
                        "Local Grade 4 Fractions;School Scheme 2.1",
                        "--out",
                        str(output_path),
                    ]
                )

            data = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(result, 0)
            self.assertEqual(data["level"], "Primary")
            self.assertEqual(data["education_system"], "General primary")
            self.assertEqual(data["unit"], "Fraction equivalence")
            self.assertEqual(data["sequence_order"], 4)
            self.assertEqual(
                data["learning_objectives"],
                ["Represent equivalent fractions with simple models", "Compare fraction models"],
            )
            self.assertEqual(data["curriculum_references"], ["Local Grade 4 Fractions", "School Scheme 2.1"])

    def test_main_scaffold_creates_yaml_resource(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "scaffolds" / "primary-fractions.yaml"

            with redirect_stdout(StringIO()):
                result = main(
                    [
                        "scaffold",
                        "--preset",
                        "primary",
                        "--title",
                        "Primary Fractions YAML",
                        "--subject",
                        "Mathematics",
                        "--course",
                        "Fractions",
                        "--unit",
                        "Fraction equivalence",
                        "--sequence-order",
                        "4",
                        "--learning-objectives",
                        "Represent equivalent fractions with simple models",
                        "--curriculum-references",
                        "Local Grade 4 Fractions",
                        "--skills",
                        "fractions;equivalent fractions",
                        "--duration-minutes",
                        "45",
                        "--prerequisites",
                        "Recognise equal parts;Count quarters",
                        "--materials",
                        "Fraction strips;Counters",
                        "--delivery-modes",
                        "classroom;tutoring",
                        "--format",
                        "yaml",
                        "--out",
                        str(output_path),
                    ]
                )

            self.assertEqual(result, 0)
            output = output_path.read_text(encoding="utf-8")
            self.assertIn("title: Primary Fractions YAML", output)
            self.assertIn("unit: Fraction equivalence", output)
            self.assertIn("sequence_order: 4", output)
            self.assertIn("duration_minutes: 45", output)
            self.assertIn("Recognise equal parts", output)
            self.assertIn("Count quarters", output)
            self.assertIn("Fraction strips", output)
            self.assertIn("Counters", output)
            self.assertIn("classroom", output)
            self.assertIn("tutoring", output)
            self.assertIn("marks: 1", output)
            self.assertIn("command_word: identify", output)
            self.assertIn("phase: warm-up", output)
            self.assertIn("time_minutes: 5", output)
            self.assertIn("standards:", output)
            self.assertIn("Count quarters", output)
            self.assertIn("rubric:", output)
            self.assertIn("Award credit for a clear, correct response.", output)

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
