import json
import tempfile
import unittest
from pathlib import Path

from exam_materials_studio.validator import (
    has_errors,
    has_warnings,
    render_validation_json,
    render_validation_report,
    validate_resource,
)


class ValidatorTests(unittest.TestCase):
    def test_valid_resource_without_quality_warnings_passes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "resource.json"
            path.write_text(
                json.dumps(
                    {
                        "title": "A Level Biology Enzymes Worksheet",
                        "slug": "a-level-biology-enzymes-worksheet",
                        "subject": "Biology",
                        "level": "A Level",
                        "resource_type": "worksheet",
                        "education_system": "Cambridge International",
                        "exam_board": "Cambridge",
                        "course": "9700 Biology",
                        "duration_minutes": 35,
                        "summary": "Practice on enzyme structure and rates of reaction.",
                        "learning_objectives": [
                            "Describe how enzyme structure supports catalysis.",
                            "Interpret rate changes in enzyme experiments.",
                        ],
                        "curriculum_references": ["Cambridge 9700 3.1"],
                        "skills": ["enzyme structure", "reaction rates"],
                        "items": [
                            {
                                "prompt": "Define active site.",
                                "answer": "The region of an enzyme where the substrate binds.",
                                "explanation": "This definition identifies the enzyme region and its substrate-binding role.",
                                "difficulty": "foundation",
                            },
                            {
                                "prompt": "Explain why high temperature reduces enzyme activity.",
                                "answer": "High temperature denatures the enzyme and changes the active site.",
                                "explanation": "Denaturation changes the active site's shape, so fewer enzyme-substrate complexes form.",
                                "difficulty": "core",
                            },
                            {
                                "prompt": "Describe one controlled variable in an enzyme rate experiment.",
                                "answer": "The pH should be kept constant.",
                                "explanation": "Changing pH can also affect enzyme shape and would make temperature effects harder to interpret.",
                                "difficulty": "extension",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            result = validate_resource(path)

            self.assertTrue(result.ok)
            self.assertEqual(result.warnings, ())

    def test_invalid_resource_returns_error(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "broken.json"
            path.write_text('{"title": "Broken"}', encoding="utf-8")

            result = validate_resource(path)

            self.assertFalse(result.ok)
            self.assertIn("Missing required fields", result.errors[0].message)

    def test_quality_warnings_surface_missing_metadata_and_thin_explanations(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "thin.json"
            path.write_text(
                json.dumps(
                    {
                        "title": "Thin Resource",
                        "slug": "thin-resource",
                        "subject": "Mathematics",
                        "level": "Primary",
                        "summary": "A thin sample.",
                        "skills": ["addition"],
                        "items": [{"prompt": "1 + 1", "answer": "2"}],
                    }
                ),
                encoding="utf-8",
            )

            result = validate_resource(path)
            report = render_validation_report([result])

            self.assertTrue(result.ok)
            self.assertFalse(has_errors([result]))
            self.assertTrue(has_warnings([result]))
            self.assertIn("Warnings:", report)
            self.assertIn("education_system is missing", report)
            self.assertIn("learning_objectives is missing", report)
            self.assertIn("curriculum_references is missing", report)
            self.assertIn("duration_minutes is missing", report)
            self.assertIn("missing difficulty for item(s): 1", report)
            self.assertIn("thin or missing explanations", report)

    def test_json_report_contains_versioned_summary_and_structured_resources(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            valid_path = root / "valid.json"
            warning_path = root / "warning.json"
            invalid_path = root / "broken.json"
            valid_path.write_text(
                json.dumps(
                    {
                        "title": "Primary Number Bonds Practice",
                        "slug": "primary-number-bonds-practice",
                        "subject": "Mathematics",
                        "level": "Primary",
                        "resource_type": "practice-set",
                        "education_system": "General primary",
                        "course": "Number",
                        "duration_minutes": 20,
                        "learning_objectives": ["Recall number bonds within 20."],
                        "curriculum_references": ["Primary mathematics: number"],
                        "summary": "Practice recalling number bonds.",
                        "skills": ["number bonds"],
                        "items": [
                            {
                                "prompt": "Complete: 7 + __ = 10.",
                                "answer": "3",
                                "explanation": "Seven and three combine to make ten.",
                                "difficulty": "foundation",
                            },
                            {
                                "prompt": "Complete: 8 + __ = 15.",
                                "answer": "7",
                                "explanation": "Eight and seven combine to make fifteen.",
                                "difficulty": "core",
                            },
                            {
                                "prompt": "Explain two ways to make 18.",
                                "answer": "For example, 10 + 8 and 9 + 9.",
                                "explanation": "Both pairs have a total value of eighteen.",
                                "difficulty": "extension",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            warning_path.write_text(
                json.dumps(
                    {
                        "title": "Draft Number Bonds Practice",
                        "slug": "draft-number-bonds-practice",
                        "subject": "Mathematics",
                        "level": "Primary",
                        "summary": "An intentionally incomplete draft.",
                        "skills": ["number bonds"],
                        "items": [{"prompt": "Complete: 6 + __ = 10.", "answer": "4"}],
                    }
                ),
                encoding="utf-8",
            )
            invalid_path.write_text('{"title": "Broken"}', encoding="utf-8")
            results = [
                validate_resource(valid_path),
                validate_resource(warning_path),
                validate_resource(invalid_path),
            ]

            report = json.loads(render_validation_json(results))

            self.assertEqual(report["schema_version"], 1)
            self.assertEqual(
                report["summary"],
                {
                    "checked": 3,
                    "passed": 2,
                    "failed": 1,
                    "errors": 1,
                    "warnings": len(results[1].warnings),
                },
            )
            self.assertEqual(report["resources"][0]["status"], "pass")
            self.assertEqual(report["resources"][0]["title"], "Primary Number Bonds Practice")
            self.assertEqual(report["resources"][0]["errors"], [])
            self.assertEqual(report["resources"][1]["status"], "pass")
            self.assertGreater(len(report["resources"][1]["warnings"]), 0)
            self.assertEqual(report["resources"][2]["status"], "fail")
            self.assertEqual(report["resources"][2]["title"], "broken.json")
            self.assertEqual(report["resources"][2]["errors"][0]["level"], "error")
            self.assertIn("Missing required fields", report["resources"][2]["errors"][0]["message"])


if __name__ == "__main__":
    unittest.main()
