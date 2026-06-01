import json
import tempfile
import unittest
from pathlib import Path

from exam_materials_studio.validator import has_errors, render_validation_report, validate_resource


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
                            },
                            {
                                "prompt": "Explain why high temperature reduces enzyme activity.",
                                "answer": "High temperature denatures the enzyme and changes the active site.",
                                "explanation": "Denaturation changes the active site's shape, so fewer enzyme-substrate complexes form.",
                            },
                            {
                                "prompt": "Describe one controlled variable in an enzyme rate experiment.",
                                "answer": "The pH should be kept constant.",
                                "explanation": "Changing pH can also affect enzyme shape and would make temperature effects harder to interpret.",
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
            self.assertIn("Warnings:", report)
            self.assertIn("education_system is missing", report)
            self.assertIn("learning_objectives is missing", report)
            self.assertIn("curriculum_references is missing", report)
            self.assertIn("thin or missing explanations", report)


if __name__ == "__main__":
    unittest.main()
